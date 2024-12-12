from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from database.models import Base, Ticker

# DATABASE_URL = "sqlite:///db/invest.db"
DATABASE_URL = "sqlite:///invest.db"

# Create an engine to connect to the SQLite database
engine = create_engine(DATABASE_URL, echo=True)

# Create the database tables
# Base.metadata.create_all(engine)


def get_session() -> Session:
    Session = sessionmaker(bind=engine)
    return Session()
