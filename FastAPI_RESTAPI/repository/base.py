from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:***********@localhost:5432/diploma"

Session = sessionmaker()
engine = create_engine(DATABASE_URL, echo=True)
Session.configure(bind=engine)


def get_session():
    return Session()
