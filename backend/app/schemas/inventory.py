from datetime import datetime

from pydantic import BaseModel

from app.models.inventory_log import InventoryAction
from app.schemas.common import PageMeta
from app.schemas.product import ProductRead


class InventoryLogRead(BaseModel):
    id: int
    product_id: int
    action: InventoryAction
    quantity_change: int
    previous_quantity: int
    new_quantity: int
    reference: str | None
    created_at: datetime
    product: ProductRead | None = None

    model_config = {"from_attributes": True}


class InventoryLogPage(BaseModel):
    items: list[InventoryLogRead]
    meta: PageMeta
