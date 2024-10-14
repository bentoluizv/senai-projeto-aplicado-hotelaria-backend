from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.db import get_database_session
from app.database.repositories.BookingRepository import BookingRepository


class RepositoryFactory:
    session: Session

    def __init__(
        self, session: Annotated[Session, Depends(get_database_session)]
    ) -> None:
        self.session = session

    def create_booking_respository(self):
        return BookingRepository(self.session)
