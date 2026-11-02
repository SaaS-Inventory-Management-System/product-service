from uuid import uuid4

import pytest

from app.domain.entities import Article


def test_create_article():
    article = Article(
        id=uuid4(),
        tenant_id=uuid4(),
        name="Vijak M8",
        sku="V-M8",
        unit="kos"
    )

    assert article.name == "Vijak M8"
    assert article.sku == "V-M8"
    assert article.unit == "kos"


def test_article_without_name():
    with pytest.raises(ValueError):
        Article(
            id=uuid4(),
            tenant_id=uuid4(),
            name="",
            sku="V-M8",
            unit="kos"
        )