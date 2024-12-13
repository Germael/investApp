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
        bot: Annotated[Bot, Depends()]
) -> list[str]:
    tickers = scraper.get_sp500_tickers()
    add_tickers(db_session, tickers)
    # await bot.send_to_telegram(f"S&P500 tickers parsed: {len(tickers)}")
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
            if ticker_data:
                ticker_info = TickerInfo(
                    ticker_name=ticker.name,
                    short_name=ticker_data.get("shortName"),
                    sector=ticker_data.get("sector"),
                    open=ticker_data.get("open"),
                    current_price=ticker_data.get("currentPrice"),
                    previous_close=ticker_data.get("previousClose"),
                    day_low=ticker_data.get("dayLow"),
                    day_high=ticker_data.get("dayHigh"),
                    dividend_rate=ticker_data.get("dividendRate"),
                    forward_pe=ticker_data.get("forwardPE"),
                    forward_eps=ticker_data.get("forwardEps"),
                    volume=ticker_data.get("volume"),
                    market_cap=ticker_data.get("marketCap"),
                    target_high_price=ticker_data.get("targetHighPrice"),
                    target_low_price=ticker_data.get("targetLowPrice"),
                    target_median_price=ticker_data.get("targetMedianPrice"),
                    target_mean_price=ticker_data.get("targetMeanPrice"),
                    recommendation_key=ticker_data.get("recommendationKey"),
                    opinion_num=ticker_data.get("numberOfAnalystOpinions"),
                    total_cash=ticker_data.get("totalCash"),
                    total_cash_per_share=ticker_data.get("totalCashPerShare"),
                    total_debt=ticker_data.get("totalDebt"),
                    total_revenue=ticker_data.get("totalRevenue"),
                    revenue_per_share=ticker_data.get("revenuePerShare"),
                    free_cash_flow=ticker_data.get("freeCashflow"),
                    operating_cash_flow=ticker_data.get("operatingCashflow"),
                )
                if ticker_info.previous_close and ticker_info.current_price:
                    ticker_info.current_price_change = ((
                                                                ticker_info.current_price - ticker_info.previous_close) / ticker_info.previous_close) * 100
                ticker_info_list.append(ticker_info)

            if len(ticker_info_list) >= 50:
                add_tickers_info(db_session, ticker_info_list)
                ticker_info_list.clear()

        add_tickers_info(db_session, ticker_info_list)

        db_session.commit()
    except Exception as e:
        db_session.rollback()
