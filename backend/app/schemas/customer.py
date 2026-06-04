from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.schemas.common import PageMeta


class CustomerBase(BaseModel):
    full_name: str = Field(min_length=2, max_length=160)
    email: EmailStr
    phone_number: str | None = Field(default=None, max_length=40)
    address: str | None = None
    city: str | None = Field(default=None, max_length=100)
    state: str | None = Field(default=None, max_length=100)
    country: str | None = Field(default=None, max_length=100)
    postal_code: str | None = Field(default=None, max_length=30)
    customer_type: str = Field(default="retail", max_length=50)


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=160)
    email: EmailStr | None = None
    phone_number: str | None = Field(default=None, max_length=40)
    address: str | None = None
    city: str | None = Field(default=None, max_length=100)
    state: str | None = Field(default=None, max_length=100)
    country: str | None = Field(default=None, max_length=100)
    postal_code: str | None = Field(default=None, max_length=30)
    customer_type: str | None = Field(default=None, max_length=50)


class CustomerRead(CustomerBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class CustomerPage(BaseModel):
    items: list[CustomerRead]
    meta: PageMeta
