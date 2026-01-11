from fastapi import APIRouter, UploadFile
from app.db.session import SessionLocal
from app.db.crud import create_document

router = APIRouter()
