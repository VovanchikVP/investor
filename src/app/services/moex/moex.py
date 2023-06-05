from datetime import (
    datetime,
    timedelta,
)

import aiohttp
import aiomoex
import pandas as pd


async def get_date(security: str) -> pd.DataFrame:
    """Получение доступных дат по данным"""
    async with aiohttp.ClientSession() as session:
        data = await aiomoex.get_market_candle_borders(session, security)
        return pd.DataFrame(data)


async def get_data_tool(security: str):
    """Получение данных по инструменту"""
    async with aiohttp.ClientSession() as session:
        return await aiomoex.find_securities(session, security, columns=None)


async def get_values_reference(name: str):
    """Варианты значений плейсхолдеров"""
    async with aiohttp.ClientSession() as session:
        return await aiomoex.get_reference(session, name)


async def get_data_now(security: str) -> dict:
    """Получение данных за текущие сутки"""
    datetime_utcnow = datetime.utcnow()
    if datetime_utcnow.weekday() == 0 and datetime_utcnow.hour <= 7:
        datetime_utcnow = datetime_utcnow - timedelta(days=3)
    elif datetime_utcnow.weekday() > 4:
        datetime_utcnow = datetime_utcnow - timedelta(days=datetime_utcnow.weekday() - 4)
    elif datetime_utcnow.hour <= 7:
        datetime_utcnow = datetime_utcnow - timedelta(days=1)
    date_now = datetime_utcnow.strftime("%Y-%m-%d")
    async with aiohttp.ClientSession() as session:
        data = await get_data_tool_by_code(security)
        data = await aiomoex.get_market_candles(session, security, 24, date_now, date_now, **data)
        return data[0] if data else {}


async def get_data_tool_by_code(security: str) -> dict:
    """Получение данных по инструменту по коду инструмента"""

    request_url = f"https://iss.moex.com/iss/securities/{security}.json"
    arguments = {"description.columns": ("name," "value")}
    async with aiohttp.ClientSession() as session:
        iss = aiomoex.ISSClient(session, request_url, arguments)
        data = await iss.get()
    df = pd.DataFrame(data["description"])
    if len(df):
        data = df.loc[df["name"] == "GROUP"]["value"].iloc[0].split("_")
        return dict(zip(("engine", "market"), data))
    return {}
