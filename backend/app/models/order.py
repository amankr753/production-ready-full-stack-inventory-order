from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class OrderStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    cancelled = "cancelled"


class PaymentStatus(str, Enum):
    unpaid = "unpaid"
    paid = "paid"
    refunded = "refunded"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id", ondelete="RESTRICT"), index=True)
    order_number: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    order_status: Mapped[OrderStatus] = mapped_column(SqlEnum(OrderStatus), default=OrderStatus.pending, index=True)
    payment_status: Mapped[PaymentStatus] = mapped_column(SqlEnum(PaymentStatus), default=PaymentStatus.unpaid, index=True)
    payment_method: Mapped[str | None] = mapped_column(String(50), nullable=True)
    subtotal: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    tax_amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    discount: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    total_amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="RESTRICT"), index=True)
    quantity: Mapped[int]
    price: Mapped[float] = mapped_column(Numeric(12, 2))
    total_price: Mapped[float] = mapped_column(Numeric(12, 2))

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
