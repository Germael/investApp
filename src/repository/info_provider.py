from database import get_session
from database.models import TickerInfo
from database.query import get_info_by_field, get_ticker_data


class InfoProvider:
    def __init__(self):
        self.db_session = get_session()

    def get_ordered_info_message(self, message: str, field: str, order: str = "DESC", limit: int = 5) -> str:
        tickers_info = get_info_by_field(self.db_session, field, order, limit)
        return self.fill_message(message, tickers_info)

    def get_ticker_info_message(self, ticker):
        ticker_info = get_ticker_data(self.db_session, ticker)
        if ticker_info:
            return self.fill_ticker_message(ticker_info)
        else:
            return f"{ticker} ticker not found."

    @staticmethod
    def fill_message(message: str, data_list: list[TickerInfo]):
        for ticker_info in data_list:
            message += (f"Company: {ticker_info.short_name}\n"
                        f"Ticker: {ticker_info.ticker_name}\n"
                        f"Price change: {ticker_info.current_price_change:.2f}%\n"
                        f"Recommendation: {ticker_info.recommendation_key}\n\n")
        return message

    @staticmethod
    def fill_ticker_message(ticker_info: TickerInfo):
        def calculate_price_change(target_price):
            if target_price and ticker_info.current_price:
                return ((target_price - ticker_info.current_price) / ticker_info.current_price) * 100
            return None

        projected_changes = {
            "median": calculate_price_change(ticker_info.target_median_price),
            "mean": calculate_price_change(ticker_info.target_mean_price),
            "low": calculate_price_change(ticker_info.target_low_price),
            "high": calculate_price_change(ticker_info.target_high_price),
        }

        return (
            f"Company: {ticker_info.short_name}\n"
            f"Ticker: {ticker_info.ticker_name}\n"
            f"Price change: {ticker_info.current_price_change:.1f}%\n"
            f"Recommendation: {ticker_info.recommendation_key}\n\n"
            f"Current price: {ticker_info.current_price}\n\n"
            f"Median price: {ticker_info.target_median_price:.1f}  {projected_changes['median']:.2f}%\n"
            f"Mean price: {ticker_info.target_mean_price:.1f}  {projected_changes['mean']:.2f}%\n"
            f"High price: {ticker_info.target_high_price:.1f}  {projected_changes['high']:.2f}%\n"
            f"Low price: {ticker_info.target_low_price:.1f}  {projected_changes['low']:.2f}%\n\n"
            f"Market cap: {ticker_info.market_cap / 1_000_000:,.0f} M\n"
            f"Total revenue: {ticker_info.total_revenue / 1_000_000:,.0f} M\n"
            f"Free cash flow: {ticker_info.free_cash_flow / 1_000_000:,.0f} M\n"
            f"Total debt: {ticker_info.total_debt / 1_000_000:,.0f} M\n\n"
            f"ForwardPE: {ticker_info.forward_pe:.2f}\n"
        )
