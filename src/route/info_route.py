from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_session
from database.models import TickerInfo
from repository.bot import Bot
from repository.info_provider import InfoProvider

info_router = APIRouter(prefix="/info")


@info_router.get("/overview")
async def get_top_performers(
        info_provider: Annotated[InfoProvider, Depends()],
        bot: Annotated[Bot, Depends()]
):

    def fill_message(message: str, data_list: list[TickerInfo]):
        for ticker_info in data_list:
            message += (f"Company: {ticker_info.short_name}\n"
                        f"Ticker: {ticker_info.ticker_name}\n"
                        f"Price change: {ticker_info.current_price_change:.2f}%\n"
                        f"Currency price: {ticker_info.current_price}\n"
                        f"Recommendation: {ticker_info.recommendation_key}\n\n")
        return message

    tickers_info = info_provider.get_ordered_info("current_price_change")
    message = "Best performers\n\n"
    await bot.send_to_telegram(fill_message(message, tickers_info))

    tickers_info = info_provider.get_ordered_info("current_price_change", "ASC")
    message = f"Worst performers\n\n"
    await bot.send_to_telegram(fill_message(message, tickers_info))
