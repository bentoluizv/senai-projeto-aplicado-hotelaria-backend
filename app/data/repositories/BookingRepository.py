from app.data.dao.BookingDAO import BookingDAO, CreationalBookingData
from app.entity.Booking import Booking
from app.errors.AlreadyExists import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError


class BookingRepository:
    def __init__(self, dao: BookingDAO):
        self.dao = dao

    def count(self) -> int:
        return self.dao.count()

    def insert(self, booking: Booking):
        exists = self.dao.findBy("uuid", booking.uuid)

        if exists:
            raise AlreadyExistsError()

        booking_dict = booking.to_dict()

        data: CreationalBookingData = {
            "status": booking_dict["status"],
            "check_in": booking_dict["check_in"],
            "created_at": booking_dict["created_at"],
            "uuid": booking_dict["uuid"],
            "check_out": booking_dict["check_out"],
            "guest_document": booking_dict["guest"]["document"],
            "accommodation_id": booking_dict["accommodation"]["id"],
        }

        self.dao.insert(data)

    def findBy(self, property: str, value: str) -> Booking:
        exists = self.dao.findBy(property, value)

        if not exists:
            raise NotFoundError()

        booking = Booking.from_dict(exists)

        return booking

    def find_many(self) -> list[Booking]:
        existing = self.dao.find_many()

        if len(existing) == 0:
            return []

        bookings = []

        for accommodation_data in existing:
            booking = Booking.from_dict(accommodation_data)
            bookings.append(booking)

        return bookings

    def update(self, booking: Booking):
        exists = self.dao.findBy("uuid", booking.uuid)

        if not exists:
            raise NotFoundError()

        self.dao.update(
            booking.uuid,
            {
                "status": booking.status,
                "check_in": booking.check_in,
                "check_out": booking.check_out,
                "guest_document": booking.guest.document,
                "accommodation_id": str(booking.accommodation.id),
            },
        )

    def delete(self, uuid: str):
        exists = self.dao.findBy("uuid", uuid)

        if not exists:
            raise NotFoundError()

        self.dao.delete(uuid)
