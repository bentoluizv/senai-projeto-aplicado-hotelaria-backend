# pylint: disable=line-too-long

"""Data Access for Guests"""

from sqlite3 import Connection

from app.domain.Guests import Guest


class GuestDAO:
    """Guest DAO is a abstraction for database operations"""

    def __init__(self, db: Connection):
        self.db = db

    def count(self):
        """counts all records"""
        cursor = self.db.cursor()
        count = cursor.execute('SELECT COUNT(*) FROM guest').fetchone().get('COUNT(*)')
        return count

    def insert(self, guest: Guest):
        """creates a new register"""
        params = guest.toObj()
        cursor = self.db.cursor()
        cursor.execute(
            'INSERT INTO guest (document, created_at, name, surname, country, phone) VALUES (:document, :created_at, :name, :surname, :country, :phone);'
            , params)

    def select(self, document) -> Guest | None:
        cursor = self.db.cursor()
        cursor.execute('SELECT document, created_at, name, surname, country, phone FROM guest WHERE guest.document = ?;',  (document,))
        response = cursor.fetchone()

        if response is None:
            return

        guest = Guest(response['document'], response['name'], response['surname'], response['phone'], response['created_at'])
        return guest

    def select_many(self) -> list[Guest]:
        """searches for all registered values"""
        cursor = self.db.cursor()
        cursor.execute('SELECT document, created_at, name, surname, country, phone FROM guest;')
        response = cursor.fetchall()

        if len(response) < 1:
            return response

        guests = [ Guest(guest['document'], guest['name'], guest['surname'], guest['phone'], guest['created_at']) for guest in response ]

        return guests


    def update(self, guest: Guest):
        """updates a record in the table as a whole. params must have the document of the data to be updated as well as all the entity values in the table"""
        params = guest.toObj()
        cursor = self.db.cursor()
        cursor.execute('UPDATE guest SET name = :name, surname = :surname, country = :country, phone = :phone WHERE document = :document;', params)

    def delete(self, document):
        """delete a record based on its document, params -> { document: str }"""
        cursor = self.db.cursor()
        cursor.execute('DELETE FROM guest WHERE document = ?', (document,))
