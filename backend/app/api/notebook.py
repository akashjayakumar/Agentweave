from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.crud import create_notebook, get_notebooks
from app.schemas.notebook import NotebookCreate, NotebookResponse
from app.rag.ingest import ingest_chunks, chunk_text
from app.rag.retrieve import retrieve_chunks


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=NotebookResponse,
)
def create(
    payload: NotebookCreate,
    db: Session = Depends(get_db),
):
    return create_notebook(db, payload.title)


@router.get(
    "/",
    response_model=list[NotebookResponse],
)
def list_notebooks(db: Session = Depends(get_db)):
    return get_notebooks(db)


@router.post("/{notebook_id}/ingest")
def ingest_text(
    notebook_id: str,
    text: str,
):
    chunks = chunk_text(text)
    ingest_chunks(notebook_id, chunks)
    return {"chunks_ingested": len(chunks)}


@router.get("/{notebook_id}/search")
def search(
    notebook_id: str,
    q: str,
):
    return retrieve_chunks(notebook_id, q)