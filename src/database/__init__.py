from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from database.models import Base

DATABASE_URL = getenv("DATABASE_URL")

# Create an engine to connect to the SQLite database
engine = create_engine(DATABASE_URL, echo=True)

# Create the database tables
Base.metadata.create_all(engine)


def get_session() -> Session:
    Session = sessionmaker(bind=engine)
    return Session()
