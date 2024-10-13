from sqlalchemy.orm import Session

from app.infra.repositories.AccommodationRepository import (
    AccommodationRepository,
)
from app.infra.repositories.AmenitieRepository import AmenitieRepository
from app.infra.repositories.BookingRepository import BookingRepository
from app.infra.repositories.GuestRepository import GuestRepository
from app.infra.repositories.UserRepository import UserRepository


class RepositoryFactory:
    session: Session

    def __init__(self, session: Session) -> None:
        self.session = session

    def create_guest_repository(self):
        return GuestRepository(session=self.session)

    def create_accommodation_repository(self):
        return AccommodationRepository(session=self.session)

    def create_amenitie_repository(self):
        return AmenitieRepository(session=self.session)

    def create_booking_repository(self):
        return BookingRepository(session=self.session)

    def create_user_repository(self):
        return UserRepository(session=self.session)
