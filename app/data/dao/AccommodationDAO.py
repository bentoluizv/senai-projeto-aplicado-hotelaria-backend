from sqlite3 import Connection
from typing import List

import click


class AccommodationDAO:
    def __init__(self, db: Connection):
        self.db = db


    def count(self):
        cursor = self.db.cursor()
        count = cursor.execute('SELECT COUNT(*) FROM accommodation').fetchone().get('COUNT(*)')
        return count


    def insert(self, accommodation) -> None:
        cursor = self.db.cursor()
        cursor.execute('INSERT INTO accommodation (uuid, created_at, name, status, total_guests, single_beds, double_beds, min_nights, price) VALUES (:uuid, :created_at, :name, :status, :total_guests, :single_beds, :double_beds, :min_nights, :price);', accommodation)

        for amenitie in accommodation['amenities']:
            cursor.execute('SELECT id FROM amenities WHERE amenitie = ?',  (amenitie, ))
            amenitie_id = cursor.fetchone()['id']
            cursor.execute('INSERT INTO amenities_per_accommodation (accommodation_uuid, amenitie_id) VALUES (?, ?)', (accommodation['uuid'], amenitie_id))

        self.db.commit()


    def find(self, property: str, value: str):
        statement = f'SELECT a.uuid, a.created_at, a.name, a.status, a.total_guests, a.single_beds, a.double_beds, a.min_nights, a.price, GROUP_CONCAT(am.amenitie) AS amenities FROM accommodation AS a JOIN amenities_per_accommodation AS apa ON a.uuid = apa.accommodation_uuid JOIN amenities AS am ON apa.amenitie_id = am.id WHERE a.{property} = ? GROUP BY a.uuid;'
        cursor = self.db.cursor()
        cursor.execute(statement,  (value,))
        result = cursor.fetchone()

        if result is None:
            return

        return result

    def find_many(self) -> List:
        statement = 'SELECT a.uuid, a.created_at, a.name, a.status, a.total_guests, a.single_beds, a.double_beds, a.min_nights, a.price, GROUP_CONCAT(am.amenitie) AS amenities FROM accommodation AS a JOIN amenities_per_accommodation AS apa ON a.uuid = apa.accommodation_uuid JOIN amenities AS am ON apa.amenitie_id = am.id GROUP BY a.uuid;'
        cursor = self.db.cursor()
        cursor.execute(statement)
        rows = cursor.fetchall()

        if len(rows) == 0:
            return []
        click.echo(rows)
        return rows


    def update(self, uuid: str, accommodation) -> None:
        statement = 'UPDATE accommodation SET name = ?, status = ?, total_guests = ?, single_beds = ?, double_beds = ?, min_nights = ?, price = ? WHERE uuid = ?;'
        cursor = self.db.cursor()

        cursor.execute(statement, (accommodation['name'], accommodation['status'],  accommodation['total_guests'],  accommodation['single_beds'],accommodation['double_beds'],accommodation['min_nights'],accommodation['price'],  uuid))

        cursor.execute(f'DELETE FROM amenities_per_accommodation WHERE accommodation_uuid = ?', (uuid,))

        for amenitie in accommodation['amenities']:
            cursor.execute('SELECT id FROM amenities WHERE amenitie = ?',  (amenitie, ))
            amenitie_id = cursor.fetchone()['id']
            cursor.execute('INSERT INTO amenities_per_accommodation (accommodation_uuid, amenitie_id) VALUES (?, ?)', (uuid, str(amenitie_id)))

        self.db.commit()


    def delete(self, uuid: str):
        statement = 'DELETE FROM accommodation WHERE uuid = ?'
        cursor = self.db.cursor()
        cursor.execute(statement, (uuid,))
        self.db.commit()
