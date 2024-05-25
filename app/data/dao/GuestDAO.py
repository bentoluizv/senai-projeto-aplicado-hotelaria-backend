from sqlite3 import Connection
from typing import List

from app.entity.Guests import GuestDTO, UpdatableGuest


class GuestDAO:
    def __init__(self, db: Connection):
        self.db = db


    def count(self):
        cursor = self.db.cursor()
        count = cursor.execute('SELECT COUNT(*) FROM guest').fetchone().get('COUNT(*)')
        return count


    def insert(self, guest: GuestDTO) -> None:
        statement = 'INSERT INTO guest (document, created_at, name, surname, country, phone) VALUES (:document, :created_at, :name, :surname, :country, :phone);'
        cursor = self.db.cursor()
        cursor.execute(statement, guest)
        self.db.commit()


    def find(self, document: str) -> GuestDTO | None:
        statement = 'SELECT document, created_at, name, surname, country, phone FROM guest WHERE guest.document = ?;'
        cursor = self.db.cursor()
        cursor.execute(statement,  (document,))
        result = cursor.fetchone()

        if result is None:
            return

        return {
            'document': result['document'],
            'name': result['name'],
            'surname': result['surname'],
            'phone': result['phone'],
            'country': result['country'],
            'created_at': result['created_at']
            }


    def find_many(self) -> List[GuestDTO]:
        statement = 'SELECT document, created_at, name, surname, country, phone FROM guest;'
        cursor = self.db.cursor()
        cursor.execute(statement)
        results = cursor.fetchall()

        if len(results) == 0:
            return []

        guests: List[GuestDTO] = [{
            'document': result['document'],
            'name': result['name'],
            'surname': result['surname'],
            'phone': result['phone'],
            'country': result['country'],
            'created_at': result['created_at']
            } for result in results]

        return guests


    def update(self, document: str, guest: UpdatableGuest) -> None:
        statement = 'UPDATE guest SET name = ?, surname = ?, country = ?, phone = ? WHERE document = ?;'
        cursor = self.db.cursor()
        cursor.execute(statement, (guest['name'], guest['surname'],  guest['country'],  guest['phone'],  document))
        self.db.commit()

    def delete(self, document: str):
        statement = 'DELETE FROM guest WHERE document = ?'
        cursor = self.db.cursor()
        cursor.execute(statement, (document,))
        self.db.commit()
