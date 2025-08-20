from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.security import require_roles
from app.database.session import get_db
from app.modules.recruitment.models import Application, Interview, Job


class JobCreate(BaseModel):
    title: str
    department_id: Optional[int] = None
    description: Optional[str] = None
    location: Optional[str] = None


class ApplicationCreate(BaseModel):
    job_id: int
    candidate_name: str
    candidate_email: str
    resume_path: Optional[str] = None


class InterviewCreate(BaseModel):
    application_id: int
    scheduled_at: datetime
    interviewer_id: int
    mode: str = "online"


router = APIRouter()


@router.post("/jobs", dependencies=[Depends(require_roles("admin", "manager"))])
def create_job(payload: JobCreate, db: Session = Depends(get_db)):
    job = Job(**payload.dict())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get("/jobs")
def list_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()


@router.post("/applications")
def apply(payload: ApplicationCreate, db: Session = Depends(get_db)):
    application = Application(**payload.dict())
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.post("/interviews", dependencies=[Depends(require_roles("admin", "manager"))])
def schedule_interview(payload: InterviewCreate, db: Session = Depends(get_db)):
    if not db.get(Application, payload.application_id):
        raise HTTPException(status_code=404, detail="Application not found")
    interview = Interview(**payload.dict())
    db.add(interview)
    db.commit()
    db.refresh(interview)
    return interview


