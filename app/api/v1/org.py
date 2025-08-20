from fastapi import APIRouter, Depends
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.security import require_roles
from app.database.session import get_db
from app.modules.org.models import Project, Team


class TeamCreate(BaseModel):
    name: str
    department_id: Optional[int] = None
    lead_id: Optional[int] = None
    description: Optional[str] = None


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    team_id: Optional[int] = None


router = APIRouter()


@router.post("/teams", dependencies=[Depends(require_roles("admin", "manager"))])
def create_team(payload: TeamCreate, db: Session = Depends(get_db)):
    t = Team(**payload.dict())
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


@router.get("/teams")
def list_teams(db: Session = Depends(get_db)):
    return db.query(Team).all()


@router.post("/projects", dependencies=[Depends(require_roles("admin", "manager"))])
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    p = Project(**payload.dict())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


@router.get("/projects")
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()


