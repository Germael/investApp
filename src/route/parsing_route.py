from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_session
from database.models import TickerInfo
from database.query import add_tickers, get_all_tickers, add_tickers_info, delete_tickers_info
from repository.bot import Bot
from repository.stock_scrapper import StockScrapper

parse_router = APIRouter(prefix="/parse", tags=["parse"])


@parse_router.get("/sp500-tickers")
async def parse_sp500_tickers(
        scraper: Annotated[StockScrapper, Depends()],
        db_session: Annotated[Session, Depends(get_session)],
) -> list[str]:
    tickers = scraper.get_sp500_tickers()
    add_tickers(db_session, tickers)
    return tickers


@parse_router.get("/tickers-info")
def parse_sp500_tickers(
        scraper: Annotated[StockScrapper, Depends()],
        db_session: Annotated[Session, Depends(get_session)]
):
    ticker_info_list = []
    tickers = get_all_tickers(db_session)

    try:
        delete_tickers_info(db_session)

        for ticker in tickers:
            ticker_data = scraper.get_ticker_info(ticker.name)
            if ticker_data and ticker_data.info:
                ticker_info = TickerInfo(
                    ticker_name=ticker.name,
                    short_name=ticker_data.info.get("shortName"),
                    sector=ticker_data.info.get("sector"),
                    open=ticker_data.info.get("open"),
                    current_price=ticker_data.info.get("currentPrice"),
                    previous_close=ticker_data.info.get("previousClose"),
                    day_low=ticker_data.info.get("dayLow"),
                    day_high=ticker_data.info.get("dayHigh"),
                    dividend_rate=ticker_data.info.get("dividendRate"),
                    forward_pe=ticker_data.info.get("forwardPE"),
                    forward_eps=ticker_data.info.get("forwardEps"),
                    volume=ticker_data.info.get("volume"),
                    market_cap=ticker_data.info.get("marketCap"),
                    target_high_price=ticker_data.info.get("targetHighPrice"),
                    target_low_price=ticker_data.info.get("targetLowPrice"),
                    target_median_price=ticker_data.info.get("targetMedianPrice"),
                    target_mean_price=ticker_data.info.get("targetMeanPrice"),
                    recommendation_key=ticker_data.info.get("recommendationKey"),
                    opinion_num=ticker_data.info.get("numberOfAnalystOpinions"),
                    total_cash=ticker_data.info.get("totalCash"),
                    total_cash_per_share=ticker_data.info.get("totalCashPerShare"),
                    total_debt=ticker_data.info.get("totalDebt"),
                    total_revenue=ticker_data.info.get("totalRevenue"),
                    revenue_per_share=ticker_data.info.get("revenuePerShare"),
                    free_cash_flow=ticker_data.info.get("freeCashflow"),
                    operating_cash_flow=ticker_data.info.get("operatingCashflow"),
                )
                if ticker_info.previous_close and ticker_info.current_price:
                    ticker_info.current_price_change = ((
                                                                ticker_info.current_price - ticker_info.previous_close) / ticker_info.previous_close) * 100
                ticker_info_list.append(ticker_info)
            else:
                continue

            if len(ticker_info_list) >= 50:
                add_tickers_info(db_session, ticker_info_list)
                ticker_info_list.clear()

        add_tickers_info(db_session, ticker_info_list)

        db_session.commit()
    except Exception as e:
        db_session.rollback()
