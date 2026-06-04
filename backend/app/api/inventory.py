from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.inventory_log import InventoryLog
from app.models.product import Product
from app.schemas.inventory import InventoryLogPage
from app.schemas.product import ProductRead
from app.services.pagination import paginate

router = APIRouter(prefix="/inventory", tags=["Inventory"], dependencies=[Depends(get_current_user)])


@router.get("/logs", response_model=InventoryLogPage)
def logs(page: int = Query(default=1, ge=1), size: int = Query(default=20, ge=1, le=100), db: Session = Depends(get_db)):
    query = db.query(InventoryLog).options(joinedload(InventoryLog.product)).order_by(InventoryLog.created_at.desc())
    items, meta = paginate(query, page, size)
    return {"items": items, "meta": meta}


@router.get("/low-stock", response_model=list[ProductRead])
def low_stock(db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.quantity_in_stock > 0, Product.quantity_in_stock <= Product.reorder_level).all()


@router.get("/out-of-stock", response_model=list[ProductRead])
def out_of_stock(db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.quantity_in_stock <= 0).all()
