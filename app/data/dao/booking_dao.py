# pylint: disable=line-too-long

"""Data Access for Booking"""

from sqlite3 import Connection


class BookingDAO:
    """Booking DAO is a abstraction for database operations"""

    def __init__(self, db: Connection):
        self.db = db

    def count(self):
        """counts all records"""
        cursor = self.db.cursor()
        cursor.execute('SELECT COUNT(*) FROM booking')
        cursor.close()

    def insert(self, params):
        """creates a new register"""
        cursor = self.db.cursor()
        cursor.execute('INSERT INTO booking (uuid, status, check_in, check_out, guest_uuid, accommodation_uuid) VALUES (:uuid, :status, :check_in, :check_out :guest_uuid :accommodation_uuid;)', params)
        cursor.close()

    def find(self, params):
        """find searches for a value according to its uuid, params -> { uuid: str }"""
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM booking JOIN guest ON booking.guest_uuid = guest.uuid JOIN accommodation ON booking.accommodation_uuid = accommodation.uuid WHERE booking.uuid = :uuid;', params)
        res = cursor.fetchone()
        cursor.close()
        return res

    def find_many(self):
        """find many searches for all registered values"""
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM booking JOIN guest ON booking.guest_uuid = guest.uuid JOIN accommodation ON booking.accommodation_uuid = accommodation.uuid;')
        res = cursor.fetchall()
        cursor.close()
        return res

    def update(self, params):
        """updates a record in the table as a whole. params must have the uuid of the data to be updated as well as all the entity values in the table"""
        cursor = self.db.cursor()
        cursor.execute('UPDATE booking SET status = :status, name = :name, total_guests = :total_guests, single_beds = :single_beds, double_beds = :double_beds, min_nights = :min_nights WHERE uuid = :uuid', params)
        cursor.close()

    def delete(self, params):
        """delete a record based on its uuid, params -> { uuid: str }"""
        cursor = self.db.cursor()
        cursor.execute('DELETE FROM booking WHERE uuid = :uuid', params)
        cursor.close()
