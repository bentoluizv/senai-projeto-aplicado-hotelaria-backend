from sqlite3 import Connection


class AmenitieDAO:
    def __init__(self, db: Connection):
        self.db = db

    def count(self):
        cursor = self.db.cursor()
        count = (
            cursor.execute("SELECT COUNT(*) FROM amenities").fetchone().get("COUNT(*)")
        )
        return count

    def insert(self, amenitie) -> None:
        statement = "INSERT INTO amenities (amenitie) VALUES (?);"
        cursor = self.db.cursor()
        cursor.execute(statement, (amenitie,))
        self.db.commit()

    def find(self, name: str):
        statement = "SELECT amenitie FROM amenities WHERE amenities.amenitie = ?;"
        cursor = self.db.cursor()
        cursor.execute(statement, (name,))
        result = cursor.fetchone()

        if result is None:
            return None

        return result

    def find_many(self):
        statement = "SELECT amenitie FROM amenities;"
        cursor = self.db.cursor()
        cursor.execute(statement)
        results = cursor.fetchall()

        if len(results) == 0:
            return []

        return results

    def delete(self, amenitie: str):
        statement = "DELETE FROM amenities WHERE amenitie = ?"
        cursor = self.db.cursor()
        cursor.execute(statement, (amenitie,))
        self.db.commit()
