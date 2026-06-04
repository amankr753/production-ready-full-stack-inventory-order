"""initial schema

Revision ID: 202606040001
Revises:
Create Date: 2026-06-04 00:01:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "202606040001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    user_role = sa.Enum("admin", "staff", name="userrole")
    order_status = sa.Enum("pending", "processing", "completed", "cancelled", name="orderstatus")
    payment_status = sa.Enum("unpaid", "paid", "refunded", name="paymentstatus")
    inventory_action = sa.Enum("stock_in", "stock_out", "order_created", "order_cancelled", "adjustment", name="inventoryaction")

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("full_name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_role", "users", ["role"])

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("product_name", sa.String(length=160), nullable=False),
        sa.Column("sku_code", sa.String(length=80), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("brand", sa.String(length=100), nullable=True),
        sa.Column("purchase_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("selling_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("quantity_in_stock", sa.Integer(), nullable=False),
        sa.Column("reorder_level", sa.Integer(), nullable=False),
        sa.Column("product_image", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_products_product_name", "products", ["product_name"])
    op.create_index("ix_products_sku_code", "products", ["sku_code"], unique=True)
    op.create_index("ix_products_category", "products", ["category"])
    op.create_index("ix_products_category_name", "products", ["category", "product_name"])
    op.create_index("ix_products_low_stock", "products", ["quantity_in_stock", "reorder_level"])

    op.create_table(
        "customers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("full_name", sa.String(length=160), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone_number", sa.String(length=40), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("state", sa.String(length=100), nullable=True),
        sa.Column("country", sa.String(length=100), nullable=True),
        sa.Column("postal_code", sa.String(length=30), nullable=True),
        sa.Column("customer_type", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_customers_full_name", "customers", ["full_name"])
    op.create_index("ix_customers_email", "customers", ["email"], unique=True)

    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("customer_id", sa.Integer(), sa.ForeignKey("customers.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("order_number", sa.String(length=40), nullable=False),
        sa.Column("order_status", order_status, nullable=False),
        sa.Column("payment_status", payment_status, nullable=False),
        sa.Column("payment_method", sa.String(length=50), nullable=True),
        sa.Column("subtotal", sa.Numeric(12, 2), nullable=False),
        sa.Column("tax_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("discount", sa.Numeric(12, 2), nullable=False),
        sa.Column("total_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_orders_customer_id", "orders", ["customer_id"])
    op.create_index("ix_orders_order_number", "orders", ["order_number"], unique=True)
    op.create_index("ix_orders_order_status", "orders", ["order_status"])
    op.create_index("ix_orders_payment_status", "orders", ["payment_status"])
    op.create_index("ix_orders_created_at", "orders", ["created_at"])

    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id", ondelete="CASCADE"), nullable=False),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("price", sa.Numeric(12, 2), nullable=False),
        sa.Column("total_price", sa.Numeric(12, 2), nullable=False),
    )
    op.create_index("ix_order_items_order_id", "order_items", ["order_id"])
    op.create_index("ix_order_items_product_id", "order_items", ["product_id"])

    op.create_table(
        "inventory_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id", ondelete="CASCADE"), nullable=False),
        sa.Column("action", inventory_action, nullable=False),
        sa.Column("quantity_change", sa.Integer(), nullable=False),
        sa.Column("previous_quantity", sa.Integer(), nullable=False),
        sa.Column("new_quantity", sa.Integer(), nullable=False),
        sa.Column("reference", sa.String(length=120), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_inventory_logs_product_id", "inventory_logs", ["product_id"])
    op.create_index("ix_inventory_logs_action", "inventory_logs", ["action"])
    op.create_index("ix_inventory_logs_created_at", "inventory_logs", ["created_at"])


def downgrade() -> None:
    op.drop_table("inventory_logs")
    op.drop_table("order_items")
    op.drop_table("orders")
    op.drop_table("customers")
    op.drop_table("products")
    op.drop_table("users")
    for name in ["inventoryaction", "paymentstatus", "orderstatus", "userrole"]:
        op.execute(f"DROP TYPE IF EXISTS {name}")
