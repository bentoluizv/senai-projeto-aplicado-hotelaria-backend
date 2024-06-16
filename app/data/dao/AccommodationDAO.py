from sqlite3 import Connection

from app.data.database.models.AccommodationModel import AccommodationModel


class AccommodationDAO:
    def __init__(self, db: Connection):
        self.db = db

    def count(self) -> int:
        cursor = self.db.cursor()
        count = cursor.execute("SELECT COUNT(*) FROM accommodation").fetchone()
        return count["COUNT(*)"]

    def insert(self, data: AccommodationModel):
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO accommodation (created_at, name, status, total_guests, single_beds, double_beds, min_nights, price) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
            (
                data["created_at"],
                data["name"],
                data["status"],
                data["total_guests"],
                data["single_beds"],
                data["double_beds"],
                data["min_nights"],
                data["price"],
            ),
        )

        id = cursor.lastrowid

        for amenitie in data["amenities"]:
            cursor.execute("SELECT id FROM amenities WHERE amenitie = ?", (amenitie,))
            amenitie_id = cursor.fetchone()["id"]
            cursor.execute(
                "INSERT INTO amenities_per_accommodation (accommodation_id, amenitie_id) VALUES (?, ?)",
                (id, amenitie_id),
            )

        self.db.commit()

    def findBy(self, property: str, value: str) -> AccommodationModel | None:
        statement = f"SELECT a.id, a.created_at, a.name, a.status, a.total_guests, a.single_beds, a.double_beds, a.min_nights, a.price, GROUP_CONCAT(am.amenitie) AS amenities FROM accommodation AS a LEFT JOIN amenities_per_accommodation AS apa ON a.id = apa.accommodation_id LEFT JOIN amenities AS am ON apa.amenitie_id = am.id WHERE a.{property} = ? GROUP BY a.id;"
        cursor = self.db.cursor()
        cursor.execute(statement, (value,))
        result = cursor.fetchone()

        if not result:
            return None

        return {
            "id": result["id"],
            "name": result["name"],
            "status": result["status"],
            "created_at": result["created_at"],
            "total_guests": result["total_guests"],
            "min_nights": result["min_nights"],
            "single_beds": result["single_beds"],
            "double_beds": result["double_beds"],
            "price": result["price"],
            "amenities": result["amenities"],
        }

    def find_many(self) -> list[AccommodationModel]:
        statement = "SELECT a.id, a.created_at, a.name, a.status, a.total_guests, a.single_beds, a.double_beds, a.min_nights, a.price, GROUP_CONCAT(am.amenitie) AS amenities FROM accommodation AS a LEFT JOIN amenities_per_accommodation AS apa ON a.id = apa.accommodation_id LEFT JOIN amenities AS am ON apa.amenitie_id = am.id GROUP BY a.id;"
        cursor = self.db.cursor()
        cursor.execute(statement)
        result = cursor.fetchall()

        if len(result) == 0:
            return []

        rows: list[AccommodationModel] = [
            {
                "id": row["id"],
                "name": row["name"],
                "status": row["status"],
                "created_at": row["created_at"],
                "total_guests": row["total_guests"],
                "min_nights": row["min_nights"],
                "single_beds": row["single_beds"],
                "double_beds": row["double_beds"],
                "price": row["price"],
                "amenities": row["amenities"],
            }
            for row in result
        ]

        return rows

    def update(self, id: str, accommodation) -> None:
        statement = "UPDATE accommodation SET name = ?, status = ?, total_guests = ?, single_beds = ?, double_beds = ?, min_nights = ?, price = ? WHERE id = ?;"
        cursor = self.db.cursor()

        cursor.execute(
            statement,
            (
                accommodation["name"],
                accommodation["status"],
                accommodation["total_guests"],
                accommodation["single_beds"],
                accommodation["double_beds"],
                accommodation["min_nights"],
                accommodation["price"],
                id,
            ),
        )

        cursor.execute(
            "DELETE FROM amenities_per_accommodation WHERE accommodation_id = ?",
            (id,),
        )

        for amenitie in accommodation["amenities"]:
            cursor.execute("SELECT id FROM amenities WHERE amenitie = ?", (amenitie,))
            amenitie_id = cursor.fetchone()["id"]
            cursor.execute(
                "INSERT INTO amenities_per_accommodation (accommodation_id, amenitie_id) VALUES (?, ?)",
                (id, str(amenitie_id)),
            )

        self.db.commit()

    def delete(self, id: str):
        statement = "DELETE FROM accommodation WHERE id = ?"
        cursor = self.db.cursor()
        cursor.execute(statement, (id,))
        self.db.commit()
