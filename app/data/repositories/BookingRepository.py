from typing import List

from app.data.dao.BookingDAO import BookingDAO, BookingDTO
from app.entity.Booking import Booking


class BookingRepository:
    def __init__(self, dao: BookingDAO):
        self.dao  = dao


    def count(self) -> int:
        return self.dao.count()


    def insert(self, booking: Booking):
        exists  = self.dao.findBy('uuid',booking.uuid)

        if exists:
            raise ValueError(f'Reserva com id {booking.uuid} já está cadastrado')

        booking_dict = booking.to_dict()

        booking_dto: BookingDTO = {
            'status': booking_dict['status'],
            'check_in': booking_dict['check_in'],
            'created_at': booking_dict['created_at'],
            'uuid': booking_dict['uuid'],
            'check_out': booking_dict['check_out'],
            'guest_document': booking_dict['guest']['document'],
            'accommodation_uuid': booking_dict['accommodation']['uuid'],
        }

        self.dao.insert(booking_dto)


    def find(self, uuid: str):
        exists = self.dao.findBy('uuid',uuid)

        if not exists:
            raise ValueError(f'Reserva com  id {uuid} não está cadastrado')

        booking = Booking.from_dict(exists)

        return booking


    def find_many(self) -> List[Booking]:
        existing = self.dao.find_many()

        if len(existing) == 0:
            return []

        guests: List[Booking] = []

        for unknown in existing:
            guest = Booking.from_dict(unknown)
            guests.append(guest)

        return guests


    def update(self, booking: Booking):
        exists = self.dao.findBy('uuid',booking.uuid)

        if not exists:
            raise ValueError(f'A Reserva com o id {booking.uuid} não está cadastrada')

        self.dao.update(
            booking.uuid,
            {
                'status': booking.status,
                'check_in': booking.check_in,
                'check_out': booking.check_out,
                'guest_document':   booking.guest.document,
                'accommodation_uuid': booking.accommodation.uuid
            })


    def delete(self, uuid: str):
        exists = self.dao.findBy('uuid',uuid)

        if not exists:
            raise ValueError(f'Reserva com o id {uuid} não está cadastrada')

        self.dao.delete(uuid)