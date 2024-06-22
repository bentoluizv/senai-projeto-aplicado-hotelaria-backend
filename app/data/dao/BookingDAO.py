from sqlite3 import Connection

from app.data.dao.schemas.BookingSchema import (
    BookingCreationalSchema,
    BookingDB,
)


class BookingDAO:
    def __init__(self, db: Connection):
        self.db = db

    def count(self) -> int:
        cursor = self.db.cursor()
        cursor = cursor.execute('SELECT COUNT(*) FROM booking')
        result = cursor.fetchone()

        return result['COUNT(*)']

    def find_many(self) -> list[BookingDB]:
        select_all_statement = """
            SELECT
                uuid,
                created_at,
                locator,
                status,
                check_in,
                check_out,
                guest_document,
                accommodation_id,
                budget

            FROM
                booking
        """

        cursor = self.db.cursor()
        cursor.execute(select_all_statement)
        result = cursor.fetchall()

        if not result:
            return []

        return [BookingDB(**element) for element in result]

    def find(self, uuid: str) -> BookingDB | None:
        select_one_statement = """
            SELECT
                uuid,
                created_at,
                locator,
                status,
                check_in,
                check_out,
                guest_document,
                accommodation_id,
                budget
            FROM
                booking
            WHERE
                booking.uuid = ?;
         """

        cursor = self.db.cursor()
        cursor.execute(select_one_statement, (uuid,))
        result = cursor.fetchone()

        if result is None:
            return None

        return BookingDB(**result)

    def find_by(self, property: str, value: str) -> list[BookingDB]:
        select_by_property_statement = f"""
            SELECT
                uuid,
                created_at,
                locator,
                status,
                check_in,
                check_out,
                guest_document,
                accommodation_id,
                budget
            FROM
                booking
            WHERE
                booking.{property} = ?;
        """

        cursor = self.db.cursor()
        cursor.execute(select_by_property_statement, (value,))

        result = cursor.fetchall()

        if result is None:
            return []

        return [BookingDB(**element) for element in result]

    def create(self, data: BookingCreationalSchema):
        insert_statement = """
            INSERT
                INTO booking (
                    uuid,
                    created_at,
                    locator,
                    status,
                    check_in,
                    check_out,
                    guest_document,
                    accommodation_id,
                    budget
                )
                VALUES (
                    :uuid,
                    :created_at,
                    :locator,
                    :status,
                    :check_in,
                    :check_out,
                    :guest_document,
                    :accommodation_id,
                    :budget
                );
        """

        booking_db = BookingDB(**data.model_dump())

        cursor = self.db.cursor()
        cursor.execute(insert_statement, booking_db.model_dump())

        self.db.commit()

    def update(self, booking: BookingDB):
        update_statement = """
            UPDATE
                booking
            SET
                status = :status,
                locator = :locator,
                check_in = :check_in,
                check_out = :check_out,
                guest_document = :guest_document,
                accommodation_id = :accommodation_id,
                budget = :budget
            WHERE
                uuid = :uuid;
        """

        cursor = self.db.cursor()
        cursor.execute(update_statement, booking.model_dump())
        self.db.commit()

    def delete(self, uuid: str):
        statement = 'DELETE FROM booking WHERE uuid = ?'
        cursor = self.db.cursor()
        cursor.execute(statement, (uuid,))
        self.db.commit()
