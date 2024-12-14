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
            response = {
                "annual": {},
                "quarterly": {},
                "other": {}
            }

            # Annual
            response['annual']['revenue'] = self._get_frame_data(ticker_data.financials, "Total Revenue")

            response['annual']['gross_profit'] = self._get_frame_data(ticker_data.financials, "Gross Profit")
            response['annual']['net_income'] = self._get_frame_data(ticker_data.financials, "Net Income")

            response['annual']['total_assets'] = self._get_frame_data(ticker_data.balance_sheet, "Total Assets")
            response['annual']['total_liabilities'] = self._get_frame_data(ticker_data.balance_sheet,
                                                       "Total Liabilities Net Minority Interest")

            response['annual']['free_cash_flow'] = self._get_frame_data(ticker_data.cash_flow, "Free Cash Flow")


            # Quarterly
            response['quarterly']['revenue'] = self._get_frame_data(ticker_data.quarterly_financials, "Total Revenue")

            response['quarterly']['gross_profit'] = self._get_frame_data(ticker_data.quarterly_financials, "Gross Profit")
            response['quarterly']['net_income'] = self._get_frame_data(ticker_data.quarterly_financials, "Net Income")

            response['quarterly']['total_assets'] = self._get_frame_data(ticker_data.quarterly_balance_sheet, "Total Assets")
            response['quarterly']['total_liabilities'] = self._get_frame_data(ticker_data.quarterly_balance_sheet,
                                                       "Total Liabilities Net Minority Interest")

            response['quarterly']['free_cash_flow'] = self._get_frame_data(ticker_data.quarterly_cash_flow, "Free Cash Flow")


            # Other
            response['other']['pe_ratio'] = ticker_data.info.get('trailingPE')
            response['other']['forward_pe'] = ticker_data.info.get('forwardPE')

            return response

        return None

    def _get_frame_data(self, frame: pd.DataFrame, field_name: str) -> dict | None:
        # Check if 'Total Revenue' exists in the DataFrame index
        if field_name not in frame.index:
            return None

        # Extract the 'Total Revenue' data from the DataFrame
        revenue_list = frame.loc[field_name]

        # Filter out any NaN values and sort by date
        revenue_dict = {date: revenue for date, revenue in revenue_list.items() if pd.notna(revenue)}
        revenue_dict = dict(sorted(revenue_dict.items()))

        # Initialize extended data dictionary
        extended_data = {}

        # Calculate price change (if applicable) and store the data
        for i, (current_time, current_value) in enumerate(revenue_dict.items()):
            # Calculate price change for all entries except the first
            change = None if i == 0 else price_change(current_value, list(revenue_dict.values())[i - 1])

            # Add the data to the extended dictionary
            extended_data[current_time] = {
                "value": current_value,
                "change": change
            }

        return extended_data


