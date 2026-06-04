from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field, computed_field

from app.schemas.common import PageMeta

T = TypeVar("T")


class ProductBase(BaseModel):
    product_name: str = Field(min_length=2, max_length=160)
    sku_code: str = Field(min_length=2, max_length=80)
    description: str | None = None
    category: str = Field(min_length=2, max_length=100)
    brand: str | None = Field(default=None, max_length=100)
    purchase_price: float = Field(ge=0)
    selling_price: float = Field(ge=0)
    quantity_in_stock: int = Field(ge=0)
    reorder_level: int = Field(ge=0, default=5)
    product_image: str | None = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    product_name: str | None = Field(default=None, min_length=2, max_length=160)
    sku_code: str | None = Field(default=None, min_length=2, max_length=80)
    description: str | None = None
    category: str | None = Field(default=None, min_length=2, max_length=100)
    brand: str | None = Field(default=None, max_length=100)
    purchase_price: float | None = Field(default=None, ge=0)
    selling_price: float | None = Field(default=None, ge=0)
    quantity_in_stock: int | None = Field(default=None, ge=0)
    reorder_level: int | None = Field(default=None, ge=0)
    product_image: str | None = None


class ProductRead(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def stock_status(self) -> str:
        if self.quantity_in_stock <= 0:
            return "out_of_stock"
        if self.quantity_in_stock <= self.reorder_level:
            return "low_stock"
        return "in_stock"

    model_config = {"from_attributes": True}


class ProductPage(BaseModel, Generic[T]):
    items: list[T]
    meta: PageMeta
