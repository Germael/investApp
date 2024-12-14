from typing import Annotated

from fastapi import APIRouter, Depends

from repository.analytics_provider import AnalyticsProvider
from repository.stock_scrapper import StockScrapper

analytics_route = APIRouter(prefix="/analytics", tags=["analytics"])


@analytics_route.get("/overview/{ticker}")
async def get_ticker_analytics(
        provider: Annotated[AnalyticsProvider, Depends()],
        scraper: Annotated[StockScrapper, Depends()],
        ticker: str,
):
    return provider.get_analytics(scraper, ticker)