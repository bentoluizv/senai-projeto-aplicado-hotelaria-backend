from sqlite3 import Connection
from typing import TypedDict


class CreationalInputData(TypedDict):
    uuid: str
    created_at: str
    status: str
    check_in: str
    check_out: str
    guest_document: str
    accommodation_id: str


class BookingDAO:
    def __init__(self, db: Connection):
        self.db = db

    def count(self):
        cursor = self.db.cursor()
        count = (
            cursor.execute("SELECT COUNT(*) FROM booking").fetchone().get("COUNT(*)")
        )
        return count

    def insert(self, data: CreationalInputData):
        statement = "INSERT INTO booking (uuid, created_at, status, check_in, check_out, document, accommodation_id) VALUES (?, ?, ?, ?, ?, ?, ?);"
        cursor = self.db.cursor()
        cursor.execute(
            statement,
            (
                data["uuid"],
                data["created_at"],
                data["status"],
                data["check_in"],
                data["check_out"],
                data["guest_document"],
                data["accommodation_id"],
            ),
        )
        self.db.commit()

    def findBy(self, property: str, value: str):
        cursor = self.db.cursor()
        cursor.execute(
            f"SELECT uuid, status, created_at, check_in, check_out, document, accommodation_id FROM booking WHERE booking.{property} = ?;",
            (value,),
        )

        booking = cursor.fetchone()

        if booking is None:
            return None

        guest_document = booking["document"]
        accommodation_id = booking["accommodation_id"]

        cursor.execute(
            "SELECT created_at, document, name, surname, country, phone FROM guest WHERE guest.document = ?",
            (guest_document,),
        )
        guest = cursor.fetchone()

        cursor.execute(
            "SELECT a.id, a.created_at, a.name, a.status, a.total_guests, a.single_beds, a.double_beds, a.min_nights, a.price, GROUP_CONCAT(am.amenitie) AS amenities FROM accommodation AS a LEFT JOIN amenities_per_accommodation AS apa ON a.id = apa.accommodation_id LEFT JOIN amenities AS am ON apa.amenitie_id = am.id WHERE a.id = ? GROUP BY a.id;",
            (accommodation_id,),
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
                "id": accommodation["id"],
                "created_at": accommodation["created_at"],
                "name": accommodation["name"],
                "status": accommodation["status"],
                "total_guests": accommodation["total_guests"],
                "single_beds": accommodation["single_beds"],
                "double_beds": accommodation["double_beds"],
                "min_nights": accommodation["min_nights"],
                "price": accommodation["price"],
                "amenities": accommodation["amenities"],
            },
        }
        return data

    def find_many(self):
        statement = "SELECT uuid, status, created_at, check_in, check_out, document, accommodation_id FROM booking"
        cursor = self.db.cursor()
        cursor.execute(statement)
        results = cursor.fetchall()

        bookings = []

        if len(results) == 0:
            return results

        for booking in results:
            guest_document = booking["document"]
            accommodation_id = booking["accommodation_id"]

            guest = cursor.execute(
                "SELECT created_at, document, name, surname, country, phone FROM guest WHERE guest.document = ?",
                (guest_document,),
            ).fetchone()

            accommodation = cursor.execute(
                "SELECT a.id, a.created_at, a.name, a.status, a.total_guests, a.single_beds, a.double_beds, a.min_nights, a.price, GROUP_CONCAT(am.amenitie) AS amenities FROM accommodation AS a LEFT JOIN amenities_per_accommodation AS apa ON a.id = apa.accommodation_id LEFT JOIN amenities AS am ON apa.amenitie_id = am.id WHERE a.id = ? GROUP BY a.id;",
                (accommodation_id,),
            ).fetchone()

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
                    "id": accommodation["id"],
                    "created_at": accommodation["created_at"],
                    "name": accommodation["name"],
                    "status": accommodation["status"],
                    "total_guests": accommodation["total_guests"],
                    "single_beds": accommodation["single_beds"],
                    "double_beds": accommodation["double_beds"],
                    "min_nights": accommodation["min_nights"],
                    "price": accommodation["price"],
                    "amenities": accommodation["amenities"],
                },
            }
            bookings.append(data)
        return bookings

    def update(self, uuid: str, booking):
        statement = "UPDATE booking SET status = ?, check_in = ?, check_out = ?, document = ?,  accommodation_id = ? WHERE uuid = ?;"
        cursor = self.db.cursor()
        cursor.execute(
            statement,
            (
                booking["status"],
                booking["check_in"],
                booking["check_out"],
                booking["guest_document"],
                booking["accommodation_id"],
                uuid,
            ),
        )
        self.db.commit()

    def delete(self, uuid: str):
        statement = "DELETE FROM booking WHERE uuid = ?"
        cursor = self.db.cursor()
        cursor.execute(statement, (uuid,))
        self.db.commit()
