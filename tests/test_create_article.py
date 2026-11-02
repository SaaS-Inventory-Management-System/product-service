from uuid import UUID, uuid4

import pytest

from app.domain.entities import Article
from app.domain.ports import ArticleRepository
from app.application.usecases.article import (
    CreateArticle
)
from app.domain.errors import (
    ArticleAlreadyExistsError
)

class FakeArticleRepository(ArticleRepository):

    def __init__(self):
        self.articles: dict[tuple[UUID, str], Article] = {}

    def get_by_sku(
        self,
        tenant_id: UUID,
        sku: str
    ) -> Article | None:

        return self.articles.get((tenant_id, sku))

    def save(self, article: Article) -> None:

        self.articles[(article.tenant_id, article.sku)] = article


def test_create_article():

    repository = FakeArticleRepository()

    use_case = CreateArticle(repository)

    tenant_id = uuid4()

    article = use_case(
        tenant_id=tenant_id,
        name="Vijak M8",
        sku="V-M8",
        unit="kos"
    )

    assert article.name == "Vijak M8"
    assert article.sku == "V-M8"

    saved_article = repository.get_by_sku(
        tenant_id=tenant_id,
        sku="V-M8"
    )

    assert saved_article == article

def test_create_article_with_duplicate_sku():

    repository = FakeArticleRepository()

    use_case = CreateArticle(repository)

    tenant_id = uuid4()

    use_case(
        tenant_id=tenant_id,
        name="Vijak M8",
        sku="V-M8",
        unit="kos"
    )

    with pytest.raises(ArticleAlreadyExistsError):

        use_case(
            tenant_id=tenant_id,
            name="Drug vijak",
            sku="V-M8",
            unit="kos"
        )