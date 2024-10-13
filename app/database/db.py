from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database.models import Base

engine = create_engine('sqlite:///./database.db')

Base.metadata.create_all(engine)


def get_database_session():
    with Session(engine) as session:
        yield session
