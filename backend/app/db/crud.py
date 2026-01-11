from sqlalchemy.orm import Session
from app.db import models


def create_notebook(db: Session, title: str):
    notebook = models.Notebook(title=title)
    db.add(notebook)
    db.commit()
    db.refresh(notebook)
    return notebook


def get_notebooks(db: Session):
    return db.query(models.Notebook).all()
