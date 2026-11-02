"""Web layer: the FastAPI delivery mechanism.

It receives the injected use cases, exposes them as HTTP routes, and
translates domain errors into HTTP status codes. This is the only place that
imports FastAPI.
"""
from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.domain.errors import CategoryNotFoundError, CategoryAlreadyExistsError, CategoryInUseError
from app.application.usecases.category import (
    GetCategory, 
    CreateCategory,
    ListCategories,
    SearchCategories,
    UpdateCategory,
    DeleteCategory
)
from app.domain.ports import CategoryRepository, ArticleRepository
from app.presentation.schemas import (
    CategoryCreateRequest, 
    CategoryResponse,
    CategoryUpdateRequest,
)

# TEMPORARY
DEV_TENANT_ID = UUID("11111111-1111-4111-8111-111111111111")

def create_router(
    repository: CategoryRepository, 
    article_repository: ArticleRepository
) -> APIRouter:
    
    router = APIRouter(prefix="/categories", tags=["Categories"])

    # usecases
    create_category_use_case = CreateCategory(repository)
    get_category_use_case = GetCategory(repository)
    list_categories_use_case = ListCategories(repository)
    search_categories_use_case = SearchCategories(repository)
    update_category_use_case = UpdateCategory(repository)
    delete_category_use_case = DeleteCategory(repository, article_repository)

    @router.post("", response_model=CategoryResponse, status_code=201)
    def create_category(request: CategoryCreateRequest):
        try:
            category = create_category_use_case(
                tenant_id=DEV_TENANT_ID,
                name=request.name,
            )
        except CategoryAlreadyExistsError as error:
            raise HTTPException(
                status_code=409,
                detail=str(error)
            ) from error
        except ValueError as error:
            raise HTTPException(
                status_code=422,
                detail=str(error)
            ) from error
        
        return category

    @router.get("/{category_id}", response_model=CategoryResponse)
    def get_category(category_id: UUID):
        try:
            category = get_category_use_case(
                tenant_id=DEV_TENANT_ID,
                category_id=category_id
            )
        except CategoryNotFoundError as error:
            raise HTTPException(
                status_code=404,
                detail=str(error)
            ) from error

        return category

    @router.get("", response_model=list[CategoryResponse])
    def list_categories(search: str | None = None):

        if search is None:
            return list_categories_use_case(
                tenant_id=DEV_TENANT_ID
            )

        try:
            return search_categories_use_case(
                tenant_id=DEV_TENANT_ID,
                query=search
            )

        except ValueError as error:
            raise HTTPException(
                status_code=422,
                detail=str(error)
            ) from error

    @router.put("/{category_id}", response_model=CategoryResponse)
    def update_category(
        category_id: UUID,
        request: CategoryUpdateRequest
    ):
        try:
            return update_category_use_case(
                tenant_id=DEV_TENANT_ID,
                category_id=category_id,
                name=request.name
            )
        
        except CategoryNotFoundError as error:
            raise HTTPException(
                status_code=404,
                detail=str(error)
            ) from error
        
        except CategoryAlreadyExistsError as error:
            raise HTTPException(
                status_code=409,
                detail=str(error)
            ) from error

        except ValueError as error:
            raise HTTPException(
                status_code=422,
                detail=str(error)
            ) from error

    @router.delete("/{category_id}", status_code=204)
    def delete_category(category_id: UUID):
        try:
            delete_category_use_case(
                tenant_id=DEV_TENANT_ID,
                category_id=category_id
            )

        except CategoryNotFoundError as error:
            raise HTTPException(
                status_code=404,
                detail=str(error)
            ) from error
        except CategoryInUseError as error:
            raise HTTPException(
                status_code=409,
                detail=str(error)
            ) from error
        
    return router