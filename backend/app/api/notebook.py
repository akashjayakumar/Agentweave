from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.crud import create_notebook, get_notebooks

router = APIRouter()


# Dependency: gives one DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create(title: str, db: Session = Depends(get_db)):
    """
    Create a new notebook.
    Source of truth: PostgreSQL notebooks table.
    """
    return create_notebook(db, title)


@router.get("/")
def list_notebooks(db: Session = Depends(get_db)):
    """
    List all notebooks.
    """
    return get_notebooks(db)
