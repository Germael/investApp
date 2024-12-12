from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_session
from database.models import TickerInfo
from database.query import add_tickers, get_all_tickers, add_tickers_info
from repository.bot import Bot
from repository.stock_scrapper import StockScrapper
from repository.utils import camel_to_snake

parse_router = APIRouter()


@parse_router.get("/parse-sp500-tickers")
async def parse_sp500_tickers(
        scraper: Annotated[StockScrapper, Depends()],
        db_session: Annotated[Session, Depends(get_session)],
        bot: Annotated[Bot, Depends()]
) -> list[str]:
    tickers = scraper.get_sp500_tickers()
    add_tickers(db_session, tickers)
    await bot.send_to_telegram(f"S&P500 tickers parsed: {len(tickers)}")
    return tickers


@parse_router.get("/parse-tickers-info")
def parse_sp500_tickers(
        scraper: Annotated[StockScrapper, Depends()],
        db_session: Annotated[Session, Depends(get_session)]
):
    ticker_info_list = []
    tickers = get_all_tickers(db_session)

    for ticker in tickers:
        ticker_data = scraper.get_ticker_info(ticker.name)
        if ticker_data:
            ticker_info_list.append(
                TickerInfo(
                    ticker_id=ticker.id,
                    open=ticker_data.get("open"),
                    previous_close=ticker_data.get("previousClose"),
                    day_low=ticker_data.get("dayLow"),
                    day_high=ticker_data.get("dayHigh"),
                    dividend_rate=ticker_data.get("dividendRate"),
                    forward_pe=ticker_data.get("forwardPE"),
                    volume=ticker_data.get("volume"),
                    market_cap=ticker_data.get("marketCap"),
                )
            )

    add_tickers_info(db_session, ticker_info_list)



