from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.customer import Customer
from app.models.inventory_log import InventoryAction, InventoryLog
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderStatusUpdate
from app.services.pagination import paginate


def _order_number() -> str:
    return f"ORD-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"


def create_order(db: Session, payload: OrderCreate) -> Order:
    if not db.get(Customer, payload.customer_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    product_ids = [item.product_id for item in payload.items]
    if len(product_ids) != len(set(product_ids)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate products in order")
    products = {product.id: product for product in db.query(Product).filter(Product.id.in_(product_ids)).with_for_update().all()}
    if len(products) != len(product_ids):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One or more products were not found")

    subtotal = 0.0
    order = Order(
        customer_id=payload.customer_id,
        order_number=_order_number(),
        payment_status=payload.payment_status,
        payment_method=payload.payment_method,
        tax_amount=payload.tax_amount,
        discount=payload.discount,
    )
    db.add(order)
    db.flush()

    for item in payload.items:
        product = products[item.product_id]
        if product.quantity_in_stock < item.quantity:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Insufficient stock for {product.product_name}")
        previous = product.quantity_in_stock
        product.quantity_in_stock -= item.quantity
        line_total = float(product.selling_price) * item.quantity
        subtotal += line_total
        db.add(OrderItem(order_id=order.id, product_id=product.id, quantity=item.quantity, price=float(product.selling_price), total_price=line_total))
        db.add(
            InventoryLog(
                product_id=product.id,
                action=InventoryAction.order_created,
                quantity_change=-item.quantity,
                previous_quantity=previous,
                new_quantity=product.quantity_in_stock,
                reference=order.order_number,
            )
        )

    order.subtotal = subtotal
    order.total_amount = max(subtotal + payload.tax_amount - payload.discount, 0)
    db.commit()
    return get_order_or_404(db, order.id)


def list_orders(db: Session, status_filter: OrderStatus | None, page: int, size: int):
    query = db.query(Order).options(joinedload(Order.customer), joinedload(Order.items).joinedload(OrderItem.product)).order_by(Order.created_at.desc())
    if status_filter:
        query = query.filter(Order.order_status == status_filter)
    return paginate(query, page, size)


def get_order_or_404(db: Session, order_id: int) -> Order:
    order = db.query(Order).options(joinedload(Order.customer), joinedload(Order.items).joinedload(OrderItem.product)).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


def update_order_status(db: Session, order_id: int, payload: OrderStatusUpdate) -> Order:
    order = get_order_or_404(db, order_id)
    if order.order_status == OrderStatus.cancelled and payload.order_status != OrderStatus.cancelled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cancelled orders cannot be reopened")
    if payload.order_status == OrderStatus.cancelled and order.order_status != OrderStatus.cancelled:
        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).with_for_update().one()
            previous = product.quantity_in_stock
            product.quantity_in_stock += item.quantity
            db.add(
                InventoryLog(
                    product_id=product.id,
                    action=InventoryAction.order_cancelled,
                    quantity_change=item.quantity,
                    previous_quantity=previous,
                    new_quantity=product.quantity_in_stock,
                    reference=order.order_number,
                )
            )
    order.order_status = payload.order_status
    if payload.payment_status:
        order.payment_status = payload.payment_status
    db.commit()
    return get_order_or_404(db, order.id)


def cancel_order(db: Session, order_id: int) -> None:
    order = update_order_status(db, order_id, OrderStatusUpdate(order_status=OrderStatus.cancelled))
    db.delete(order)
    db.commit()


def top_selling(db: Session, limit: int = 5):
    return (
        db.query(Product.product_name, func.sum(OrderItem.quantity).label("sold"))
        .join(OrderItem, Product.id == OrderItem.product_id)
        .join(Order, Order.id == OrderItem.order_id)
        .filter(Order.order_status != OrderStatus.cancelled)
        .group_by(Product.product_name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(limit)
        .all()
    )
