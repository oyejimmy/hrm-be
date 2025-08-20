from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session

from app.auth.security import get_password_hash
from app.modules.attendance.models import Attendance
from app.modules.communication.models import Announcement, Event
from app.modules.leave.models import LeaveRequest
from app.modules.payroll.models import Payroll
from app.modules.performance.models import PerformanceReview
from app.modules.recruitment.models import Application, Interview, Job
from app.modules.org.models import Team, Project
from app.modules.training.models import Course, Enrollment
from app.modules.user.models import Department, User


def seed(db: Session) -> None:
    # Departments
    eng = Department(name="Engineering", description="Builds and maintains products")
    hr = Department(name="HR", description="People operations")
    db.add_all([eng, hr])
    db.commit()
    db.refresh(eng)
    db.refresh(hr)

    # Users
    admin = User(email="admin@example.com", full_name="Admin User", password_hash=get_password_hash("admin123"), role="admin", department_id=hr.id)
    manager = User(email="lead@example.com", full_name="Team Lead", password_hash=get_password_hash("lead123"), role="manager", department_id=eng.id)
    employee = User(email="emp@example.com", full_name="Employee One", password_hash=get_password_hash("emp123"), role="employee", department_id=eng.id)
    db.add_all([admin, manager, employee])
    db.commit()
    db.refresh(admin)
    db.refresh(manager)
    db.refresh(employee)

    # Attendance
    db.add_all([
        Attendance(employee_id=employee.id, check_in=datetime.utcnow() - timedelta(hours=9), check_out=datetime.utcnow(), status="present"),
        Attendance(employee_id=employee.id, check_in=datetime.utcnow() - timedelta(days=1, hours=9), check_out=datetime.utcnow() - timedelta(days=1), status="wfh"),
    ])

    # Leave
    db.add(
        LeaveRequest(employee_id=employee.id, leave_type="annual", start_date=datetime.utcnow() + timedelta(days=7), end_date=datetime.utcnow() + timedelta(days=10), reason="Vacation")
    )

    # Payroll
    db.add(
        Payroll(
            employee_id=employee.id,
            pay_period_start=date.today().replace(day=1),
            pay_period_end=date.today(),
            base_salary=2000,
            bonus=200,
            deductions=50,
            net_pay=2150,
        )
    )

    # Recruitment
    job = Job(title="Backend Engineer", department_id=eng.id, description="Build APIs", location="Remote")
    db.add(job)
    db.commit()
    db.refresh(job)
    app = Application(job_id=job.id, candidate_name="Jane Doe", candidate_email="jane@example.com")
    db.add(app)
    db.commit()
    db.refresh(app)
    db.add(Interview(application_id=app.id, scheduled_at=datetime.utcnow() + timedelta(days=2), interviewer_id=manager.id, mode="online"))

    # Performance
    db.add(PerformanceReview(employee_id=employee.id, reviewer_id=manager.id, period="monthly", kpi_score=85, comments="Good work"))

    # Training
    course = Course(title="Backend Engineering (Python)", description="Foundations and APIs", track="Backend Engineering")
    db.add(course)
    db.commit()
    db.refresh(course)
    db.add(Enrollment(course_id=course.id, employee_id=employee.id, progress=10, completed=0))

    # Communication
    db.add_all([
        Announcement(title="Public Holiday", content="Office closed next Friday.", created_by=admin.id),
        Event(title="Town Hall", description="Quarterly updates", start_at=datetime.utcnow() + timedelta(days=3), end_at=datetime.utcnow() + timedelta(days=3, hours=2), created_by=admin.id),
    ])

    # Org (Teams & Projects)
    team = Team(name="Platform Team", department_id=eng.id, lead_id=manager.id, description="Core backend services")
    db.add(team)
    db.commit()
    db.refresh(team)
    db.add(Project(name="HRMS Backend", description="FastAPI service", team_id=team.id, status="active"))

    db.commit()


