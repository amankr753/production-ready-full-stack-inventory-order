from datetime import datetime

from pydantic import BaseModel, Field

from app.models.order import OrderStatus, PaymentStatus
from app.schemas.common import PageMeta
from app.schemas.customer import CustomerRead
from app.schemas.product import ProductRead


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    customer_id: int
    payment_status: PaymentStatus = PaymentStatus.unpaid
    payment_method: str | None = Field(default=None, max_length=50)
    tax_amount: float = Field(default=0, ge=0)
    discount: float = Field(default=0, ge=0)
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderStatusUpdate(BaseModel):
    order_status: OrderStatus
    payment_status: PaymentStatus | None = None


class OrderItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float
    total_price: float
    product: ProductRead | None = None

    model_config = {"from_attributes": True}


class OrderRead(BaseModel):
    id: int
    customer_id: int
    order_number: str
    order_status: OrderStatus
    payment_status: PaymentStatus
    payment_method: str | None
    subtotal: float
    tax_amount: float
    discount: float
    total_amount: float
    created_at: datetime
    customer: CustomerRead | None = None
    items: list[OrderItemRead]

    model_config = {"from_attributes": True}


class OrderPage(BaseModel):
    items: list[OrderRead]
    meta: PageMeta
