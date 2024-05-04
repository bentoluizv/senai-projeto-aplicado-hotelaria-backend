

"""Guarantee the invariance of the relationship between application and database."""
from typing import List

from app.domain.guest import Guest


class GuestReposiroty:
    """represents an repository of guests"""
    def __init__(self, db):
        pass

    def create(self, guest: Guest) -> None:
        """creates a new record in the database"""

    def select(self, uuid) -> Guest:
        """select a record by its uuid"""

    def select_many(self) -> List[Guest]:
        """select all registered records"""

    def update(self, guest: Guest) -> None:
        """updates a record by its uuid"""

    def delete(self, uuid) -> None:
        """deletes a record by its uuid """

