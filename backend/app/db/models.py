from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.db.session import Base
import uuid


def uuid_str():
    return str(uuid.uuid4())


class Notebook(Base):
    __tablename__ = "notebooks"

    id = Column(String, primary_key=True, default=uuid_str)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
