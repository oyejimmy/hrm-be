from datetime import datetime
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.session import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    description = Column(Text, nullable=True)
    location = Column(String(100), nullable=True)
    status = Column(String(50), default="open")  # open, closed, on_hold
    posted_at = Column(DateTime, default=datetime.utcnow)

    department = relationship("app.modules.user.models.Department")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    candidate_name = Column(String(255), nullable=False)
    candidate_email = Column(String(255), nullable=False)
    resume_path = Column(String(500), nullable=True)
    status = Column(String(50), default="received")  # received, shortlisted, interviewed, offered, rejected
    applied_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="applications")


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    interviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mode = Column(String(50), default="online")  # online, onsite, phone
    feedback = Column(Text, nullable=True)
    result = Column(String(50), nullable=True)  # pass, fail, hold

    application = relationship("Application")
    interviewer = relationship("app.modules.user.models.User")


