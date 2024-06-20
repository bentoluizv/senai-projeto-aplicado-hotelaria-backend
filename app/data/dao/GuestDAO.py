from sqlite3 import Connection

from app.schemas.GuestSchema import GuestDB, GuestSchema


class GuestDAO:
    def __init__(self, db: Connection):
        self.db = db

    def count(self) -> int:
        cursor = self.db.cursor()
        cursor = cursor.execute('SELECT COUNT(*) FROM guest')
        result = cursor.fetchone()

        return result['COUNT(*)']

    def find_many(self) -> list[GuestDB]:
        statement = """SELECT
                        document,
                        created_at,
                        name,
                        surname,
                        country,
                        phone
                    FROM
                        guest;"""

        cursor = self.db.cursor()
        cursor.execute(statement)

        result = cursor.fetchall()

        return [GuestDB(**row) for row in result]

    def find(self, document: str) -> GuestDB | None:
        statement = f"""SELECT
                            document,
                            created_at,
                            name,
                            surname,
                            country,
                            phone
                        FROM
                            guest
                        WHERE
                            guest.document = {document};"""

        cursor = self.db.cursor()
        cursor.execute(statement)
        result = cursor.fetchone()

        if not result:
            return None

        return GuestDB(**result)

    def find_by(self, property: str, value: str) -> list[GuestDB]:
        statement = f"""SELECT
                            document,
                            created_at,
                            name,
                            surname,
                            country,
                            phone
                        FROM
                            guest
                        WHERE
                            guest.{property} = {value};"""

        cursor = self.db.cursor()
        cursor.execute(statement)
        result = cursor.fetchall()
        return [GuestDB(**row) for row in result]

    def create(self, guest: GuestSchema):
        statement = """INSERT
                            INTO guest
                            (
                                document,
                                created_at,
                                name,
                                surname,
                                country,
                                phone
                            )
                        VALUES
                        (
                            :document,
                            :created_at,
                            :name,
                            :surname,
                            :country,
                            :phone
                        );"""

        guest_db = GuestDB(**guest.model_dump())

        cursor = self.db.cursor()
        cursor.execute(statement, guest_db.model_dump())

        self.db.commit()

    def update(self, document: str, guest: GuestSchema) -> None:
        statement = f"""UPDATE
                            guest
                        SET
                            name = :name,
                            surname = :surname,
                            country = :country,
                            phone = :phone
                         WHERE
                        document = {document};"""

        cursor = self.db.cursor()
        cursor.execute(statement, guest.model_dump())

        self.db.commit()

    def delete(self, document: str):
        statement = f"""
                    DELETE
                        FROM
                            guest
                        WHERE
                            document = {document}
                    """

        cursor = self.db.cursor()
        cursor.execute(statement)

        self.db.commit()
