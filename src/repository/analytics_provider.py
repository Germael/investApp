from database import get_session
from repository.stock_scrapper import StockScrapper


class AnalyticsProvider:
    def __init__(self):
        self.db_session = get_session()

    def get_analytics_message(self, scraper: StockScrapper, ticker: str) -> str:
        pass