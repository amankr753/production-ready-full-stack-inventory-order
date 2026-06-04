from fastapi import HTTPException, status
from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

from app.models.inventory_log import InventoryAction, InventoryLog
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def ensure_unique_sku(db: Session, sku_code: str, product_id: int | None = None) -> None:
    query = db.query(Product).filter(Product.sku_code == sku_code)
    if product_id:
        query = query.filter(Product.id != product_id)
    if query.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="SKU code already exists")


def create_product(db: Session, payload: ProductCreate) -> Product:
    ensure_unique_sku(db, payload.sku_code)
    product = Product(**payload.model_dump())
    db.add(product)
    db.flush()
    db.add(
        InventoryLog(
            product_id=product.id,
            action=InventoryAction.stock_in,
            quantity_change=product.quantity_in_stock,
            previous_quantity=0,
            new_quantity=product.quantity_in_stock,
            reference="initial_stock",
        )
    )
    db.commit()
    db.refresh(product)
    return product


def list_products(db: Session, search: str | None, category: str | None, page: int, size: int, sort: str):
    from app.services.pagination import paginate

    query = db.query(Product)
    if search:
        term = f"%{search}%"
        query = query.filter(or_(Product.product_name.ilike(term), Product.sku_code.ilike(term), Product.brand.ilike(term)))
    if category:
        query = query.filter(Product.category == category)
    direction = desc if sort.startswith("-") else asc
    sort_field = sort[1:] if sort.startswith("-") else sort
    if sort_field not in {"product_name", "selling_price", "quantity_in_stock", "created_at"}:
        sort_field = "created_at"
    return paginate(query.order_by(direction(getattr(Product, sort_field))), page, size)


def get_product_or_404(db: Session, product_id: int) -> Product:
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


def update_product(db: Session, product_id: int, payload: ProductUpdate) -> Product:
    product = get_product_or_404(db, product_id)
    data = payload.model_dump(exclude_unset=True)
    if "sku_code" in data:
        ensure_unique_sku(db, data["sku_code"], product_id)
    old_quantity = product.quantity_in_stock
    for key, value in data.items():
        setattr(product, key, value)
    if "quantity_in_stock" in data and data["quantity_in_stock"] != old_quantity:
        db.add(
            InventoryLog(
                product_id=product.id,
                action=InventoryAction.adjustment,
                quantity_change=data["quantity_in_stock"] - old_quantity,
                previous_quantity=old_quantity,
                new_quantity=data["quantity_in_stock"],
                reference="manual_update",
            )
        )
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> None:
    product = get_product_or_404(db, product_id)
    db.delete(product)
    db.commit()
