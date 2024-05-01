# pylint: disable=line-too-long

"""Data Access for Guests"""

from sqlite3 import Connection
from typing import Any


class GuestDAO:
    """Guest DAO is a abstraction for database operations"""

    def __init__(self, db: Connection):
        self.db = db

    def find(self, params: dict[str, str]):
        """find searches for a value according to its uuid, params -> { uuid: str }"""
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM guest WHERE uuid = :uuid;',  params)
        res = cursor.fetchone()
        cursor.close()
        return res

    def find_many(self):
        """find many searches for all registered values"""
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM guest;')
        res = cursor.fetchall()
        cursor.close()
        return res

    def update(self, params: dict[str, Any]) -> None:
        """updates a record in the table as a whole. params must have the uuid of the data to be updated as well as all the entity values in the table"""
        cursor = self.db.cursor()
        cursor.execute('UPDATE accommodation SET name = :name, surname = :surname, country = :country WHERE uuid = :uuid', params)
        cursor.close()

    def delete(self, params: dict[str, str]):
        """delete a record based on its uuid, params -> { uuid: str }"""
        cursor = self.db.cursor()
        cursor.execute('DELETE FROM guest WHERE uuid = :uuid', params)
        cursor.close()
