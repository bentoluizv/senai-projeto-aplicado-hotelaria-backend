from sqlite3 import Connection

from app.schemas.AccommodationSchema import (
    AccommodationDB,
    AccommodationSchema,
)


class AccommodationDAO:
    def __init__(self, db: Connection):
        self.db = db

    def count(self) -> int:
        cursor = self.db.cursor()
        cursor = cursor.execute('SELECT COUNT(*) FROM accommodation')
        result = cursor.fetchone()

        return result['COUNT(*)']

    def find_many(self) -> list[AccommodationDB]:
        statement = """SELECT
                            a.id,
                            a.created_at,
                            a.name,
                            a.status,
                            a.total_guests,
                            a.single_beds,
                            a.double_beds,
                            a.min_nights,
                            a.price,
                            GROUP_CONCAT(am.amenitie) AS amenities
                        FROM accommodation AS a
                            LEFT JOIN amenities_per_accommodation AS apa
                                ON a.id = apa.accommodation_id
                            LEFT JOIN amenities AS am
                                ON apa.amenitie_id = am.id
                            GROUP BY a.id;"""

        cursor = self.db.cursor()
        cursor.execute(statement)
        result = cursor.fetchall()

        if not result:
            return []

        for row in result:
            row['amenities'] = row['amenities'].split(',')

        return [AccommodationDB(**row) for row in result]

    def find(self, id: str) -> AccommodationDB | None:
        statement = f"""SELECT
                            a.id,
                            a.created_at,
                            a.name,
                            a.status,
                            a.total_guests,
                            a.single_beds,
                            a.double_beds,
                            a.min_nights,
                            a.price,
                            GROUP_CONCAT(am.amenitie) AS amenities
                        FROM accommodation AS a
                            LEFT JOIN amenities_per_accommodation AS apa
                                ON a.id = apa.accommodation_id
                            LEFT JOIN amenities AS am
                                ON apa.amenitie_id = am.id
                            WHERE a.id = {id}
                            GROUP BY a.id;"""

        cursor = self.db.cursor()
        cursor.execute(statement)
        result = cursor.fetchone()

        if not result:
            return None

        for row in result:
            row['amenities'] = row['amenities'].split(',')

        return AccommodationDB(**result)

    def find_by(self, property: str, value: str) -> list[AccommodationDB]:
        statement = f"""SELECT
                            a.id,
                            a.created_at,
                            a.name,
                            a.status,
                            a.total_guests,
                            a.single_beds,
                            a.double_beds,
                            a.min_nights,
                            a.price,
                            GROUP_CONCAT(am.amenitie) AS amenities
                        FROM accommodation AS a
                            LEFT JOIN amenities_per_accommodation AS apa
                                ON a.id = apa.accommodation_id
                            LEFT JOIN amenities AS am
                                ON apa.amenitie_id = am.id
                            WHERE a.{property} = {value}
                            GROUP BY a.id;"""

        cursor = self.db.cursor()
        cursor.execute(statement)
        result = cursor.fetchall()

        if not result:
            return result

        for row in result:
            row['amenities'] = row['amenities'].split(',')

        return [AccommodationDB(**row) for row in result]

    def create(self, accommodation: AccommodationSchema):
        statement = """INSERT
                        INTO
                            accommodation (
                                created_at,
                                name,
                                status,
                                total_guests,
                                single_beds,
                                double_beds,
                                min_nights,
                                price
                            )
                        VALUES (
                            :created_at,
                            :name,
                            :status,
                            :total_guests,
                            :single_beds,
                            :double_beds,
                            :min_nights,
                            :price
                        );"""

        cursor = self.db.cursor()
        cursor.execute(statement, accommodation.model_dump())

        last_accommodation_id = cursor.lastrowid

        for amenitie in accommodation.amenities:
            select_amenitie_id_statement = f"""
                    SELECT
                        id
                    FROM
                        amenities
                    WHERE
                        amenitie = {amenitie};
                    """

            cursor.execute(select_amenitie_id_statement)
            existing_amenitie = cursor.fetchone()

            insert_amenitie_statement = f"""
                    INSERT
                        INTO amenities_per_accommodation
                        (
                            accommodation_id,
                            amenitie_id
                        )
                        VALUES
                        (
                            {last_accommodation_id},
                            {existing_amenitie['id']}
                        );
                    """
            cursor.execute(insert_amenitie_statement)

        self.db.commit()

    def update(self, id: str, accommodation: AccommodationSchema) -> None:
        update_accommodatio_statement = f"""
            UPDATE
                accommodation
            SET
                name = :name,
                status = :status,
                total_guests = :total_guests,
                single_beds = :single_beds,
                double_beds = :double_beds,
                min_nights = :min_nights,
                price = :price
            WHERE id = {id};
        """

        cursor = self.db.cursor()
        cursor.execute(
            update_accommodatio_statement, accommodation.model_dump()
        )

        delete_amenities_statement = f"""
            DELETE
                FROM
                    amenities_per_accommodation
                WHERE
                    accommodation_id = {id}
        """

        cursor.execute(delete_amenities_statement)

        for amenitie in accommodation.amenities:
            select_amenitie_id_statement = f"""
                SELECT
                    id
                FROM
                    amenities
                WHERE
                    amenitie = {amenitie}
            """

            cursor.execute(select_amenitie_id_statement)
            result = cursor.fetchone()

            insert_amenitie_statement = f"""
                INSERT
                    INTO
                        amenities_per_accommodation
                        (
                            accommodation_id,
                            amenitie_id
                        )
                    VALUES
                        (
                            {id},
                            {result[id]}
                        )
                """

        cursor.execute(insert_amenitie_statement)
        self.db.commit()

    def delete(self, id: str):
        delete_statement = f"""
            DELETE
                FROM
                    accommodation
                WHERE
                    id = {id}
        """

        cursor = self.db.cursor()
        cursor.execute(delete_statement)
        self.db.commit()
