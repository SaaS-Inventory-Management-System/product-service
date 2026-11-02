from fastapi import FastAPI

from app.presentation.routers.health import router as health_router
from app.presentation.routers.articles import create_router as create_articles_router
from app.presentation.routers.categories import create_router as create_categories_router

from app.fakes.repositories import (
    InMemoryArticleRepository,
    InMemoryCategoryRepository
)


app = FastAPI(title="Product Service")

articles_repository = InMemoryArticleRepository()
categories_repository = InMemoryCategoryRepository()

app.include_router(health_router)
app.include_router(create_articles_router(articles_repository, categories_repository))
app.include_router(create_categories_router(categories_repository, articles_repository))