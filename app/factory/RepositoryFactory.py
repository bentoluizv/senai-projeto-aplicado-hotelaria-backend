from sqlalchemy.orm import Session

from app.database.repositories.BookingRepository import BookingRepository


class RepositoryFactory:
    session: Session

    def __init__(self, session: Session) -> None:
        self.session = session

    def create_booking_respository(self):
        return BookingRepository(self.session)
