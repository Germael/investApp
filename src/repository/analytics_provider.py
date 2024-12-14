from database import get_session


class AnalyticsProvider:
    def __init__(self):
        self.db_session = get_session()

    def get_analytics_message(self, ticker: str) -> str:
        pass