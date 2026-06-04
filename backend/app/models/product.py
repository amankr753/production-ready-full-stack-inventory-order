from datetime import datetime, timezone

from sqlalchemy import DateTime, Index, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        Index("ix_products_category_name", "category", "product_name"),
        Index("ix_products_low_stock", "quantity_in_stock", "reorder_level"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_name: Mapped[str] = mapped_column(String(160), index=True)
    sku_code: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(100), index=True)
    brand: Mapped[str | None] = mapped_column(String(100), nullable=True)
    purchase_price: Mapped[float] = mapped_column(Numeric(12, 2))
    selling_price: Mapped[float] = mapped_column(Numeric(12, 2))
    quantity_in_stock: Mapped[int] = mapped_column(default=0)
    reorder_level: Mapped[int] = mapped_column(default=5)
    product_image: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    order_items = relationship("OrderItem", back_populates="product")
    inventory_logs = relationship("InventoryLog", back_populates="product", cascade="all, delete-orphan")

    @property
    def stock_status(self) -> str:
        if self.quantity_in_stock <= 0:
            return "out_of_stock"
        if self.quantity_in_stock <= self.reorder_level:
            return "low_stock"
        return "in_stock"
