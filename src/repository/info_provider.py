from database import get_session
from database.models import TickerInfo
from database.query import get_info_by_field


class InfoProvider:
    def __init__(self):
        self.db_session = get_session()


    def get_ordered_info_message(self, message: str, field: str, order: str = "DESC", limit: int = 5) -> str:
        tickers_info = get_info_by_field(self.db_session, field, order, limit)
        return self.fill_message(message, tickers_info)


    def fill_message(self, message: str, data_list: list[TickerInfo]):
        for ticker_info in data_list:
            message += (f"Company: {ticker_info.short_name}\n"
                        f"Ticker: {ticker_info.ticker_name}\n"
                        f"Price change: {ticker_info.current_price_change:.2f}%\n"
                        f"Recommendation: {ticker_info.recommendation_key}\n\n")
        return message