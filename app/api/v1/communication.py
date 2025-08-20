from fastapi import APIRouter, Depends
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.security import require_roles
from app.database.session import get_db
from app.modules.communication.models import Announcement, Event


class AnnouncementCreate(BaseModel):
    title: str
    content: str
    created_by: int


class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_at: datetime
    end_at: datetime
    created_by: int


router = APIRouter()


@router.post("/announcements", dependencies=[Depends(require_roles("admin", "manager"))])
def create_announcement(payload: AnnouncementCreate, db: Session = Depends(get_db)):
    ann = Announcement(**payload.dict())
    db.add(ann)
    db.commit()
    db.refresh(ann)
    return ann


@router.get("/announcements")
def list_announcements(db: Session = Depends(get_db)):
    return db.query(Announcement).all()


@router.post("/events", dependencies=[Depends(require_roles("admin", "manager"))])
def create_event(payload: EventCreate, db: Session = Depends(get_db)):
    evt = Event(**payload.dict())
    db.add(evt)
    db.commit()
    db.refresh(evt)
    return evt


@router.get("/events")
def list_events(db: Session = Depends(get_db)):
    return db.query(Event).all()


