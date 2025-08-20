from datetime import date
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.security import require_roles
from app.database.session import get_db
from app.modules.payroll.models import Payroll


class PayrollCreate(BaseModel):
    employee_id: int
    pay_period_start: date
    pay_period_end: date
    base_salary: float
    bonus: float = 0.0
    deductions: float = 0.0


router = APIRouter()


@router.post("/", dependencies=[Depends(require_roles("admin"))])
def create_payroll(payload: PayrollCreate, db: Session = Depends(get_db)):
    net_pay = payload.base_salary + payload.bonus - payload.deductions
    pr = Payroll(
        employee_id=payload.employee_id,
        pay_period_start=payload.pay_period_start,
        pay_period_end=payload.pay_period_end,
        base_salary=payload.base_salary,
        bonus=payload.bonus,
        deductions=payload.deductions,
        net_pay=net_pay,
    )
    db.add(pr)
    db.commit()
    db.refresh(pr)
    return pr


@router.get("/user/{user_id}", dependencies=[Depends(require_roles("admin", "manager"))])
def payrolls_for_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(Payroll).filter(Payroll.employee_id == user_id).all()


