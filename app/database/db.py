from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database.models import Base
from app.settings.Settings import Settings

engine = create_engine(Settings().DATABASE_URL)  # type: ignore

Base.metadata.create_all(bind=engine, checkfirst=True)


def get_database_session():
    with Session(engine) as session:
        yield session
