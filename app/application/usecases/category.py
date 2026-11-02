from uuid import UUID, uuid4

from app.domain.entities import Category
from app.domain.ports import CategoryRepository, ArticleRepository

from ...domain.errors import CategoryNotFoundError, CategoryAlreadyExistsError, CategoryInUseError

class CreateCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def __call__(
        self,
        tenant_id: UUID,
        name: str,
    ) -> Category:

        category = Category(
            id=uuid4(),
            tenant_id=tenant_id,
            name=name
        )
        
        existing_category = self.repository.get_by_name(
            tenant_id=tenant_id,
            name=name
        )

        if existing_category is not None:
            raise CategoryAlreadyExistsError(
                f"Category with name '{existing_category.name}' already exists."
            )
        
        self.repository.save(category)

        return category

class GetCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def __call__(self, tenant_id: UUID, category_id: UUID) -> Category:
        category = self.repository.get_by_id(tenant_id, category_id)

        if category is None:
            raise CategoryNotFoundError(
                f"Category with ID '{category_id}' does not exist."
            )

        return category

class ListCategories:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def __call__(self, tenant_id: UUID) -> list[Category]:
        return self.repository.list_categories(tenant_id)

class SearchCategories:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def __call__(self, tenant_id: UUID, query: str) -> list[Category]:
        query = query.strip()

        if not query:
            raise ValueError("The search string cannot be empty.")
        
        return self.repository.search(tenant_id, query)

class UpdateCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def __call__(
        self,
        tenant_id: UUID,
        category_id: UUID,
        name: str,
    ) -> Category:
        category = self.repository.get_by_id(tenant_id, category_id)
        
        if category is None:
            raise CategoryNotFoundError(
                f"Category with ID '{category_id}' does not exist."
            )

        updated_category = category.with_updated_details(
            name=name
        )

        existing_category = self.repository.get_by_name(
            tenant_id=tenant_id,
            name=updated_category.name
        )

        if (
            existing_category is not None
            and existing_category.id != category_id
        ):
            raise CategoryAlreadyExistsError(
                f"Category with name '{name}' already exists."
            )

        self.repository.save(updated_category)

        return updated_category

class DeleteCategory:
    def __init__(
        self, 
        repository: CategoryRepository, 
        article_repository: ArticleRepository
    ):
        self.repository = repository
        self.article_repository = article_repository

    def __call__(self, tenant_id: UUID, category_id: UUID) -> None:
        category = self.repository.get_by_id(tenant_id, category_id)

        if category is None:
            raise CategoryNotFoundError(
                f"Category with ID '{category_id}' does not exist."
            )

        if self.article_repository.has_active_articles_in_category(
            tenant_id=tenant_id,
            category_id=category_id
        ):
            raise CategoryInUseError(
                "Cannot delete category because it contains active articles."
            )

        deleted_category = category.mark_deleted()
        self.repository.save(deleted_category)



