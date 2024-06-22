from sqlite3 import Connection

from app.data.dao.schemas.GuestSchema import GuestCreationalSchema, GuestDB


class GuestDAO:
    def __init__(self, db: Connection):
        self.db = db

    def count(self) -> int:
        cursor = self.db.cursor()
        cursor = cursor.execute('SELECT COUNT(*) FROM guest')
        result = cursor.fetchone()

        return result['COUNT(*)']

    def find_many(self) -> list[GuestDB]:
        select_all_statement = """
            SELECT
                document,
                created_at,
                name,
                surname,
                country,
                phone
            FROM
                guest;
        """

        cursor = self.db.cursor()
        cursor.execute(select_all_statement)
        result = cursor.fetchall()

        return [GuestDB(**row) for row in result]

    def find(self, document: str) -> GuestDB | None:
        select_by_id_statement = """
            SELECT
                document,
                created_at,
                name,
                surname,
                country,
                phone
            FROM
                guest
            WHERE
                guest.document = ?;
        """

        cursor = self.db.cursor()
        cursor.execute(select_by_id_statement, (document,))
        result = cursor.fetchone()

        if not result:
            return None

        return GuestDB(**result)

    def find_by(self, property: str, value: str) -> list[GuestDB]:
        select_by_property_statement = f"""
            SELECT
                document,
                created_at,
                name,
                surname,
                country,
                phone
            FROM
                guest
            WHERE
                guest.{property} = ?;
        """

        cursor = self.db.cursor()
        cursor.execute(select_by_property_statement, (value,))
        result = cursor.fetchall()

        return [GuestDB(**row) for row in result]

    def create(self, guest: GuestCreationalSchema):
        create_statement = """
            INSERT
                INTO guest (
                    document,
                    created_at,
                    name,
                    surname,
                    country,
                    phone
                )
                VALUES (
                    :document,
                    :created_at,
                    :name,
                    :surname,
                    :country,
                    :phone
                );
        """

        guest_db = GuestDB(**guest.model_dump())

        cursor = self.db.cursor()
        cursor.execute(create_statement, guest_db.model_dump())
        self.db.commit()

    def update(self, guest: GuestCreationalSchema) -> None:
        update_statement = """
            UPDATE
                guest
            SET
                name = :name,
                surname = :surname,
                country = :country,
                phone = :phone
            WHERE
                document = :document;
        """

        cursor = self.db.cursor()
        cursor.execute(update_statement, guest.model_dump())
        self.db.commit()

    def delete(self, document: str):
        delete_statement = """
            DELETE
                FROM
                    guest
                WHERE
                    document = ?
        """

        cursor = self.db.cursor()
        cursor.execute(delete_statement, (document,))
        self.db.commit()
