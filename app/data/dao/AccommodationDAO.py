from sqlite3 import Connection

from app.data.dao.AmenitieDAO import AmenitieDAO
from app.data.dao.schemas.AccommodationSchema import (
    AccommodationCreationalSchema,
    AccommodationDB,
)


class AccommodationDAO:
    def __init__(self, db: Connection):
        self.db = db
        self.amenities_dao = AmenitieDAO(db)

    def count(self) -> int:
        cursor = self.db.cursor()
        cursor = cursor.execute('SELECT COUNT(*) FROM accommodation')
        result = cursor.fetchone()

        return result['COUNT(*)']

    def find_many(self) -> list[AccommodationDB]:
        select_all_statement = """
            SELECT
                a.id,
                a.created_at,
                a.name,
                a.status,
                a.total_guests,
                a.single_beds,
                a.double_beds,
                a.min_nights,
                a.price,
                GROUP_CONCAT(am.name) AS amenities
            FROM accommodation AS a
            LEFT JOIN amenities_per_accommodation AS apa
                ON a.id = apa.accommodation_id
            LEFT JOIN amenities AS am
                ON apa.amenitie_id = am.id
            GROUP BY a.id;
        """

        cursor = self.db.cursor()
        cursor.execute(select_all_statement)
        result = cursor.fetchall()

        if not result:
            return []

        data = []

        for row in result:
            cells = {
                'id': row['id'],
                'created_at': row['created_at'],
                'name': row['name'],
                'status': row['status'],
                'total_guests': row['total_guests'],
                'single_beds': row['single_beds'],
                'double_beds': row['double_beds'],
                'min_nights': row['min_nights'],
                'price': row['price'],
                'amenities': row['amenities'].split(','),
            }

            data.append(cells)

        return [AccommodationDB(**row) for row in data]

    def find(self, id: int) -> AccommodationDB | None:
        select_one_statement = f"""
            SELECT
                a.id,
                a.created_at,
                a.name,
                a.status,
                a.total_guests,
                a.single_beds,
                a.double_beds,
                a.min_nights,
                a.price,
                GROUP_CONCAT(am.name) AS amenities
            FROM accommodation AS a
            LEFT JOIN amenities_per_accommodation AS apa
                ON a.id = apa.accommodation_id
            LEFT JOIN amenities AS am
                ON apa.amenitie_id = am.id
            WHERE a.id = {id}
            GROUP BY a.id;
        """

        cursor = self.db.cursor()
        cursor.execute(select_one_statement)
        result = cursor.fetchone()

        if not result:
            return None

        data = {
            'id': result['id'],
            'created_at': result['created_at'],
            'name': result['name'],
            'status': result['status'],
            'total_guests': result['total_guests'],
            'single_beds': result['single_beds'],
            'double_beds': result['double_beds'],
            'min_nights': result['min_nights'],
            'price': result['price'],
            'amenities': result['amenities'].split(','),
        }

        return AccommodationDB(**data)

    def find_by(
        self, property: str, value: str | int
    ) -> list[AccommodationDB]:
        select_by_property_statement = f"""
            SELECT
                a.id,
                a.created_at,
                a.name,
                a.status,
                a.total_guests,
                a.single_beds,
                a.double_beds,
                a.min_nights,
                a.price,
                GROUP_CONCAT(am.name) AS amenities
            FROM accommodation AS a
            LEFT JOIN amenities_per_accommodation AS apa
                ON a.id = apa.accommodation_id
            LEFT JOIN amenities AS am
                ON apa.amenitie_id = am.id
            WHERE a.{property} = ?
            GROUP BY a.id;
        """

        cursor = self.db.cursor()
        cursor.execute(select_by_property_statement, (value,))
        result = cursor.fetchall()

        if not result:
            return result

        data = []

        for row in result:
            cells = {
                'id': row['id'],
                'created_at': row['created_at'],
                'name': row['name'],
                'status': row['status'],
                'total_guests': row['total_guests'],
                'single_beds': row['single_beds'],
                'double_beds': row['double_beds'],
                'min_nights': row['min_nights'],
                'price': row['price'],
                'amenities': row['amenities'].split(','),
            }

            data.append(cells)

        return [AccommodationDB(**row) for row in data]

    def create(self, accommodation: AccommodationCreationalSchema):
        insert_statement = """
            INSERT
                INTO accommodation (
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
                );
        """

        cursor = self.db.cursor()
        cursor.execute(insert_statement, accommodation.model_dump())

        last_accommodation_id = cursor.lastrowid

        if not last_accommodation_id:
            raise ValueError('Something went wrong!')

        for amenitie in accommodation.amenities:
            exists = self.amenities_dao.find_by_name(amenitie)

            if not exists:
                raise ValueError('Amentie does not exists')

            self.amenities_dao.insert_amenitie_in_accommodation(
                last_accommodation_id, exists.id
            )

        self.db.commit()

    def update(self, accommodation: AccommodationDB) -> None:
        update_accommodation_statement = """
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
            WHERE id = :id;
        """

        cursor = self.db.cursor()
        cursor.execute(
            update_accommodation_statement, accommodation.model_dump()
        )

        for amenitie in accommodation.amenities:
            exists = self.amenities_dao.find_by_name(amenitie)

            if not exists:
                raise ValueError('Amentie does not exists')

            amenities_in_accommodation = (
                self.amenities_dao.list_amenities_from_accommodation(
                    accommodation.id
                )
            )

            if amenitie not in amenities_in_accommodation:
                self.amenities_dao.insert_amenitie_in_accommodation(
                    accommodation_id=accommodation.id, amenitie_id=exists.id
                )

        self.db.commit()

    def delete(self, id: int):
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
