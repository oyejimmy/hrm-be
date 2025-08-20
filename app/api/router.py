from fastapi import APIRouter

from app.api.v1 import (
    auth,
    employees,
    attendance,
    leaves,
    payroll,
    recruitment,
    performance,
    training,
    communication,
    dashboard,
    org,
    perks,
)


api_router = APIRouter(prefix="/api")

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(employees.router, prefix="/employees", tags=["employees"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
api_router.include_router(leaves.router, prefix="/leaves", tags=["leaves"])
api_router.include_router(payroll.router, prefix="/payroll", tags=["payroll"])
api_router.include_router(recruitment.router, prefix="/recruitment", tags=["recruitment"])
api_router.include_router(performance.router, prefix="/performance", tags=["performance"])
api_router.include_router(training.router, prefix="/training", tags=["training"])
api_router.include_router(communication.router, prefix="/communication", tags=["communication"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(org.router, prefix="/org", tags=["org"])
api_router.include_router(perks.router, prefix="/perks", tags=["perks"])


