from src.app.api.schemes import InvestmentAccountSchema
from src.app.models.money import InvestmentAccount
from src.app.services.common import BaseServices


class InvestmentAccountServices(BaseServices):
    MODEL = InvestmentAccount
    SCHEMA = InvestmentAccountSchema
