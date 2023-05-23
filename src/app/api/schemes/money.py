from pydantic import BaseModel


class InvestmentAccountSchema(BaseModel):
    name: str
