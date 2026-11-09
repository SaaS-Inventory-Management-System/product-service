from abc import ABC, abstractmethod
from uuid import UUID

from ..domain.entities import Article, Category


class ArticleRepository(ABC):
    @abstractmethod
    def get_by_sku(self, tenant_id: UUID, sku: str) -> Article | None:
        ...

    @abstractmethod
    def save(self, article: Article) -> None:
        ...

    @abstractmethod
    def get_by_id(self, tenant_id: UUID, article_id: UUID) -> Article | None:
        ...

    @abstractmethod
    def list_articles(self, tenant_id: UUID) -> list[Article]:
        ...

    @abstractmethod
    def search(self, tenant_id: UUID, query: str) -> list[Article]:
        ...

    @abstractmethod
    def has_active_articles_in_category(self, tenant_id: UUID, category_id: UUID) -> bool:
        ...

class CategoryRepository(ABC):
    @abstractmethod
    def get_by_name(self, tenant_id: UUID, name: str) -> Category | None:
        ...

    @abstractmethod
    def save(self, category: Category) -> None:
        ...

    @abstractmethod
    def get_by_id(self, tenant_id: UUID, category_id: UUID) -> Category | None:
        ...

    @abstractmethod
    def list_categories(self, tenant_id: UUID) -> list[Category]:
        ...

    @abstractmethod
    def search(self, tenant_id: UUID, query: str) -> list[Category]:
        ...