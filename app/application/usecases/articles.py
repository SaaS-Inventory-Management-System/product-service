from uuid import UUID, uuid4

from app.domain.entities import Article
from app.application.ports import ArticleRepository, CategoryRepository

from ...domain.errors import ArticleNotFoundError, ArticleAlreadyExistsError, CategoryNotFoundError

class CreateArticle:
    def __init__(
        self, 
        repository: ArticleRepository, 
        category_repository: CategoryRepository
    ):
        self.repository = repository
        self.category_repository = category_repository

    def __call__(
        self,
        tenant_id: UUID,
        name: str,
        sku: str,
        unit: str,
        category_id: UUID | None = None
    ) -> Article:

        article = Article(
            id=uuid4(),
            tenant_id=tenant_id,
            name=name,
            sku=sku,
            unit=unit,
            category_id=category_id
        )

        if category_id is not None:
            category = self.category_repository.get_by_id(tenant_id, category_id)
            if category is None:
                raise CategoryNotFoundError(
                    f"Category with ID '{category_id}' does not exist."
                )
        
        existing_article = self.repository.get_by_sku(
            tenant_id=tenant_id,
            sku=sku
        )

        if existing_article is not None:
            raise ArticleAlreadyExistsError(
                f"Article with code '{existing_article.sku}' already exists."
            )
        
        self.repository.save(article)

        return article

class GetArticle:
    def __init__(self, repository: ArticleRepository):
        self.repository = repository

    def __call__(self, tenant_id: UUID, article_id: UUID) -> Article:
        article = self.repository.get_by_id(tenant_id, article_id)

        if article is None:
            raise ArticleNotFoundError(
                f"Article with ID '{article_id}' does not exist."
            )

        return article

class ListArticles:
    def __init__(self, repository: ArticleRepository):
        self.repository = repository

    def __call__(self, tenant_id: UUID) -> list[Article]:
        return self.repository.list_articles(tenant_id)

class SearchArticles:
    def __init__(self, repository: ArticleRepository):
        self.repository = repository

    def __call__(self, tenant_id: UUID, query: str) -> list[Article]:
        query = query.strip()

        if not query:
            raise ValueError("The search string cannot be empty.")
        
        return self.repository.search(tenant_id, query)

class UpdateArticle:
    def __init__(
        self, 
        repository: ArticleRepository,
        category_repository: CategoryRepository
    ):
        self.repository = repository
        self.category_repository = category_repository

    def __call__(
        self,
        tenant_id: UUID,
        article_id: UUID,
        name: str,
        sku: str,
        unit: str,
        category_id: UUID | None = None
    ) -> Article:
        article = self.repository.get_by_id(tenant_id, article_id)
        
        if article is None:
            raise ArticleNotFoundError(
                f"Article with ID '{article_id}' does not exist."
            )

        updated_article = article.with_updated_details(
            name=name,
            sku=sku,
            unit=unit,
            category_id=category_id
        )

        if category_id is not None:
            category = self.category_repository.get_by_id(tenant_id, category_id)
            if category is None:
                raise CategoryNotFoundError(
                    f"Category with ID '{category_id}' does not exist."
                )

        existing_article = self.repository.get_by_sku(
            tenant_id=tenant_id,
            sku=updated_article.sku
        )
        if (
            existing_article is not None
            and existing_article.id != article_id
        ):
            raise ArticleAlreadyExistsError(
                f"Article with code '{sku}' already exists."
            )

        self.repository.save(updated_article)

        return updated_article

class DeleteArticle:
    def __init__(self, repository: ArticleRepository):
        self.repository = repository

    def __call__(self, tenant_id: UUID, article_id: UUID) -> None:
        article = self.repository.get_by_id(tenant_id, article_id)

        if article is None:
            raise ArticleNotFoundError(
                f"Article with ID '{article_id}' does not exist."
            )

        deleted_article = article.mark_deleted()
        self.repository.save(deleted_article)



