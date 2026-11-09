"""Web layer: the FastAPI delivery mechanism.

It receives the injected use cases, exposes them as HTTP routes, and
translates domain errors into HTTP status codes. This is the only place that
imports FastAPI.
"""
from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.domain.errors import ArticleNotFoundError, ArticleAlreadyExistsError, CategoryNotFoundError
from app.application.usecases.articles import (
    GetArticle, 
    CreateArticle,
    ListArticles,
    SearchArticles,
    UpdateArticle,
    DeleteArticle
)
from app.application.ports import ArticleRepository, CategoryRepository
from app.presentation.schemas import (
    ArticleCreateRequest, 
    ArticleResponse,
    ArticleUpdateRequest,
)

# TEMPORARY
DEV_TENANT_ID = UUID("11111111-1111-4111-8111-111111111111")

def create_router(
    repository: ArticleRepository, 
    category_repository: CategoryRepository
) -> APIRouter:
    
    router = APIRouter(prefix="/articles", tags=["Articles"])

    # usecases
    create_article_use_case = CreateArticle(repository, category_repository)
    get_article_use_case = GetArticle(repository)
    list_articles_use_case = ListArticles(repository)
    search_articles_use_case = SearchArticles(repository)
    update_article_use_case = UpdateArticle(repository, category_repository)
    delete_article_use_case = DeleteArticle(repository)

    @router.post("", response_model=ArticleResponse, status_code=201)
    def create_article(request: ArticleCreateRequest):
        try:
            article = create_article_use_case(
                tenant_id=DEV_TENANT_ID,
                name=request.name,
                sku=request.sku,
                unit=request.unit,
                category_id=request.category_id
            )
        except ArticleAlreadyExistsError as error:
            raise HTTPException(
                status_code=409,
                detail=str(error)
            ) from error
        except CategoryNotFoundError as error:
            raise HTTPException(
                status_code=404,
                detail=str(error)
            ) from error
        except ValueError as error:
            raise HTTPException(
                status_code=422,
                detail=str(error)
            ) from error
        
        return article

    @router.get("/{article_id}", response_model=ArticleResponse)
    def get_article(article_id: UUID):
        try:
            article = get_article_use_case(
                tenant_id=DEV_TENANT_ID,
                article_id=article_id
            )
        except ArticleNotFoundError as error:
            raise HTTPException(
                status_code=404,
                detail=str(error)
            ) from error

        return article

    @router.get("", response_model=list[ArticleResponse])
    def list_articles(search: str | None = None):

        if search is None:
            return list_articles_use_case(
                tenant_id=DEV_TENANT_ID
            )

        try:
            return search_articles_use_case(
                tenant_id=DEV_TENANT_ID,
                query=search
            )

        except ValueError as error:
            raise HTTPException(
                status_code=422,
                detail=str(error)
            ) from error

    @router.put("/{article_id}", response_model=ArticleResponse)
    def update_article(
        article_id: UUID,
        request: ArticleUpdateRequest
    ):
        try:
            return update_article_use_case(
                tenant_id=DEV_TENANT_ID,
                article_id=article_id,
                name=request.name,
                sku=request.sku,
                unit=request.unit,
                category_id=request.category_id
            )
        
        except ArticleNotFoundError as error:
            raise HTTPException(
                status_code=404,
                detail=str(error)
            ) from error
        except ArticleAlreadyExistsError as error:
            raise HTTPException(
                status_code=409,
                detail=str(error)
            ) from error
        except CategoryNotFoundError as error:
            raise HTTPException(
                status_code=404,
                detail=str(error)
            ) from error
        except ValueError as error:
            raise HTTPException(
                status_code=422,
                detail=str(error)
            ) from error

    @router.delete("/{article_id}", status_code=204)
    def delete_article(article_id: UUID):
        try:
            delete_article_use_case(
                tenant_id=DEV_TENANT_ID,
                article_id=article_id
            )

        except ArticleNotFoundError as error:
            raise HTTPException(
                status_code=404,
                detail=str(error)
            ) from error
    
    return router