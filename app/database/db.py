from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.database.db_init import db_init
from app.database.models import Base, GuestDB

engine = create_engine('sqlite:///./database.db')

Base.metadata.create_all(engine)


with Session(engine) as session:
    existing_data = session.scalars(select(GuestDB)).all()

    if len(existing_data) == 0:
        db_init(session)
        session.commit()
        session.close()


def get_session():
    with Session(engine) as session:
        yield session

        session.commit()
        session.close()
