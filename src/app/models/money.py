from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)

from src.app.configs.db import Base


class InvestmentAccount(Base):
    """Инвистиционный счет"""

    __tablename__ = "investment_account"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, unique=True)
    broker_name = Column(String)


class Operations(Base):
    """Денежные операции"""

    __tablename__ = "operations"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    type = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    broker_report_id = Column(Integer, ForeignKey("broker_report.id", ondelete="CASCADE"), nullable=False)


class BrokerReportModel(Base):
    """Отчеты брокера"""

    __tablename__ = "broker_report"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    date_start = Column(Date, nullable=False)
    date_end = Column(Date, nullable=False)
    file = Column(String, nullable=False)
    investment_account_id = Column(Integer, ForeignKey("investment_account.id", ondelete="CASCADE"), nullable=False)


class OperationSecuritiesModel(Base):
    """Опрерации с ценными бумагами"""

    __tablename__ = "operation_securities"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    number = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    operation_type = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    cost_unit = Column(Float, nullable=False)
    nkd = Column(Float, nullable=False)
    commission_broker = Column(Float, nullable=False)
    commission_rialto = Column(Float, nullable=False)
    broker_report_id = Column(Integer, ForeignKey("broker_report.id", ondelete="CASCADE"), nullable=False)


class AssetsModel(Base):
    """Активы (динамическая таблица содержащая данные по текущему состоянию портфеля)"""

    __tablename__ = "assets"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    cost_unit = Column(Float, nullable=False)
    investment_account_id = Column(Integer, ForeignKey("investment_account.id", ondelete="CASCADE"), nullable=False)
