import uvicorn

from src.app import create_app
from src.app.configs.config import settings
from src.app.tasks.tasks import scheduler

app = create_app()


@app.on_event("startup")
async def startup():
    scheduler.start()


if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, reload=settings.RELOAD)
