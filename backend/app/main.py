from fastapi import FastAPI
from app.api import notebook

app = FastAPI(title="AgentWeave")

app.include_router(
    notebook.router,
    prefix="/notebooks",
    tags=["Notebooks"],
)
