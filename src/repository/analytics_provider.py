import pandas as pd

from yfinance import Ticker

from database import get_session
from repository.stock_scrapper import StockScrapper
from repository.utils import price_change


class AnalyticsProvider:
    def __init__(self):
        self.db_session = get_session()

    def get_analytics(self, scraper: StockScrapper, ticker: str):
        ticker_data: Ticker = scraper.get_ticker_info(ticker)

        if ticker_data:
            # Get annual revenue data
            a_revenue_data = self._get_revenue_data(ticker_data.financials)

            # Get quarterly revenue data
            q_revenue_data = self._get_revenue_data(ticker_data.quarterly_financials)

        return None

    def _get_revenue_data(self, financials: pd.DataFrame) -> dict | None:
        # Check if 'Total Revenue' exists in the DataFrame index
        if 'Total Revenue' not in financials.index:
            return None

        # Extract the 'Total Revenue' data from the DataFrame
        revenue_list = financials.loc['Total Revenue']

        # Filter out any NaN values and sort by date
        revenue_dict = {date: revenue for date, revenue in revenue_list.items() if pd.notna(revenue)}
        revenue_dict = dict(sorted(revenue_dict.items()))

        # Initialize extended data dictionary
        extended_data = {}

        # Calculate price change (if applicable) and store the data
        for i, (current_time, current_price) in enumerate(revenue_dict.items()):
            # Calculate price change for all entries except the first
            change = None if i == 0 else price_change(current_price, list(revenue_dict.values())[i - 1])

            # Add the data to the extended dictionary
            extended_data[current_time] = {
                "price": current_price,
                "change": change
            }

        return extended_data


