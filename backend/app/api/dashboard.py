from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.schemas.dashboard import DashboardSummary
from app.services.dashboard_service import dashboard_summary

router = APIRouter(prefix="/dashboard", tags=["Dashboard"], dependencies=[Depends(get_current_user)])


@router.get("/summary", response_model=DashboardSummary)
def summary(db: Session = Depends(get_db)):
    return dashboard_summary(db)
