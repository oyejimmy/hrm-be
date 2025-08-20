from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.auth.security import get_current_user, require_roles
from app.database.session import get_db
from app.modules.attendance.models import Attendance
from app.modules.leave.models import LeaveRequest
from app.modules.payroll.models import Payroll
from app.modules.recruitment.models import Job
from app.modules.user.models import Department, User


router = APIRouter()


@router.get("/employee")
def employee_dashboard(db: Session = Depends(get_db), user=Depends(get_current_user)):
    leaves_pending = db.query(LeaveRequest).filter(LeaveRequest.employee_id == user.id, LeaveRequest.status == "pending").count()
    upcoming_payroll = (
        db.query(Payroll)
        .filter(Payroll.employee_id == user.id)
        .order_by(Payroll.pay_period_end.desc())
        .first()
    )
    today_status = (
        db.query(Attendance)
        .filter(Attendance.employee_id == user.id)
        .order_by(Attendance.id.desc())
        .first()
    )
    announcements_count = 0  # Can be expanded by joining announcements
    return {
        "user": {"id": user.id, "name": user.full_name, "role": user.role},
        "pending_leaves": leaves_pending,
        "latest_payroll": upcoming_payroll.net_pay if upcoming_payroll else None,
        "today_status": today_status.status if today_status else None,
        "announcements": announcements_count,
    }


@router.get("/admin", dependencies=[Depends(require_roles("admin"))])
def admin_dashboard(db: Session = Depends(get_db)):
    total_employees = db.query(User).count()
    total_departments = db.query(Department).count()
    open_jobs = db.query(Job).filter(Job.status == "open").count()
    total_payroll_this_month = (
        db.query(func.sum(Payroll.net_pay)).filter(Payroll.pay_period_end >= date.today().replace(day=1)).scalar()
        or 0
    )
    pending_leaves = db.query(LeaveRequest).filter(LeaveRequest.status == "pending").count()
    return {
        "employees": total_employees,
        "departments": total_departments,
        "open_jobs": open_jobs,
        "payroll_this_month": total_payroll_this_month,
        "pending_leaves": pending_leaves,
    }


