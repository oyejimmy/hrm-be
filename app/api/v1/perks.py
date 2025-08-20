from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.security import require_roles
from app.database.session import get_db
from app.modules.perks.models import EmployeePerk, Perk


class PerkCreate(BaseModel):
    name: str
    description: str | None = None


class EmployeePerkCreate(BaseModel):
    employee_id: int
    perk_id: int
    amount: float = 0


router = APIRouter()


@router.post("/", dependencies=[Depends(require_roles("admin", "manager"))])
def create_perk(payload: PerkCreate, db: Session = Depends(get_db)):
    p = Perk(**payload.dict())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


@router.get("/")
def list_perks(db: Session = Depends(get_db)):
    return db.query(Perk).all()


@router.post("/assign", dependencies=[Depends(require_roles("admin", "manager"))])
def assign_perk(payload: EmployeePerkCreate, db: Session = Depends(get_db)):
    ep = EmployeePerk(**payload.dict())
    db.add(ep)
    db.commit()
    db.refresh(ep)
    return ep


@router.get("/employee/{employee_id}")
def perks_for_employee(employee_id: int, db: Session = Depends(get_db)):
    return db.query(EmployeePerk).filter(EmployeePerk.employee_id == employee_id).all()


