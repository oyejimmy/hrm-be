from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.session import Base


class Perk(Base):
    __tablename__ = "perks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)


class EmployeePerk(Base):
    __tablename__ = "employee_perks"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    perk_id = Column(Integer, ForeignKey("perks.id"), nullable=False)
    amount = Column(Float, default=0.0)
    status = Column(String(50), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

    employee = relationship("app.modules.user.models.User")
    perk = relationship("Perk")


