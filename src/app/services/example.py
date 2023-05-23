from bs4 import (
    BeautifulSoup,
    PageElement,
)


class BrokerReports:
    @classmethod
    async def create(cls, report):
        self = BrokerReports()
        self.report = await cls._get_data_reports(report)
        return self

    @classmethod
    async def _get_data_reports(cls, report):
        reports = await report.read()
        soup_org_name = BeautifulSoup(reports, "lxml")
        tables = soup_org_name.find_all("table")[:-1]
        for i in tables:
            await cls._get_data_table(i)
        return reports

    @classmethod
    async def _get_data_table(cls, table: PageElement):
        tr = [i for i in table.findAll("tr")]
        head = [i.text for i in tr[0].findAll("td")]
        body = [[j.text for j in i.findAll("td")] for i in tr[1:]]
        print(head)
        print(body)
