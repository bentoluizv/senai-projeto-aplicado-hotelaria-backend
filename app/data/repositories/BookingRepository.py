from typing import List

from app.data.dao.BookingDAO import BookingDAO, BookingDTO
from app.entity.Booking import Booking
from app.utils.transform import transform


class BookingRepository:
    def __init__(self, dao: BookingDAO):
        self.dao = dao

    def count(self) -> int:
        return self.dao.count()

    def insert(self, booking: Booking):
        exists = self.dao.findBy("uuid", str(booking.uuid))

        if exists:
            raise ValueError(f"Reserva com id {booking.uuid} já está cadastrado")

        booking_dict = booking.to_dict()

        booking_dto: BookingDTO = {
            "status": booking_dict["status"],
            "check_in": booking_dict["check_in"].isoformat(),
            "created_at": booking_dict["created_at"].isoformat(),
            "uuid": str(booking_dict["uuid"]),
            "check_out": booking_dict["check_out"].isoformat(),
            "guest_document": booking_dict["guest"]["document"],
            "accommodation_uuid": str(booking_dict["accommodation"]["uuid"]),
        }

        self.dao.insert(booking_dto)

    def find(self, uuid: str):
        exists = self.dao.findBy("uuid", uuid)

        if not exists:
            raise ValueError(f"Reserva com  id {uuid} não está cadastrado")

        if exists["accommodation"]["amenities"] is not None:
            amenities = exists["accommodation"]["amenities"]
            exists["accommodation"]["amenities"] = amenities.split(",")
        else:
            exists["accommodation"]["amenities"] = []

        booking = Booking.from_dict(transform(exists))

        return booking

    def find_many(self) -> List[Booking]:
        existing = self.dao.find_many()

        if len(existing) == 0:
            return []

        bookings: List[Booking] = []

        for unknown in existing:
            if unknown["accommodation"]["amenities"] is not None:
                amenities = unknown["accommodation"]["amenities"]
                unknown["accommodation"]["amenities"] = amenities.split(",")
            else:
                unknown["accommodation"]["amenities"] = []

            booking = Booking.from_dict(transform(unknown))
            bookings.append(booking)
        return bookings

    def update(self, booking: Booking):
        exists = self.dao.findBy("uuid", str(booking.uuid))

        if not exists:
            raise ValueError(f"A Reserva com o id {booking.uuid} não está cadastrada")

        self.dao.update(
            str(booking.uuid),
            {
                "status": booking.status,
                "check_in": booking.check_in.isoformat(),
                "check_out": booking.check_out.isoformat(),
                "guest_document": booking.guest.document,
                "accommodation_uuid": str(booking.accommodation.uuid),
            },
        )

    def delete(self, uuid: str):
        exists = self.dao.findBy("uuid", uuid)

        if not exists:
            raise ValueError(f"Reserva com o id {uuid} não está cadastrada")

        self.dao.delete(uuid)
