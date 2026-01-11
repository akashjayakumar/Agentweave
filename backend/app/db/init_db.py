from app.db.session import engine
from app.db.models import Base  # noqa: F401
from app.db import models       # ensures all models are registered


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("✅ Database tables created")
