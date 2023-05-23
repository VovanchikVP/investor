from sqlalchemy import (
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
)

from src.app.configs.db import Base


class InvestmentAccount(Base):
    __tablename__ = "investment_account"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, unique=True)


class Operations(Base):
    __tablename__ = "operations"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, unique=True)
    date = Column(Date, nullable=False)
    type = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    investment_account_id = Column(Integer, ForeignKey("investment_account.id", ondelete="CASCADE"), nullable=False)
