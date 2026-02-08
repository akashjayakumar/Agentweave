from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.crud import create_notebook, get_notebooks
from app.schemas.notebook import NotebookCreate, NotebookResponse
from app.rag.ingest import ingest_chunks, chunk_text
from app.rag.retrieve import retrieve_chunks
from app.agents.reader import reader_agent
from app.agents.explainer import explainer_agent
from fastapi import UploadFile, File
from pypdf import PdfReader
from app.rag.ingest import ingest_chunks, chunk_text
from app.scrapers.rbi import scrape_rbi
from app.agents.change_detector import detect_changes


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

@router.get("/{notebook_id}/ask")
def ask_notebook(
    notebook_id: str,
    q: str,
):
    """
    Ask a question against a notebook.
    """
    chunks = retrieve_chunks(notebook_id, q)
    points = reader_agent(chunks)
    answer = explainer_agent(points)

    return {
        "question": q,
        "answer": answer,
        "sources": chunks,
    }

@router.post("/{notebook_id}/upload-pdf")
def upload_pdf(
    notebook_id: str,
    file: UploadFile = File(...),
):
    reader = PdfReader(file.file)


    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""


    chunks = chunk_text(text)
    ingest_chunks(notebook_id, chunks)


    return {
        "filename": file.filename,
        "chunks_ingested": len(chunks),
        }

@router.post("/{notebook_id}/scrape-rbi")
def ingest_rbi(
    notebook_id: str,
):
    pages = scrape_rbi()


    all_text = ""
    for page in pages:
        all_text += page["title"] + "\n"

    chunks = chunk_text(all_text)
    ingest_chunks(notebook_id, chunks)


    return {
        "pages_ingested": len(pages),
        "chunks_ingested": len(chunks),
    }

@router.post("/{notebook_id}/detect-changes")
def detect_notebook_changes(
    notebook_id: str,
    text: str,
):
    from app.rag.ingest import chunk_text

    new_chunks = chunk_text(text)
    changes = detect_changes(notebook_id, new_chunks)

    return {
        "total_chunks": len(new_chunks),
        "changed_chunks": len(changes),
        "changes": changes,
    }