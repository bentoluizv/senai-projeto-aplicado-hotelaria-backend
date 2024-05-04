
"""Guarantee the invariance of the relationship between application and database."""
from typing import List

from app.domain.booking import Booking


class BookingReposiroty:
    """represents an repository of bookings"""
    def __init__(self, db):
        pass

    def create(self, booking: Booking) -> None:
        """creates a new record in the database"""

    def select(self, uuid) -> Booking:
        """select a record by its uuid"""

    def select_many(self) -> List[Booking]:
        """select all registered records"""

    def update(self, booking: Booking) -> None:
        """updates a record by its uuid"""

    def delete(self, uuid) -> None:
        """deletes a record by its uuid """

