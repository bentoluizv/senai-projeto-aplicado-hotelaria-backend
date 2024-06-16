from sqlite3 import Connection

from app.data.database.models.GuestModel import GuestModel


class GuestDAO:
    def __init__(self, db: Connection):
        self.db = db

    def count(self) -> int:
        cursor = self.db.cursor()
        row = cursor.execute("SELECT COUNT(*) FROM guest").fetchone()
        return row["COUNT(*)"]

    def insert(self, guest: GuestModel) -> None:
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO guest (document, created_at, name, surname, country, phone) VALUES (?, ?, ?, ?, ?, ?);",
            (
                guest["document"],
                guest["created_at"],
                guest["name"],
                guest["surname"],
                guest["country"],
                guest["phone"],
            ),
        )
        self.db.commit()

    def findBy(self, property: str, value: str) -> GuestModel | None:
        statement = f"SELECT document, created_at, name, surname, country, phone FROM guest WHERE guest.{property} = ?;"
        cursor = self.db.cursor()
        cursor.execute(statement, (value,))
        result = cursor.fetchone()

        if result is None:
            return None

        return {
            "document": result["document"],
            "created_at": result["created_at"],
            "name": result["name"],
            "surname": result["surname"],
            "country": result["country"],
            "phone": result["phone"],
        }

    def find_many(self) -> list[GuestModel]:
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT document, created_at, name, surname, country, phone FROM guest;"
        )
        results = cursor.fetchall()

        if len(results) == 0:
            return []

        guests: list[GuestModel] = [
            {
                "document": result["document"],
                "name": result["name"],
                "surname": result["surname"],
                "phone": result["phone"],
                "country": result["country"],
                "created_at": result["created_at"],
            }
            for result in results
        ]

        return guests

    def update(self, document: str, guest) -> None:
        cursor = self.db.cursor()
        cursor.execute(
            "UPDATE guest SET name = ?, surname = ?, country = ?, phone = ? WHERE document = ?;",
            (
                guest["name"],
                guest["surname"],
                guest["country"],
                guest["phone"],
                document,
            ),
        )
        self.db.commit()

    def delete(self, document: str):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM guest WHERE document = ?", (document,))
        self.db.commit()
