from fastapi import APIRouter, Depends, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.order import OrderStatus
from app.schemas.common import Message
from app.schemas.order import OrderCreate, OrderPage, OrderRead, OrderStatusUpdate
from app.services.order_service import cancel_order, create_order, get_order_or_404, list_orders, update_order_status

router = APIRouter(prefix="/orders", tags=["Orders"], dependencies=[Depends(get_current_user)])


@router.post("", response_model=OrderRead, status_code=201)
def create(payload: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db, payload)


@router.get("", response_model=OrderPage)
def all_orders(status: OrderStatus | None = None, page: int = Query(default=1, ge=1), size: int = Query(default=20, ge=1, le=100), db: Session = Depends(get_db)):
    items, meta = list_orders(db, status, page, size)
    return {"items": items, "meta": meta}


@router.get("/{order_id}", response_model=OrderRead)
def detail(order_id: int, db: Session = Depends(get_db)):
    return get_order_or_404(db, order_id)


@router.get("/{order_id}/invoice", response_class=HTMLResponse)
def invoice(order_id: int, db: Session = Depends(get_db)):
    order = get_order_or_404(db, order_id)
    rows = "".join(
        f"<tr><td>{item.product.product_name if item.product else item.product_id}</td><td>{item.quantity}</td><td>{float(item.price):.2f}</td><td>{float(item.total_price):.2f}</td></tr>"
        for item in order.items
    )
    return f"""
    <!doctype html>
    <html><head><title>Invoice {order.order_number}</title>
    <style>body{{font-family:Arial,sans-serif;margin:40px;color:#18202f}}table{{width:100%;border-collapse:collapse}}td,th{{border-bottom:1px solid #d9dee8;padding:10px;text-align:left}}.total{{text-align:right;font-size:20px;font-weight:700}}</style>
    </head><body>
    <h1>Invoice {order.order_number}</h1>
    <p>Customer: {order.customer.full_name if order.customer else order.customer_id}</p>
    <p>Status: {order.order_status.value} | Payment: {order.payment_status.value}</p>
    <table><thead><tr><th>Product</th><th>Qty</th><th>Price</th><th>Total</th></tr></thead><tbody>{rows}</tbody></table>
    <p class="total">Grand total: {float(order.total_amount):.2f}</p>
    </body></html>
    """


@router.put("/{order_id}", response_model=OrderRead)
def update(order_id: int, payload: OrderStatusUpdate, db: Session = Depends(get_db)):
    return update_order_status(db, order_id, payload)


@router.delete("/{order_id}", response_model=Message)
def remove(order_id: int, db: Session = Depends(get_db)):
    cancel_order(db, order_id)
    return {"message": "Order cancelled and deleted"}
