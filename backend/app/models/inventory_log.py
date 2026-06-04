from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class InventoryAction(str, Enum):
    stock_in = "stock_in"
    stock_out = "stock_out"
    order_created = "order_created"
    order_cancelled = "order_cancelled"
    adjustment = "adjustment"


class InventoryLog(Base):
    __tablename__ = "inventory_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), index=True)
    action: Mapped[InventoryAction] = mapped_column(SqlEnum(InventoryAction), index=True)
    quantity_change: Mapped[int]
    previous_quantity: Mapped[int]
    new_quantity: Mapped[int]
    reference: Mapped[str | None] = mapped_column(String(120), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    product = relationship("Product", back_populates="inventory_logs")
