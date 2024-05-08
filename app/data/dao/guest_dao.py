# pylint: disable=line-too-long

"""Data Access for Guests"""

from sqlite3 import Connection


class GuestDAO:
    """Guest DAO is a abstraction for database operations"""

    def __init__(self, db: Connection):
        self.db = db

    def count(self):
        """counts all records"""
        cursor = self.db.cursor()
        res = cursor.execute('SELECT COUNT(*) FROM guest').fetchone()
        return res

    def insert(self, params):
        """creates a new register"""
        cursor = self.db.cursor()
        cursor.execute('INSERT INTO guest (uuid, created_at, name, surname, country) VALUES (:uuid, :created_at, :name, :surname, :country);', params)
        if len(params['phones']) > 0:
            for phone in params['phones']:
                cursor.execute('INSERT INTO phones_per_guest (guest_uuid, phone) VALUES (?, ?);', (params['uuid'], phone))

    def select(self, params):
        """searches for a value according to its uuid, params -> { uuid: str }"""
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM guest WHERE uuid = :uuid;',  params)
        res = cursor.fetchone()
        return res

    def select_many(self):
        """searches for all registered values"""
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM guest;')
        res = cursor.fetchall()
        return res

    def update(self, params):
        """updates a record in the table as a whole. params must have the uuid of the data to be updated as well as all the entity values in the table"""
        cursor = self.db.cursor()
        cursor.execute('UPDATE guest SET name = :name, surname = :surname, country = :country WHERE uuid = :uuid;', params)

    def delete(self, params):
        """delete a record based on its uuid, params -> { uuid: str }"""
        cursor = self.db.cursor()
        cursor.execute('DELETE FROM guest WHERE uuid = :uuid', params)
