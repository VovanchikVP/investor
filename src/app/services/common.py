from pydantic import BaseModel
from sqlalchemy import (
    delete,
    select,
    update,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.configs.db import Base


class BaseServices:
    MODEL = Base
    SCHEMA = BaseModel

    @classmethod
    async def get_all(cls, session: AsyncSession):
        """Получает все записи из базы данных"""
        result = await session.execute(select(cls.MODEL))
        return result.scalars().all()

    @classmethod
    async def add(cls, session: AsyncSession, data: SCHEMA):
        """Добавляет запись в базу данных"""
        new_obj = cls.MODEL(**data.dict())
        session.add(new_obj)
        return new_obj

    @classmethod
    async def update(cls, session: AsyncSession, record_id: int, data: dict) -> None:
        """Обновляет запись в базе данных"""
        await session.execute(update(cls.MODEL).where(cls.MODEL.id == record_id).values(**data))

    @classmethod
    async def delete(cls, session: AsyncSession, record_id: int):
        """Удаление записи в БД"""
        return await session.execute(delete(cls.MODEL).where(cls.MODEL.id == record_id).returning(cls.MODEL))

    @classmethod
    async def get_by(cls, session: AsyncSession, param_name: str, param_value: any):
        """Удаление записи в БД"""
        result = await session.execute(select(cls.MODEL).where(getattr(cls.MODEL, param_name) == param_value))
        return result.scalars().all()
