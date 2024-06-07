from sqlite3 import Connection
from typing import List, TypedDict


class BookingDTO(TypedDict):
    status: str
    check_in: str
    created_at: str
    uuid: str
    check_out: str
    guest_document: str
    accommodation_uuid: str


class BookingDAO:
    def __init__(self, db: Connection):
        self.db = db

    def count(self):
        cursor = self.db.cursor()
        count = (
            cursor.execute("SELECT COUNT(*) FROM booking").fetchone().get("COUNT(*)")
        )
        return count

    def insert(self, booking: BookingDTO) -> None:
        statement = "INSERT INTO booking (uuid, created_at, status, check_in, check_out, document, accommodation_uuid) VALUES (?, ?, ?, ?, ?, ?, ?);"
        cursor = self.db.cursor()
        cursor.execute(
            statement,
            (
                booking["uuid"],
                booking["created_at"],
                booking["status"],
                booking["check_in"],
                booking["check_out"],
                booking["guest_document"],
                booking["accommodation_uuid"],
            ),
        )
        self.db.commit()

    def findBy(self, property: str, value: str):
        cursor = self.db.cursor()
        cursor.execute(
            f"SELECT uuid, status, created_at, check_in, check_out, document, accommodation_uuid FROM booking WHERE booking.{property} = ?;",
            (value,),
        )
        booking = cursor.fetchone()

        if booking is None:
            return None

        guest_document = booking["document"]
        accommodation_uuid = booking["accommodation_uuid"]

        cursor.execute(
            "SELECT created_at, document, name, surname, country, phone FROM guest WHERE guest.document = ?",
            (guest_document,),
        )
        guest = cursor.fetchone()

        cursor.execute(
            "SELECT uuid, created_at, name, status, total_guests, single_beds, double_beds, min_nights, price FROM accommodation WHERE accommodation.uuid = ?",
            (accommodation_uuid,),
        )
        accommodation = cursor.fetchone()

        data = {
            "uuid": booking["uuid"],
            "status": booking["status"],
            "created_at": booking["created_at"],
            "check_in": booking["check_in"],
            "check_out": booking["check_out"],
            "guest": {
                "document": guest["document"],
                "created_at": guest["created_at"],
                "name": guest["name"],
                "surname": guest["surname"],
                "country": guest["country"],
                "phone": guest["phone"],
            },
            "accommodation": {
                "uuid": accommodation["uuid"],
                "created_at": accommodation["created_at"],
                "name": accommodation["name"],
                "status": accommodation["status"],
                "total_guests": accommodation["total_guests"],
                "single_beds": accommodation["single_beds"],
                "double_beds": accommodation["double_beds"],
                "min_nights": accommodation["min_nights"],
                "price": accommodation["price"],
            },
        }

        return data

    def find_many(self) -> List:
        statement = "SELECT uuid, status, created_at, check_in, check_out, document, accommodation_uuid FROM booking"
        cursor = self.db.cursor()
        cursor.execute(statement)
        results = cursor.fetchall()

        bookings = []

        if len(results) == 0:
            return []

        for booking in results:
            guest_document = booking["document"]
            accommodation_uuid = booking["accommodation_uuid"]

            cursor.execute(
                "SELECT created_at, document, name, surname, country, phone FROM guest WHERE guest.document = ?",
                (guest_document,),
            )
            guest = cursor.fetchone()

            cursor.execute(
                "SELECT uuid, created_at, name, status, total_guests, single_beds, double_beds, min_nights, price FROM accommodation WHERE accommodation.uuid = ?",
                (accommodation_uuid,),
            )
            accommodation = cursor.fetchone()
            data = {
                "uuid": booking["uuid"],
                "status": booking["status"],
                "created_at": booking["created_at"],
                "check_in": booking["check_in"],
                "check_out": booking["check_out"],
                "guest": {
                    "document": guest["document"],
                    "created_at": guest["created_at"],
                    "name": guest["name"],
                    "surname": guest["surname"],
                    "country": guest["country"],
                    "phone": guest["phone"],
                },
                "accommodation": {
                    "uuid": accommodation["uuid"],
                    "created_at": accommodation["created_at"],
                    "name": accommodation["name"],
                    "status": accommodation["status"],
                    "total_guests": accommodation["total_guests"],
                    "single_beds": accommodation["single_beds"],
                    "double_beds": accommodation["double_beds"],
                    "min_nights": accommodation["min_nights"],
                    "price": accommodation["price"],
                },
            }
            bookings.append(data)
        return bookings

    def update(self, uuid: str, booking) -> None:
        statement = "UPDATE booking SET status = ?, check_in = ?, check_out = ?, document = ?,  accommodation_uuid = ? WHERE uuid = ?;"
        cursor = self.db.cursor()
        cursor.execute(
            statement,
            (
                booking["status"],
                booking["check_in"],
                booking["check_out"],
                booking["guest_document"],
                booking["accommodation_uuid"],
                uuid,
            ),
        )
        self.db.commit()

    def delete(self, uuid: str):
        statement = "DELETE FROM booking WHERE uuid = ?"
        cursor = self.db.cursor()
        cursor.execute(statement, (uuid,))
        self.db.commit()
