import uvicorn

from src.app import create_app
from src.app.configs.config import settings

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.RELOAD)
