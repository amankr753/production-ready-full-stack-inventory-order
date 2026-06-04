import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.customer import Customer
from app.models.product import Product
from app.models.user import User, UserRole


def main():
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.email == "admin@example.com").first():
            db.add(User(full_name="Admin User", email="admin@example.com", hashed_password=get_password_hash("Password123"), role=UserRole.admin))
        if not db.query(Customer).filter(Customer.email == "buyer@example.com").first():
            db.add(Customer(full_name="Retail Buyer", email="buyer@example.com", phone_number="+1 555 0100", city="Austin", country="USA", customer_type="retail"))
        if not db.query(Product).filter(Product.sku_code == "SCAN-001").first():
            db.add(Product(product_name="Wireless Barcode Scanner", sku_code="SCAN-001", description="Warehouse-ready handheld scanner.", category="Hardware", brand="Acme", purchase_price=45, selling_price=89, quantity_in_stock=18, reorder_level=5))
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    main()
