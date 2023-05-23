from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.configs.db import Base


class BaseServices:
    MODEL = Base
    SCHEMA = BaseModel

    @classmethod
    async def get_all(cls, session: AsyncSession):
        result = await session.execute(select(cls.MODEL))
        return result.scalars().all()

    @classmethod
    async def add(cls, session: AsyncSession, data: SCHEMA):
        new_obj = cls.MODEL(**data.dict())
        session.add(new_obj)
        return new_obj
