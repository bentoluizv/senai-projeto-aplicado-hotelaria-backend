from sqlite3 import Connection

from app.schemas.BookingSchema import BookingDB, BookingSchema


class BookingDAO:
    def __init__(self, db: Connection):
        self.db = db

    def count(self) -> int:
        cursor = self.db.cursor()
        cursor = cursor.execute('SELECT COUNT(*) FROM booking')
        result = cursor.fetchone()

        return result['COUNT(*)']

    def find_many(self):
        statement = """
            SELECT
                uuid,
                status,
                created_at,
                check_in,
                check_out,
                document,
                accommodation_id
            FROM
                booking
        """

        cursor = self.db.cursor()
        cursor.execute(statement)
        result = cursor.fetchall()

        if not result:
            return []

        return [BookingDB(**element) for element in result]

    def update(self, uuid: str, data: BookingSchema):
        statement = """
            UPDATE
                booking
            SET
                status = :status,
                check_in = :check_in,
                check_out = :check_out,
                guest_document = :guest_document,
                accommodation_id = :accommodation_id
                buggert
            WHERE
                uuid = :;
        """

        cursor = self.db.cursor()
        cursor.execute(
            statement,
            (
                data.status,
                data.check_in,
                data.check_out,
                data.guest_documemt,
                data.accommodation_id,
                uuid,
            ),
        )
        self.db.commit()

    def insert(self, data: BookingSchema):
        booking_db = BookingDB(**data.model_dump())

        insert_statement = """
            INSERT
                INTO
                    booking
                        (
                        uuid,
                        created_at,
                        status,
                        check_in,
                        check_out,
                        guest_document,
                        accommodation_id
                        budget
                        )
                VALUES
                    (
                    :uuid,
                    :created_at,
                    :status,
                    :check_in,
                    :check_out,
                    :guest_document,
                    :accommodation_id,
                    :budget
                    );
            """

        cursor = self.db.cursor()
        cursor.execute(insert_statement, booking_db.model_dump())

        self.db.commit()

    def find(self, uuid: str) -> BookingDB | None:
        cursor = self.db.cursor()
        cursor.execute(
            f"""SELECT
                    uuid,
                    created_at,
                    status,
                    check_in,
                    check_out,
                    accommodation_id
                    guest_document
                FROM booking
                WHERE booking.uuid = {uuid};""",
        )

        result = cursor.fetchone()

        if result is None:
            return None

        return BookingDB(**result)

    def findBy(self, property: str, value: str):
        cursor = self.db.cursor()
        cursor.execute(
            f"""SELECT
                    uuid,
                    created_at,
                    status,
                    check_in,
                    check_out,
                    accommodation_id
                    guest_document
                FROM booking
                WHERE booking.{property} = {value};""",
        )

        result = cursor.fetchall()

        if result is None:
            return []

        return [BookingDB(**element) for element in result]

    def delete(self, uuid: str):
        statement = 'DELETE FROM booking WHERE uuid = ?'
        cursor = self.db.cursor()
        cursor.execute(statement, (uuid,))
        self.db.commit()
