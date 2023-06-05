import asyncio

from src.app.configs.db import async_session
from src.app.services.moex.moex import get_data_now
from src.app.services.money import AssetsServices


class AssetVerificationServices:
    EXCLUDE_CODE = ["RUB"]

    @classmethod
    async def create(cls):
        session = async_session()
        assets = await AssetsServices.get_all(session)
        moex_data = await cls._get_data_moex(assets)
        print(moex_data)

    @classmethod
    async def _get_data_moex(cls, assets):
        """Получение данных с московской биржи по активам в портфеле"""
        moex_data = {}
        pending = [
            asyncio.create_task(get_data_now(i.code), name=i.code) for i in assets if i.code not in cls.EXCLUDE_CODE
        ]
        while pending:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
            for done_task in done:
                moex_data[done_task.get_name()] = await done_task
        return moex_data
