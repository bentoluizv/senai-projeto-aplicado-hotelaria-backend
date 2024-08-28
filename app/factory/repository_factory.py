from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.data.database.db import get_database_session
from app.data.repositories.AccommodationRepository import (
    AccommodationRepository,
)
from app.data.repositories.AmenitieRepository import AmenitieRepository
from app.data.repositories.BookingRepository import BookingRepository
from app.data.repositories.GuestRepository import GuestRepository


class RepositoryFactory:
    session: Session

    def __init__(
        self, session: Annotated[Session, Depends(get_database_session)]
    ):
        self.session = session

    def create_guest_repository(self) -> GuestRepository:
        return GuestRepository(self.session)

    def create_accommodation_repository(self) -> AccommodationRepository:
        return AccommodationRepository(self.session)

    def create_booking_repository(self) -> BookingRepository:
        return BookingRepository(self.session)

    def create_amenitie_repository(self) -> AmenitieRepository:
        return AmenitieRepository(self.session)
