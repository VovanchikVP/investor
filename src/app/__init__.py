from fastapi import FastAPI

from src.app.extensions import configure_extensions
from src.app.tasks.tasks import site


def create_app():
    """Aplication factory"""

    app = FastAPI()
    configure_extensions(app)
    site.mount_app(app)

    return app
