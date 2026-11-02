from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ArticleCreateRequest(BaseModel):
    name: str
    sku: str
    unit: str
    category_id: UUID | None = None

class ArticleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    name: str
    sku: str
    unit: str
    category_id: UUID | None = None

class ArticleUpdateRequest(BaseModel):
    name: str
    sku: str
    unit: str
    category_id: UUID | None = None

class CategoryCreateRequest(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    name: str

class CategoryUpdateRequest(BaseModel):
    name: str