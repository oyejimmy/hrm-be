from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.security import get_current_user, require_roles
from app.database.session import get_db
from app.modules.leave.models import LeaveRequest


class LeaveCreate(BaseModel):
    leave_type: str
    start_date: datetime
    end_date: datetime
    reason: Optional[str] = None


router = APIRouter()


@router.post("/")
def create_leave(payload: LeaveCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    leave = LeaveRequest(
        employee_id=user.id,
        leave_type=payload.leave_type,
        start_date=payload.start_date,
        end_date=payload.end_date,
        reason=payload.reason,
    )
    db.add(leave)
    db.commit()
    db.refresh(leave)
    return leave


@router.get("/me")
def my_leaves(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(LeaveRequest).filter(LeaveRequest.employee_id == user.id).all()


@router.post("/{leave_id}/approve", dependencies=[Depends(require_roles("admin", "manager"))])
def approve(leave_id: int, db: Session = Depends(get_db), reviewer=Depends(get_current_user)):
    leave = db.get(LeaveRequest, leave_id)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    leave.status = "approved"
    leave.reviewed_by = reviewer.id
    leave.reviewed_at = datetime.utcnow()
    db.commit()
    db.refresh(leave)
    return leave


@router.post("/{leave_id}/reject", dependencies=[Depends(require_roles("admin", "manager"))])
def reject(leave_id: int, db: Session = Depends(get_db), reviewer=Depends(get_current_user)):
    leave = db.get(LeaveRequest, leave_id)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    leave.status = "rejected"
    leave.reviewed_by = reviewer.id
    leave.reviewed_at = datetime.utcnow()
    db.commit()
    db.refresh(leave)
    return leave


