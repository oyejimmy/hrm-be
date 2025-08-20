from fastapi import APIRouter, Depends
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.security import require_roles
from app.database.session import get_db
from app.modules.training.models import Course, Enrollment


class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    track: Optional[str] = None


class EnrollmentCreate(BaseModel):
    course_id: int
    employee_id: int


router = APIRouter()


@router.post("/courses", dependencies=[Depends(require_roles("admin", "manager"))])
def create_course(payload: CourseCreate, db: Session = Depends(get_db)):
    course = Course(**payload.dict())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@router.get("/courses")
def list_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()


@router.post("/enroll", dependencies=[Depends(require_roles("admin", "manager"))])
def enroll(payload: EnrollmentCreate, db: Session = Depends(get_db)):
    enrollment = Enrollment(**payload.dict())
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


@router.get("/employee/{employee_id}")
def enrollments_for_employee(employee_id: int, db: Session = Depends(get_db)):
    return db.query(Enrollment).filter(Enrollment.employee_id == employee_id).all()


