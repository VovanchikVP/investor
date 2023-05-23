from fastapi import (
    Depends,
    UploadFile,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.schemes import (
    ExampleSchema,
    InvestmentAccountSchema,
)
from src.app.common.exceptions.http_exception import DuplicatedEntryError
from src.app.configs.db import get_session
from src.app.services.example import BrokerReports
from src.app.services.money import InvestmentAccountServices


async def initial_data(file: UploadFile, data: ExampleSchema = Depends()):
    """Пример запроса данных"""
    await BrokerReports.create(file)
    print(data)
    return {"test": "test"}


async def add_investment_account(data: InvestmentAccountSchema, session: AsyncSession = Depends(get_session)):
    """Пример запроса данных"""
    obj = await InvestmentAccountServices.add(session, data)
    try:
        await session.commit()
        return obj
    except IntegrityError as ex:
        await session.rollback()
        raise DuplicatedEntryError("The city is already stored")
