from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.db import get_database_session
from app.database.repositories.AccommodationRepository import (
    AccommodationRepository,
)
from app.database.repositories.AmenitieRepository import AmenitieRepository
from app.database.repositories.BookingRepository import BookingRepository
from app.database.repositories.GuestRepository import GuestRepository
from app.database.repositories.UserRepository import UserRepository


class RepositoryFactory:
    session: Session

    def __init__(
        self, session: Annotated[Session, Depends(get_database_session)]
    ) -> None:
        self.session = session

    def create_booking_respository(self):
        return BookingRepository(self.session)

    def create_guest_respository(self):
        return GuestRepository(self.session)

    def create_accommodation_respository(self):
        return AccommodationRepository(self.session)

    def create_user_respository(self):
        return UserRepository(self.session)

    def create_amenitie_respository(self):
        return AmenitieRepository(self.session)
