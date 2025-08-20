from fastapi import FastAPI

from app.api.router import api_router
from app.database.session import Base, engine
from app.core.startup import seed_if_empty


def create_db_and_tables() -> None:
    Base.metadata.create_all(bind=engine)


app = FastAPI(title="HRM-BE")
app.include_router(api_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    seed_if_empty()


@app.get("/")
def root():
    return {"message": "HRM-BE API is running 🚀"}
