from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.security import get_current_user, require_roles
from app.database.session import get_db
from app.modules.attendance.models import Attendance


class AttendanceCreate(BaseModel):
    status: str = "present"  # present, absent, wfh, leave
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None


router = APIRouter()


@router.post("/checkin")
def check_in(payload: AttendanceCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    record = Attendance(employee_id=user.id, status=payload.status, check_in=payload.check_in or datetime.utcnow())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.post("/checkout")
def check_out(payload: AttendanceCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    record = (
        db.query(Attendance)
        .filter(Attendance.employee_id == user.id)
        .order_by(Attendance.id.desc())
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="No check-in record found")
    record.check_out = payload.check_out or datetime.utcnow()
    db.commit()
    db.refresh(record)
    return record


@router.get("/me")
def my_attendance(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Attendance).where(Attendance.employee_id == user.id).all()


@router.get("/user/{user_id}", dependencies=[Depends(require_roles("admin", "manager"))])
def attendance_for_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(Attendance).where(Attendance.employee_id == user_id).all()


