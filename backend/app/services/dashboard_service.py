from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.schemas.dashboard import DashboardSummary, MetricPoint
from app.services.order_service import top_selling


def dashboard_summary(db: Session) -> DashboardSummary:
    total_revenue = db.query(func.coalesce(func.sum(Order.total_amount), 0)).filter(Order.order_status != OrderStatus.cancelled).scalar()
    monthly = (
        db.query(extract("month", Order.created_at).label("month"), func.coalesce(func.sum(Order.total_amount), 0).label("revenue"))
        .filter(Order.order_status != OrderStatus.cancelled)
        .group_by("month")
        .order_by("month")
        .all()
    )
    recent = (
        db.query(Order)
        .order_by(Order.created_at.desc())
        .limit(5)
        .all()
    )
    inventory_status = [
        MetricPoint(label="In Stock", value=db.query(Product).filter(Product.quantity_in_stock > Product.reorder_level).count()),
        MetricPoint(label="Low Stock", value=db.query(Product).filter(Product.quantity_in_stock > 0, Product.quantity_in_stock <= Product.reorder_level).count()),
        MetricPoint(label="Out of Stock", value=db.query(Product).filter(Product.quantity_in_stock <= 0).count()),
    ]
    return DashboardSummary(
        total_products=db.query(Product).count(),
        total_customers=db.query(Customer).count(),
        total_orders=db.query(Order).count(),
        total_revenue=float(total_revenue or 0),
        monthly_sales=[MetricPoint(label=str(int(row.month)), value=float(row.revenue)) for row in monthly],
        low_stock_products=db.query(Product).filter(Product.quantity_in_stock <= Product.reorder_level).count(),
        recent_orders=[{"id": order.id, "order_number": order.order_number, "status": order.order_status, "total": float(order.total_amount)} for order in recent],
        top_selling_products=[MetricPoint(label=row.product_name, value=float(row.sold)) for row in top_selling(db)],
        inventory_status=inventory_status,
    )
