from sqlalchemy.orm import Session

from database import get_session
from database.models import TickerInfo
from database.query import get_info_by_field


class InfoProvider:
    def __init__(self):
        self.db_session = get_session()


    def get_ordered_info(self, field: str, order: str = "DESC", limit: int = 10) -> list[TickerInfo]:
        return get_info_by_field(self.db_session, field, order, limit)