from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Ticker(Base):
    __tablename__ = "ticker"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    sp_ticker = Column(Boolean, default=True)


class TickerInfo(Base):
    __tablename__ = "ticker_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker_name = Column(String, nullable=False)
    open = Column(Float)
    previous_close = Column(Float)
    day_low = Column(Float)
    day_high = Column(Float)
    dividend_rate = Column(Float)
    forward_pe = Column(Float)
    volume = Column(Integer)
    market_cap = Column(Integer)

