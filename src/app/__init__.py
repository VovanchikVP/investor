from fastapi import FastAPI

from src.app.extensions import configure_extensions


def create_app():
    """Aplication factory"""

    app = FastAPI()
    configure_extensions(app)

    return app
