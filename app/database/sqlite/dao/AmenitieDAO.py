from sqlite3 import Connection

from app.database.schemas.AmenitieSchema import AmenitieDB


class AmenitieDAO:
    def __init__(self, db: Connection):
        self.db = db

    def count(self) -> int:
        cursor = self.db.cursor()
        cursor = cursor.execute('SELECT COUNT(*) FROM amenities')
        result = cursor.fetchone()

        return result['COUNT(*)']

    def find_many(self) -> list[AmenitieDB]:
        select_all_statement = """
            SELECT
                id,
                name
            FROM
                amenities;
        """

        cursor = self.db.cursor()
        cursor.execute(select_all_statement)
        result = cursor.fetchall()

        return [AmenitieDB(**row) for row in result]

    def find(self, id: str) -> AmenitieDB | None:
        select_by_id_statement = """
            SELECT
                id,
                name
            FROM
                amenities
            WHERE
                amenities.id = ?;
        """

        cursor = self.db.cursor()
        cursor.execute(select_by_id_statement, (id,))
        result = cursor.fetchone()

        if not result:
            return None

        return AmenitieDB(**result)

    def find_by_name(self, name: str) -> AmenitieDB:
        select_by_property_statement = """
            SELECT
                id,
                name
            FROM
                amenities
            WHERE
                amenities.name = ?;
        """

        cursor = self.db.cursor()
        cursor.execute(select_by_property_statement, (name,))
        result = cursor.fetchone()

        return AmenitieDB(**result)

    def create(self, name: str):
        create_statement = """
            INSERT
                INTO amenities (
                    name
                )
                VALUES (
                    :name
                );
        """

        cursor = self.db.cursor()
        cursor.execute(create_statement, (name,))
        self.db.commit()

    def delete(self, id: str):
        delete_statement = """
            DELETE
                FROM
                    amenities
                WHERE
                    id = ?
        """

        cursor = self.db.cursor()
        cursor.execute(delete_statement, (id,))
        self.db.commit()

    def list_amenities_from_accommodation(
        self, accommodation_id: int
    ) -> list[AmenitieDB]:
        select_amenities_from_accommodation = """
            SELECT
                a.id,
                a.name
            FROM
                amenities AS a
            JOIN amenities_per_accommodation AS apa
                ON a.id = apa.amenitie_id
            WHERE
                apa.accommodation_id = ?;

        """

        cursor = self.db.cursor()
        cursor.execute(
            select_amenities_from_accommodation, (accommodation_id,)
        )
        result = cursor.fetchall()

        return [AmenitieDB(**amenitie) for amenitie in result]

    def delete_amenitie_from_accommodation(
        self, accommodation_id: int, amenitie_id: int
    ):
        delete_amenitie_from_accommodation = """
            DELETE
                FROM
                    amenities_per_accommodation
                WHERE
                    accommodation_id = ?
                AND
                    amenitie_id = ?;

        """

        cursor = self.db.cursor()
        cursor.execute(
            delete_amenitie_from_accommodation, (accommodation_id, amenitie_id)
        )

        self.db.commit()

    def insert_amenitie_in_accommodation(
        self, accommodation_id: int, amenitie_id: int
    ):
        cursor = self.db.cursor()

        insert_amenitie_in_accommodation = """
            INSERT
                INTO amenities_per_accommodation
                    (
                    accommodation_id,
                    amenitie_id
                    )
                VALUES
                    (
                    ?,
                    ?
                    );
        """
        cursor.execute(
            insert_amenitie_in_accommodation,
            (
                accommodation_id,
                amenitie_id,
            ),
        )

        self.db.commit()
