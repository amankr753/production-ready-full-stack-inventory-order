from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.services.pagination import paginate


def ensure_unique_email(db: Session, email: str, customer_id: int | None = None) -> None:
    query = db.query(Customer).filter(Customer.email == email.lower())
    if customer_id:
        query = query.filter(Customer.id != customer_id)
    if query.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Customer email already exists")


def create_customer(db: Session, payload: CustomerCreate) -> Customer:
    ensure_unique_email(db, str(payload.email))
    data = payload.model_dump()
    data["email"] = str(payload.email).lower()
    customer = Customer(**data)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def list_customers(db: Session, search: str | None, page: int, size: int):
    query = db.query(Customer).order_by(Customer.created_at.desc())
    if search:
        term = f"%{search}%"
        query = query.filter(or_(Customer.full_name.ilike(term), Customer.email.ilike(term), Customer.phone_number.ilike(term)))
    return paginate(query, page, size)


def get_customer_or_404(db: Session, customer_id: int) -> Customer:
    customer = db.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer


def update_customer(db: Session, customer_id: int, payload: CustomerUpdate) -> Customer:
    customer = get_customer_or_404(db, customer_id)
    data = payload.model_dump(exclude_unset=True)
    if "email" in data and data["email"]:
        ensure_unique_email(db, str(data["email"]), customer_id)
        data["email"] = str(data["email"]).lower()
    for key, value in data.items():
        setattr(customer, key, value)
    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer_id: int) -> None:
    customer = get_customer_or_404(db, customer_id)
    db.delete(customer)
    db.commit()
