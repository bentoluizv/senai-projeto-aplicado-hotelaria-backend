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
            #f"SELECT uuid, status, created_at, check_in, check_out, document, accommodation_uuid FROM booking WHERE booking.{property} = ?;",
            #(value,),
            f"SELECT uuid, status, created_at, check_in, check_out, document, accommodation_uuid FROM booking WHERE booking.{property} LIKE ?;",
            (f"{value}%",),
            
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
            "SELECT a.uuid, a.created_at, a.name, a.status, a.total_guests, a.single_beds, a.double_beds, a.min_nights, a.price, GROUP_CONCAT(am.amenitie) AS amenities FROM accommodation AS a LEFT JOIN amenities_per_accommodation AS apa ON a.uuid = apa.accommodation_uuid LEFT JOIN amenities AS am ON apa.amenitie_id = am.id WHERE a.uuid = ? GROUP BY a.uuid;",
            (accommodation_uuid,),
        )
        accommodation = cursor.fetchone()

        bookings = []
        
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
                "amenities": accommodation["amenities"],
            },
        }
        bookings.append(data)
       
        
        print("teste de execução")
        return bookings

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
                "SELECT a.uuid, a.created_at, a.name, a.status, a.total_guests, a.single_beds, a.double_beds, a.min_nights, a.price, GROUP_CONCAT(am.amenitie) AS amenities FROM accommodation AS a LEFT JOIN amenities_per_accommodation AS apa ON a.uuid = apa.accommodation_uuid LEFT JOIN amenities AS am ON apa.amenitie_id = am.id WHERE a.uuid = ? GROUP BY a.uuid;",
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
                    "amenities": accommodation["amenities"],
                },
            }
            bookings.append(data)
        print("teste de execução")
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
