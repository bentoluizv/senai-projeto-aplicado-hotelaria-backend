from sqlite3 import Connection
from typing import List


class AccommodationDAO:
    def __init__(self, db: Connection):
        self.db = db


    def count(self):
        cursor = self.db.cursor()
        count = cursor.execute('SELECT COUNT(*) FROM accommodation').fetchone().get('COUNT(*)')
        return count


    def insert(self, accommodation) -> None:
        statement = 'INSERT INTO accommodation (uuid, created_at, name, status, total_guests, single_beds, double_beds, min_nights, price) VALUES (:uuid, :created_at, :name, :status, :total_guests, :single_beds, :double_beds, :min_nights, :price);'
        cursor = self.db.cursor()
        cursor.execute(statement, accommodation)
        self.db.commit()


    def find(self, property: str, value: str):
        statement = f'SELECT uuid, created_at, name, status, total_guests, single_beds, double_beds, min_nights, price FROM accommodation WHERE accommodation.{property} = ?;'
        cursor = self.db.cursor()
        cursor.execute(statement,  (value,))
        result = cursor.fetchone()

        if result is None:
            return

        return result

    def find_many(self) -> List:
        statement = 'SELECT uuid, created_at, name, status, total_guests, single_beds, double_beds, min_nights, price FROM accommodation;'
        cursor = self.db.cursor()
        cursor.execute(statement)
        results = cursor.fetchall()

        if len(results) == 0:
            return []

        accommodations: List = [{
            'uuid': result['uuid'],
            'name': result['name'],
            'status': result['status'],
            'total_guests': result['total_guests'],
            'single_beds': result['single_beds'],
            'double_beds': result['double_beds'],
            'min_nights': result['min_nights'],
            'price': result['price'],
            'created_at': result['created_at']
            } for result in results]

        return accommodations


    def update(self, uuid: str, accommodation) -> None:
        statement = 'UPDATE accommodation SET name = ?, status = ?, total_guests = ?, single_beds = ?, double_beds = ?, min_nights = ?, price = ? WHERE uuid = ?;'
        cursor = self.db.cursor()
        cursor.execute(statement, (accommodation['name'], accommodation['status'],  accommodation['total_guests'],  accommodation['single_beds'],accommodation['double_beds'],accommodation['min_nights'],accommodation['price'],  uuid))
        self.db.commit()

    def delete(self, uuid: str):
        statement = 'DELETE FROM accommodation WHERE uuid = ?'
        cursor = self.db.cursor()
        cursor.execute(statement, (uuid,))
        self.db.commit()
