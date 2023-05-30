from datetime import (
    date,
    datetime,
)

from pydantic import BaseModel


class InvestmentAccountSchema(BaseModel):
    name: str
    broker_name: str


class OperationsSchema(BaseModel):
    name: str
    code: str
    date: date
    type: str
    cost: float
    broker_report_id: int


class BrokerReportSchema(BaseModel):
    date_start: date
    date_end: date
    file: str
    investment_account_id: int


class OperationSecuritiesSchema(BaseModel):
    number: str
    datetime: datetime
    name: str
    code: str
    operation_type: str
    quantity: int
    cost_unit: float
    nkd: float
    commission_broker: float
    commission_rialto: float
    broker_report_id: float


class AssetsSchema(BaseModel):
    name: str
    code: str
    quantity: float
    cost_unit: float
    investment_account_id: int
