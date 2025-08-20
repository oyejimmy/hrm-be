from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.modules.seed import seed


def seed_if_empty():
    db: Session = SessionLocal()
    try:
        # Check if users exist
        from app.modules.user.models import User

        if db.query(User).count() == 0:
            seed(db)
    finally:
        db.close()


