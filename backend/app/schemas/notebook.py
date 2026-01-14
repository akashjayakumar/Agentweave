from pydantic import BaseModel
from datetime import datetime


class NotebookCreate(BaseModel):
    title: str


class NotebookResponse(BaseModel):
    id: str
    title: str
    created_at: datetime

    class Config:
        from_attributes = True
