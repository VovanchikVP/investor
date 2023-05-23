from fastapi import FastAPI

from src.app.api.routers import router


def configure_extensions(app: FastAPI):
    """Configure extensions"""
    app.include_router(router)
