import pandas as pd

from yfinance import Ticker

from database import get_session
from repository.utils import price_change


class AnalyticsProvider:
    def __init__(self):
        self.db_session = get_session()

    def get_analytics(self, ticker: Ticker):
        return {
            "annual": self.get_annual_analytics(ticker),
            "quarterly": self.get_quarter_analytics(ticker),
            "other": self.get_other_analytics(ticker)
        }

    def get_annual_analytics(self, ticker: Ticker) -> dict:
        return {
            'revenue': self._get_frame_data(ticker.financials, "Total Revenue"),
            'gross_profit': self._get_frame_data(ticker.financials, "Gross Profit"),
            'net_income': self._get_frame_data(ticker.financials, "Net Income"),
            'total_assets': self._get_frame_data(ticker.balance_sheet, "Total Assets"),
            'total_liabilities': self._get_frame_data(ticker.balance_sheet,
                                                      "Total Liabilities Net Minority Interest"),
            'free_cash_flow': self._get_frame_data(ticker.cash_flow, "Free Cash Flow")
        }

    def get_quarter_analytics(self, ticker: Ticker) -> dict:
        return {
            'revenue': self._get_frame_data(ticker.quarterly_financials, "Total Revenue"),
            'gross_profit': self._get_frame_data(ticker.quarterly_financials, "Gross Profit"),
            'net_income': self._get_frame_data(ticker.quarterly_financials, "Net Income"),
            'total_assets': self._get_frame_data(ticker.quarterly_balance_sheet, "Total Assets"),
            'total_liabilities': self._get_frame_data(ticker.quarterly_balance_sheet,
                                                      "Total Liabilities Net Minority Interest"),
            'free_cash_flow': self._get_frame_data(ticker.quarterly_cash_flow, "Free Cash Flow")
        }

    def get_other_analytics(self, ticker: Ticker) -> dict:
        return {
            'pe_ratio': ticker.info.get('trailingPE'),
            'forward_pe': ticker.info.get('forwardPE'),
        }

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
