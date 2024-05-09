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
        cursor.execute(
            'INSERT INTO guest (document, created_at, name, surname, country) VALUES (:document, :created_at, :name, :surname, :country);', params)
        cursor.execute(
            'INSERT INTO phones_per_guest (document, phone) VALUES (?, ?);',
            (params['document'], params['phone']))

    def select(self, params):
        """searches for a value according to its document, params -> { document: str }"""
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM guest WHERE document = :document;',  params)
        res = cursor.fetchone()
        return res

    def select_many(self):
        """searches for all registered values"""
        cursor = self.db.cursor()
        cursor.execute('SELECT guest.document, guest.created_at, guest.name, guest.surname, guest.country, phones_per_guest.phone FROM guest JOIN phones_per_guest ON guest.document = phones_per_guest.document;')
        res = cursor.fetchall()
        return res

    def update(self, params):
        """updates a record in the table as a whole. params must have the document of the data to be updated as well as all the entity values in the table"""
        cursor = self.db.cursor()
        cursor.execute('UPDATE guest SET name = :name, surname = :surname, country = :country WHERE document = :document;', params)

    def delete(self, params):
        """delete a record based on its document, params -> { document: str }"""
        cursor = self.db.cursor()
        cursor.execute('DELETE FROM guest WHERE document = :document', params)
