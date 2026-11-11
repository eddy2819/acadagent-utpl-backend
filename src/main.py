from fastapi import FastAPI

from src.api.v1.router import router

app = FastAPI(
    title="AcadAgent-UTPL",
    description="Backend del sistema de homologación y validación de propuestas TIC.",
    version="0.1.0",
)

app.include_router(router, prefix="/api/v1")
