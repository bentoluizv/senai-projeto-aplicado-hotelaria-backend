from app.database.db import get_database_session
from app.utils.populate_db import populate_db


def seed():
    session = get_database_session()

    with next(session) as session:
        populate_db(session)


if __name__ == '__main__':
    seed()
