from fastapi import APIRouter, Depends
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.security import require_roles
from app.database.session import get_db
from app.modules.performance.models import PerformanceReview


class ReviewCreate(BaseModel):
    employee_id: int
    reviewer_id: int
    period: str
    kpi_score: int
    comments: Optional[str] = None


router = APIRouter()


@router.post("/reviews", dependencies=[Depends(require_roles("admin", "manager"))])
def create_review(payload: ReviewCreate, db: Session = Depends(get_db)):
    review = PerformanceReview(**payload.dict())
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.get("/employee/{employee_id}")
def reviews_for_employee(employee_id: int, db: Session = Depends(get_db)):
    return db.query(PerformanceReview).filter(PerformanceReview.employee_id == employee_id).all()


