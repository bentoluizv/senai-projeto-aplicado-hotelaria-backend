"""Guarantee the invariance of the relationship between application and database."""
from typing import List
from app.domain.accommodation import Accommodation


class AccommodationRepository:
    """represents an repository of accommodations"""
    def __init__(self, db):
        pass

    def create(self, accommodation: Accommodation) -> None:
        """creates a new record in the database"""

    def select(self, uuid) -> Accommodation:
        """select a record by its uuid"""

    def select_many(self) -> List[Accommodation]:
        """select all registered records"""

    def update(self, accommodation: Accommodation) -> None:
        """updates a record by its uuid"""

    def delete(self, uuid) -> None:
        """deletes a record by its uuid """
