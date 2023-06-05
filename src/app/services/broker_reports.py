import os
import re
import uuid
from datetime import (
    date,
    datetime,
)
from pathlib import Path

import aiofiles
import numpy as np
import pandas as pd
from bs4 import (
    BeautifulSoup,
    PageElement,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.schemes.money import (
    AssetsSchema,
    BrokerReportSchema,
    InvestmentAccountSchema,
    OperationSecuritiesSchema,
    OperationsSchema,
)
from src.app.services.money import (
    AssetsServices,
    BrokerReportServices,
    InvestmentAccountServices,
    OperationSecuritiesServices,
    OperationServices,
)


class BrokerReportSBERServices:
    SPLIT_FOR_INVESTMENT = "Торговый код: "
    MONEY_MOVEMENT_TABLE = "Движение денежных средств за период"
    SECURITIES_TRANSACTIONS_TABLE = "Сделки купли/продажи ценных бумаг"
    SECURITIES_DIRECTORY_TABLE = "Справочник Ценных Бумаг**"
    RENAME_COL_MONEY_MOVEMENT_TABLE = {
        "Дата": "date",
        "Описание операции": "name",
        "Сумма зачисления": "cost__in",
        "Сумма списания": "cost__out",
        "Валюта": "code",
    }
    RENAME_COL_SECURITIES_TRANSACTIONS_TABLE = {
        "Дата заключения": "date",
        "Время заключения": "time",
        "Наименование ЦБ": "name",
        "Код ЦБ": "code",
        "Вид": "operation_type",
        "Количество, шт.": "quantity",
        "Сумма": "sum",
        "НКД": "nkd",
        "Комиссия Брокера": "commission_broker",
        "Комиссия Биржи": "commission_rialto",
        "Номер сделки": "number",
    }
    RENAME_COL_SECURITIES_DIRECTORY_TABLE = {
        "Код": "code",
        "ISIN ценной бумаги": "isin",
    }
    BASE_PATH = os.path.join(Path(__file__).absolute().parents[3], Path(f"data/broker_reports"))

    def __init__(self):
        self.tables_data = {}
        self.file = None
        self.investment_account = None
        self.date_start = None
        self.date_end = None
        self.date_generate = None
        self.broker_report = None
        self.broker_name = None
        self.securities_directory = {}

    @classmethod
    async def create(cls, report):
        self = BrokerReportSBERServices()
        self.file = report
        self.report = await self._get_data_reports(report)
        self.broker_name = "SBER"
        return self

    async def add_money_movement(self, session: AsyncSession):
        """Добаляет данные по движению дежных средств"""

        await self._add_investment_account(session)
        if not self.investment_account:
            return None
        if not await self._add_broker_report_in_db(session):
            return None

        try:
            self.securities_directory = await self._prepare_table_info()
            table: pd.DataFrame = await self._prepare_money_movement_table()
            for i in table.to_dict("records"):
                await OperationServices.add(session, OperationsSchema(**i))
                await self._change_assets(i, session, type_data="money")

            table: pd.DataFrame = await self._prepare_securities_table()
            for i in table.to_dict("records"):
                data = await OperationSecuritiesServices.get_by(session, "number", i["number"])
                if data:
                    continue
                await OperationSecuritiesServices.add(session, OperationSecuritiesSchema(**i))
                await self._change_assets(i, session, type_data="securities")

            await session.commit()
        except Exception as err:
            await session.rollback()
            await BrokerReportServices.delete(session, self.broker_report.id)
            os.remove(self.broker_report.file)
            await session.commit()
            raise err

    async def _change_assets(self, data: dict, session: AsyncSession, type_data: str) -> None:
        """Вносит изменения в данные портфеля"""
        data["investment_account_id"] = self.investment_account.id
        if type_data == "money":
            data["cost_unit"] = 1
            data["quantity"] = data["cost"] if data["type"] == "enrollment" else -data["cost"]
        elif type_data == "securities" and data["operation_type"] == "sale":
            data["quantity"] = -data["quantity"]
        unit = AssetsSchema(**data)

        data = await AssetsServices.get_by_code(data["code"], session)
        if data is None:
            await AssetsServices.add(session, unit)
        else:
            if type_data == "money":
                fields = {"quantity": round(data.quantity + unit.quantity, 2)}
            elif type_data == "securities":
                fields = {"quantity": data.quantity + unit.quantity}
                if unit.quantity > 0:
                    cost_unit = (unit.cost_unit * unit.quantity + data.cost_unit * data.quantity) / (
                        unit.quantity + data.quantity
                    )
                    fields.update({"cost_unit": round(cost_unit, 2)})
            else:
                fields = {}
            if fields["quantity"] == 0 and type_data == "securities":
                await AssetsServices.delete(session, data.id)
            else:
                await AssetsServices.update(session, data.id, fields)

    async def _add_broker_report_in_db(self, session: AsyncSession) -> bool:
        """Добавляет отчет брокера в базу данных"""
        data = BrokerReportSchema(
            date_start=self.date_start,
            date_end=self.date_end,
            file=os.path.join(self.BASE_PATH, Path(f"{uuid.uuid4()}.html")),
            investment_account_id=self.investment_account.id,
        )
        if await BrokerReportServices.duplicate_check(session, data):
            return False

        async with aiofiles.open(data.file, mode="wb") as out_file:
            content = await self.file.read()  # async read
            await out_file.write(content)  # async write
        self.broker_report = await BrokerReportServices.add(session, data)
        await session.commit()
        return True

    async def _get_data_reports(self, report):
        reports = await report.read()
        soup_org_name = BeautifulSoup(reports, "lxml")
        tables = soup_org_name.find_all("table")[:-1]
        dates = soup_org_name.find("h3").text.strip()
        dates = (self.convert_date_format(i) for i in re.findall(r"\d\d.\d\d.\d{4}", dates))
        self.date_start, self.date_end, self.date_generate = dates
        for num, i in enumerate(tables):
            head_position = 1 if num == 1 else 0
            self.tables_data.update((await self._get_data_table(i, head_position),))
        return reports

    async def _get_data_table(self, table: PageElement, head_position: int = 0) -> tuple[str, pd.DataFrame]:
        name = await self._get_investment_account(table.findPrevious("p").text.strip())
        tr = [i for i in table.findAll("tr")]
        head = [i.text for i in tr[head_position].findAll("td")]
        body = [[j.text for j in i.findAll("td")] for i in tr[head_position + 1 :]]
        body = [i for i in body if len(i) == len(head)]
        df = pd.DataFrame(body, columns=head)
        return name, df

    async def _get_investment_account(self, name: str) -> str:
        if self.SPLIT_FOR_INVESTMENT in name:
            self.investment_account = name.split(self.SPLIT_FOR_INVESTMENT)[-1]
        return name

    async def _add_investment_account(self, session: AsyncSession) -> None:
        """Добавляет инвестиционный счет при его отсутствии"""
        if self.investment_account:
            investment_account = await InvestmentAccountServices.get_by_name(self.investment_account, session)
            if investment_account is None:
                investment_account = await InvestmentAccountServices.add(
                    session, InvestmentAccountSchema(name=self.investment_account, broker_name=self.broker_name)
                )
                await session.commit()
            self.investment_account = investment_account

    async def _prepare_money_movement_table(self) -> pd.DataFrame:
        """Преобразование таблицы Движение денежных средств за период"""

        table: pd.DataFrame = self.tables_data.get(self.MONEY_MOVEMENT_TABLE)
        if table is None:
            return pd.DataFrame()
        table = table[list(self.RENAME_COL_MONEY_MOVEMENT_TABLE)].rename(columns=self.RENAME_COL_MONEY_MOVEMENT_TABLE)
        table["name"] = table["name"].apply(lambda x: x.split(" от ")[0])
        table["date"] = table["date"].apply(self.convert_date_format)

        table_in = table[[i for i in self.RENAME_COL_MONEY_MOVEMENT_TABLE.values() if not i.endswith("__out")]]
        table_in = table_in.rename(columns={key: key.split("__")[0] for key in table_in.columns})
        table_in["type"] = np.full(len(table_in), "enrollment")

        table_out = table[[i for i in self.RENAME_COL_MONEY_MOVEMENT_TABLE.values() if not i.endswith("__in")]]
        table_out = table_out.rename(columns={key: key.split("__")[0] for key in table_out.columns})
        table_out["type"] = np.full(len(table_out), "write-off")

        table = pd.concat([table_in, table_out]).reset_index(drop=True)
        table["broker_report_id"] = np.full(len(table), self.broker_report.id)
        table["cost"] = table["cost"].apply(self.str_to_float)
        table["cost"] = table["cost"].round(decimals=2)
        return table[table["cost"] > 0]

    async def _prepare_securities_table(self) -> pd.DataFrame:
        """Преобразование таблицы Сделки купли/продажи ценных бумаг"""
        table: pd.DataFrame = self.tables_data.get(self.SECURITIES_TRANSACTIONS_TABLE)
        if table is None:
            return pd.DataFrame()
        table = table[list(self.RENAME_COL_SECURITIES_TRANSACTIONS_TABLE)].rename(
            columns=self.RENAME_COL_SECURITIES_TRANSACTIONS_TABLE
        )

        table["datetime"] = table["date"].map(str) + " " + table["time"].map(str)
        table["datetime"] = table["datetime"].apply(self.convert_datetime_format)
        table["sum"] = table["sum"].apply(self.str_to_float)
        table["quantity"] = table["quantity"].apply(self.str_to_float)

        table["operation_type"] = table["operation_type"].replace({"Покупка": "purchase", "Продажа": "sale"})
        table["cost_unit"] = table["sum"] / table["quantity"]
        table["cost_unit"] = table["cost_unit"].round(decimals=2)
        table["broker_report_id"] = np.full(len(table), self.broker_report.id)
        table["code"] = table["code"].replace(self.securities_directory)
        return table.drop(["date", "time", "sum"], axis=1)

    async def _prepare_table_info(self) -> dict:
        """Составление словаря кодов инструментов"""
        table: pd.DataFrame = self.tables_data.get(self.SECURITIES_DIRECTORY_TABLE)
        if table is None:
            return {}
        table = table[list(self.RENAME_COL_SECURITIES_DIRECTORY_TABLE)].rename(
            columns=self.RENAME_COL_SECURITIES_DIRECTORY_TABLE
        )
        return dict(zip(table["isin"], table["code"]))

    @staticmethod
    def convert_datetime_format(data: str) -> datetime:
        """Преобразаует строку в объект даты"""
        return datetime.strptime(data, "%d.%m.%Y %H:%M:%S")

    @staticmethod
    def convert_date_format(data: str) -> date:
        """Преобразование строки в дату"""
        return datetime.strptime(data, "%d.%m.%Y").date()

    @staticmethod
    def str_to_float(data: str) -> float:
        """Преобразует строку в число"""
        return float(data.replace(" ", ""))
