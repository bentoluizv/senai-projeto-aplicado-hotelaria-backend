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
        count = cursor.execute('SELECT COUNT(*) FROM guest').fetchone().get('COUNT(*)')
        return count

    def insert(self, params):
        """creates a new register"""
        cursor = self.db.cursor()
        cursor.execute(
            'INSERT INTO guest (document, created_at, name, surname, country, phone) VALUES (:document, :created_at, :name, :surname, :country, :phone);'
            , params)

    def select(self, document):
        """searches for a value according to its document, params -> { document: str }"""
        cursor = self.db.cursor()
        cursor.execute('SELECT document, created_at, name, surname, country, phone FROM guest WHERE guest.document = ?;',  (document,))
        res = cursor.fetchone()
        return res

    def select_many(self):
        """searches for all registered values"""
        cursor = self.db.cursor()
        cursor.execute('SELECT document, created_at, name, surname, country, phone FROM guest;')
        res = cursor.fetchall()
        return res

    def update(self, params):
        """updates a record in the table as a whole. params must have the document of the data to be updated as well as all the entity values in the table"""
        cursor = self.db.cursor()
        cursor.execute('UPDATE guest SET name = :name, surname = :surname, country = :country, phone = :phone WHERE document = :document;', params)

    def delete(self, document):
        """delete a record based on its document, params -> { document: str }"""
        cursor = self.db.cursor()
        cursor.execute('DELETE FROM guest WHERE document = ?', (document,))
