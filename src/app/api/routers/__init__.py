from fastapi import APIRouter

from src.app.api.routers.reports import initial_data

router = APIRouter(prefix="/api/v1")

trans_router = APIRouter(prefix="/example_rout", tags=["Пример роута"])

trans_router.add_api_route("", initial_data, methods=["POST"])

router.include_router(trans_router)
