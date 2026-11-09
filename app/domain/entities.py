from dataclasses import dataclass, replace
from datetime import datetime, timezone
from uuid import UUID

@dataclass()
class Article:
    id: UUID
    tenant_id: UUID
    name: str
    sku: str
    unit: str
    category_id: UUID | None = None
    deleted_at: datetime | None = None

    def __post_init__(self):
        self.name = self.name.strip()
        if not self.name:
            raise ValueError("Article name cannot be left blank.")

        if not self.sku.strip():
            raise ValueError("Article code cannot be left blank.")

        if not self.unit.strip():
            raise ValueError("The unit of measurement cannot be empty.")

    def with_updated_details(
        self,
        name: str,
        sku: str,
        unit: str,
        category_id: UUID | None
    ) -> "Article":
        
        return replace(
            self,
            name=name,
            sku=sku,
            unit=unit,
            category_id=category_id
        )

    def mark_deleted(self) -> "Article":
        return replace(
            self,
            deleted_at=datetime.now(timezone.utc)
        )

@dataclass()
class Category:
    id: UUID
    tenant_id: UUID
    name: str
    deleted_at: datetime | None = None

    def __post_init__(self):
        self.name = self.name.strip()

        if not self.name:
            raise ValueError("Category name cannot be left blank.")

    def with_updated_details(self, name: str) -> "Category":
        return replace(self, name=name)

    def mark_deleted(self) -> "Category":
        return replace(
            self,
            deleted_at=datetime.now(timezone.utc)
        )