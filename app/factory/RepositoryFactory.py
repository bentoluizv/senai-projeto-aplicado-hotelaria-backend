from sqlalchemy.orm import Session

from app.infra.database.repositories.AccommodationRepository import (
    AccommodationRepository,
)
from app.infra.database.repositories.AmenitieRepository import (
    AmenitieRepository,
)
from app.infra.database.repositories.BookingRepository import BookingRepository
from app.infra.database.repositories.GuestRepository import GuestRepository


class RepositoryFactory:
    session: Session

    def __init__(self, session: Session) -> None:
        self.session = session

    def create_guest_repository(self):
        return GuestRepository(self.session)

    def create_accommodation_repository(self):
        return AccommodationRepository(self.session)

    def create_amenitie_repository(self):
        return AmenitieRepository(self.session)

    def create_booking_repository(self):
        return BookingRepository(self.session)
