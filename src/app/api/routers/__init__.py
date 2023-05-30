from fastapi import APIRouter

from src.app.api.routers.reports import (
    add_investment_account,
    add_reports_broker,
    initial_data,
)

router = APIRouter(prefix="/api/v1")

trans_router = APIRouter(prefix="/example_rout", tags=["Пример роута"])
money_router = APIRouter(prefix="/add_investment_account", tags=["Добавление счета"])
reports_broker = APIRouter(prefix="/add_reports_broker", tags=["Добавление отчета"])

trans_router.add_api_route("", initial_data, methods=["POST"])
money_router.add_api_route("", add_investment_account, methods=["POST"])
reports_broker.add_api_route("", add_reports_broker, methods=["POST"])

router.include_router(trans_router)
router.include_router(money_router)
router.include_router(reports_broker)
