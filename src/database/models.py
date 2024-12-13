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
    short_name = Column(String)
    sector = Column(String)
    open = Column(Float)
    current_price = Column(Float)
    previous_close = Column(Float)
    day_low = Column(Float)
    day_high = Column(Float)
    current_price_change = Column(Float)
    dividend_rate = Column(Float)
    forward_pe = Column(Float)
    forward_eps = Column(Float)
    volume = Column(Integer)
    market_cap = Column(Integer)
    target_high_price = Column(Float)
    target_low_price = Column(Float)
    target_median_price = Column(Float)
    target_mean_price = Column(Float)
    recommendation_key = Column(String)
    opinion_num = Column(Integer)
    total_cash = Column(Integer)
    total_cash_per_share = Column(Float)
    total_debt = Column(Integer)
    total_revenue = Column(Integer)
    revenue_per_share = Column(Float)
    free_cash_flow = Column(Integer)
    operating_cash_flow = Column(Integer)


