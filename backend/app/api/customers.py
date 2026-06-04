from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.customer import Customer
from app.schemas.common import Message
from app.schemas.customer import CustomerCreate, CustomerPage, CustomerRead, CustomerUpdate
from app.schemas.order import OrderRead
from app.services.customer_service import create_customer, delete_customer, get_customer_or_404, list_customers, update_customer

router = APIRouter(prefix="/customers", tags=["Customers"], dependencies=[Depends(get_current_user)])


@router.post("", response_model=CustomerRead, status_code=201)
def create(payload: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(db, payload)


@router.get("", response_model=CustomerPage)
def all_customers(search: str | None = None, page: int = Query(default=1, ge=1), size: int = Query(default=20, ge=1, le=100), db: Session = Depends(get_db)):
    items, meta = list_customers(db, search, page, size)
    return {"items": items, "meta": meta}


@router.get("/{customer_id}", response_model=CustomerRead)
def detail(customer_id: int, db: Session = Depends(get_db)):
    return get_customer_or_404(db, customer_id)


@router.get("/{customer_id}/orders", response_model=list[OrderRead])
def order_history(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).options(joinedload(Customer.orders)).filter(Customer.id == customer_id).first()
    if not customer:
        return []
    return customer.orders


@router.put("/{customer_id}", response_model=CustomerRead)
def update(customer_id: int, payload: CustomerUpdate, db: Session = Depends(get_db)):
    return update_customer(db, customer_id, payload)


@router.delete("/{customer_id}", response_model=Message)
def remove(customer_id: int, db: Session = Depends(get_db)):
    delete_customer(db, customer_id)
    return {"message": "Customer deleted"}
