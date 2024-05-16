# pylint: disable=line-too-long

"""Data Access for Accommodations"""

from curses import raw
from sqlite3 import Connection

from app.domain.Accomodation import Accommodation


class AccommodationDAO:
    def __init__(self, db: Connection):
        self.db = db

    def count(self)  -> int:
        """counts all records"""
        cursor = self.db.cursor()
        count = cursor.execute('SELECT COUNT(*) FROM accommodation').fetchone().get('COUNT(*)')
        return count

    def find_many(self) -> list[Accommodation]:
        """find many searches for all registered values"""
        cursor = self.db.cursor()
        cursor.execute('SELECT uuid, created_at, status, name, total_guests, single_beds, double_beds, min_nights, price FROM accommodation;')
        result = cursor.fetchall()
        accommodations =  list(map(lambda x: Accommodation(x), result))
        return accommodations


    def find(self, uuid):
        """find searches for a value according to its uuid, params -> { uuid: str }"""
        cursor = self.db.cursor()
        cursor.execute('SELECT uuid, created_at, status, name, total_guests, single_beds, double_beds, min_nights, price FROM accommodation WHERE uuid = ?',  (uuid,))
        raw_accomoddation = cursor.fetchone()
        if (raw_accomoddation is None):
            return
        accommodation = Accommodation(raw_accomoddation)
        cursor.execute('SELECT am.amenitie FROM amenities_per_accommodation AS ap JOIN amenities AS am ON ap.amenitie_name = am.amenitie WHERE ap.accommodation_uuid = ?;', (uuid,))
        raw_amenities = cursor.fetchall()
        for amenitie in raw_amenities:
            accommodation.add_amenitie(amenitie['amenitie'])
        return accommodation

    def insert(self, accommodation: Accommodation) -> None:
        """creates a new register"""
        accommodation_dto = accommodation.to_dict()
        cursor = self.db.cursor()
        cursor.execute('INSERT INTO accommodation (uuid, created_at, status, name, total_guests, single_beds, double_beds, min_nights, price) VALUES (:uuid, :created_at, :status, :name, :total_guests, :single_beds, :double_beds, :min_nights, :price) RETURNING uuid;', accommodation_dto)
        for amenitie in accommodation.amenities:
            cursor.execute('INSERT INTO amenities_per_accommodation (accommodation_uuid, amenitie_name) VALUES (?, ?)', (accommodation_dto['uuid'], amenitie))

    def update(self, accommodation: Accommodation) -> None:
        """updates a record in the table as a whole. params must have the uuid of the data to be updated as well as all the entity values in the table"""
        accommodation_dto = accommodation.to_dict()
        cursor = self.db.cursor()
        cursor.execute('UPDATE accommodation SET status = :status, name = :name, total_guests = :total_guests, single_beds = :single_beds, double_beds = :double_beds, min_nights = :min_nights, price = :price WHERE uuid = :uuid', accommodation_dto)
        cursor.close()

    def delete(self, uuid):
        """delete a record based on its uuid, params -> { uuid: str }"""
        cursor = self.db.cursor()
        cursor.execute('DELETE FROM accommodation WHERE uuid = ?', (uuid,))
