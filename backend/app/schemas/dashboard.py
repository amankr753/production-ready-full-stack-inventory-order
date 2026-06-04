from pydantic import BaseModel


class MetricPoint(BaseModel):
    label: str
    value: float


class DashboardSummary(BaseModel):
    total_products: int
    total_customers: int
    total_orders: int
    total_revenue: float
    monthly_sales: list[MetricPoint]
    low_stock_products: int
    recent_orders: list[dict]
    top_selling_products: list[MetricPoint]
    inventory_status: list[MetricPoint]
