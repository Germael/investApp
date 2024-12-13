from sqlalchemy.orm import Session
from sqlalchemy import delete, select, asc, desc

from database.models import Ticker, TickerInfo


def add_tickers(db_session: Session, ticker_names: list[str]):
    tickers = []

    try:
        db_session.execute(delete(Ticker).where(Ticker.sp_ticker))

        for name in ticker_names:
            tickers.append(Ticker(name=name))

        db_session.bulk_save_objects(tickers)
        db_session.commit()
    except Exception as e:
        db_session.rollback()


def add_tickers_info(db_session: Session, tickers_info: list[TickerInfo]):
    db_session.bulk_save_objects(tickers_info)


def delete_tickers_info(db_session: Session):
    db_session.execute(delete(TickerInfo))


def get_ticker_data(db_session: Session, ticker: str):
    ticker_info = db_session.query(TickerInfo).where(TickerInfo.ticker_name == ticker.upper()).first()
    return ticker_info

def get_all_tickers(db_session: Session) -> list[Ticker]:
    tickers_response = db_session.execute(select(Ticker))
    tickers = tickers_response.scalars().all()
    return list(tickers)


def get_info_by_field(db_session: Session, field: str, order: str = "DESC", limit: int = 10) -> list[TickerInfo]:
    # Determine the sorting order (ASC or DESC)
    sorting_order = desc if order.upper() == "DESC" else asc

    # Get the field dynamically from the TickerInfo model
    field_column = getattr(TickerInfo, field, None)
    if field_column is None:
        raise ValueError(f"Invalid field '{field}' for sorting.")

    # Build the query with ordering
    query = select(TickerInfo).where(field_column.isnot(None)).order_by(sorting_order(field_column)).limit(limit)

    # Execute the query and fetch results
    tickers_response = db_session.execute(query)
    tickers = tickers_response.scalars().all()
    return list(tickers)
