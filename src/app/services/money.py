from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.schemes import (
    AssetsSchema,
    BrokerReportSchema,
    InvestmentAccountSchema,
    OperationSecuritiesSchema,
    OperationsSchema,
)
from src.app.models.money import (
    AssetsModel,
    BrokerReportModel,
    InvestmentAccount,
    Operations,
    OperationSecuritiesModel,
)
from src.app.services.common import BaseServices


class InvestmentAccountServices(BaseServices):
    MODEL = InvestmentAccount
    SCHEMA = InvestmentAccountSchema

    @classmethod
    async def get_by_name(cls, name: str, session: AsyncSession) -> MODEL:
        result = await session.execute(select(cls.MODEL).where(cls.MODEL.name == name))
        return result.scalars().first()


class OperationServices(BaseServices):
    MODEL = Operations
    SCHEMA = OperationsSchema


class BrokerReportServices(BaseServices):
    MODEL = BrokerReportModel
    SCHEMA = BrokerReportSchema

    @classmethod
    async def duplicate_check(cls, session: AsyncSession, data: SCHEMA) -> bool:
        """Проверяет осуществлена ли загрузка"""
        data = await session.execute(
            select(cls.MODEL)
            .where(cls.MODEL.investment_account_id == data.investment_account_id)
            .where(cls.MODEL.date_start == data.date_start)
            .where(cls.MODEL.date_end == data.date_end)
        )
        if data.scalars().first() is None:
            return False
        return True


class OperationSecuritiesServices(BaseServices):
    MODEL = OperationSecuritiesModel
    SCHEMA = OperationSecuritiesSchema


class AssetsServices(BaseServices):
    MODEL = AssetsModel
    SCHEMA = AssetsSchema

    @classmethod
    async def get_by_code(cls, code: str, session: AsyncSession) -> MODEL:
        result = await session.execute(select(cls.MODEL).where(cls.MODEL.code == code))
        return result.scalars().first()
