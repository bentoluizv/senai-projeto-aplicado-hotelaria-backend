from app.database.db import get_database_session
from app.utils.populate_db import populate_db


def init_db():
    session = get_database_session()
    session = next(session)
    populate_db(session)


if __name__ == '__main__':
    init_db()
