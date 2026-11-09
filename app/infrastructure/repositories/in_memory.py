from uuid import UUID

from app.domain.entities import Article, Category
from app.application.ports import ArticleRepository, CategoryRepository


class InMemoryArticleRepository(ArticleRepository):

    def __init__(self):
        self.articles: dict[tuple[UUID, UUID], Article] = {}

    def save(self, article: Article) -> None:
        self.articles[(article.tenant_id, article.id)] = article

    def get_by_id(
        self,
        tenant_id: UUID,
        article_id: UUID
    ) -> Article | None:

        article = self.articles.get((tenant_id, article_id))

        if article is not None and article.deleted_at is None:
            return article

        return None

    def get_by_sku(
        self,
        tenant_id: UUID,
        sku: str
    ) -> Article | None:

        for article in self.articles.values():
            if (
                article.tenant_id == tenant_id
                and article.sku == sku
                and article.deleted_at is None
            ):
                return article

        return None

    def list_articles(self, tenant_id: UUID) -> list[Article]:
        return [
            article
            for article in self.articles.values()
            if article.tenant_id == tenant_id
            and article.deleted_at is None
        ]

    def search(
        self,
        tenant_id: UUID,
        query: str
    ) -> list[Article]:

        query = query.casefold()

        return [
            article
            for article in self.articles.values()
            if article.tenant_id == tenant_id
            and article.deleted_at is None
            and (
                query in article.name.casefold()
                or query in article.sku.casefold()
            )
        ]

    def has_active_articles_in_category(
        self,
        tenant_id: UUID,
        category_id: UUID
    ) -> bool:

        return any(
            article.tenant_id == tenant_id
            and article.category_id == category_id
            and article.deleted_at is None
            for article in self.articles.values()
        )


class InMemoryCategoryRepository(CategoryRepository):

    def __init__(self):
        self.categories: dict[tuple[UUID, UUID], Category] = {}

    def save(self, category: Category) -> None:
        self.categories[(category.tenant_id, category.id)] = category

    def get_by_id(
        self,
        tenant_id: UUID,
        category_id: UUID
    ) -> Category | None:

        category = self.categories.get((tenant_id, category_id))

        if category is not None and category.deleted_at is None:
            return category

        return None

    def get_by_name(
        self,
        tenant_id: UUID,
        name: str
    ) -> Category | None:

        name = name.strip().casefold()

        for category in self.categories.values():
            if (
                category.tenant_id == tenant_id
                and category.name.casefold() == name
                and category.deleted_at is None
            ):
                return category

        return None

    def list_categories(self, tenant_id: UUID) -> list[Category]:

        return [
            category
            for category in self.categories.values()
            if category.tenant_id == tenant_id
            and category.deleted_at is None
        ]

    def search(
        self,
        tenant_id: UUID,
        query: str
    ) -> list[Category]:

        query = query.strip().casefold()

        return [
            category
            for category in self.categories.values()
            if category.tenant_id == tenant_id
            and category.deleted_at is None
            and query in category.name.casefold()
        ]