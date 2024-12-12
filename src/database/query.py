from sqlalchemy.orm import Session
from sqlalchemy import delete, select, Sequence

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
    try:
        delete(TickerInfo)
        db_session.bulk_save_objects(tickers_info)
        db_session.commit()
    except Exception as e:
        db_session.rollback()


def get_all_tickers(db_session: Session) -> list[Ticker]:
    tickers_response = db_session.execute(select(Ticker))
    tickers = tickers_response.scalars().all()
    return list(tickers)
