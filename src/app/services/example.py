import pandas as pd
from bs4 import (
    BeautifulSoup,
    PageElement,
)


class BrokerReports:
    TABLE_NAMES = [
        "Оценка активов на конец периода",
        "Портфель Ценных Бумаг",
        "Денежные средства",
        "Движение денежных средств за период",
        "Сделки купли/продажи ценных бумаг",
        "Справочник Ценных Бумаг",
    ]

    def __init__(self):
        self.tables_data = {}

    @classmethod
    async def create(cls, report):
        self = BrokerReports()
        self.report = await self._get_data_reports(report)
        return self

    async def _get_data_reports(self, report):
        reports = await report.read()
        soup_org_name = BeautifulSoup(reports, "lxml")
        tables = soup_org_name.find_all("table")[:-1]
        for num, i in enumerate(tables):
            head_position = 1 if num == 1 else 0
            self.tables_data[self.TABLE_NAMES[num]] = await self._get_data_table(i, head_position)
        return reports

    @classmethod
    async def _get_data_table(cls, table: PageElement, head_position: int = 0) -> pd.DataFrame:
        tr = [i for i in table.findAll("tr")]
        head = [i.text for i in tr[head_position].findAll("td")]
        body = [[j.text for j in i.findAll("td")] for i in tr[head_position + 1 :]]
        body = [i for i in body if len(i) == len(head)]
        df = pd.DataFrame(body, columns=head)
        return df
