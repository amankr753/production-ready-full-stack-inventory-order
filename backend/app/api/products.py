from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Query, Request, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_admin
from app.db.session import get_db
from app.schemas.common import Message
from app.schemas.product import ProductCreate, ProductPage, ProductRead, ProductUpdate
from app.services.product_service import create_product, delete_product, get_product_or_404, list_products, update_product

router = APIRouter(prefix="/products", tags=["Products"], dependencies=[Depends(get_current_user)])


@router.post("", response_model=ProductRead, status_code=201)
def create(payload: ProductCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    return create_product(db, payload)


@router.get("", response_model=ProductPage[ProductRead])
def all_products(
    search: str | None = None,
    category: str | None = None,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    sort: str = "-created_at",
    db: Session = Depends(get_db),
):
    items, meta = list_products(db, search, category, page, size, sort)
    return {"items": items, "meta": meta}


@router.get("/{product_id}", response_model=ProductRead)
def detail(product_id: int, db: Session = Depends(get_db)):
    return get_product_or_404(db, product_id)


@router.put("/{product_id}", response_model=ProductRead)
def update(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db), _=Depends(require_admin)):
    return update_product(db, product_id, payload)


@router.post("/{product_id}/image", response_model=ProductRead)
async def upload_image(product_id: int, request: Request, image: UploadFile = File(...), db: Session = Depends(get_db), _=Depends(require_admin)):
    product = get_product_or_404(db, product_id)
    suffix = Path(image.filename or "").suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".webp"}:
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail="Only JPG, PNG, and WEBP images are supported")
    upload_dir = Path(__file__).resolve().parents[1] / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid4().hex}{suffix}"
    destination = upload_dir / filename
    destination.write_bytes(await image.read())
    product.product_image = str(request.base_url).rstrip("/") + f"/uploads/{filename}"
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", response_model=Message)
def remove(product_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    delete_product(db, product_id)
    return {"message": "Product deleted"}
