from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.database.models import GuestDB
from app.entities.Guest import Guest, GuestUpdateDTO


class GuestRepository:
    session: Session

    def __init__(self, session: Session) -> None:
        self.session = session

    def count(self) -> int:
        if not self.session.is_active:
            raise Exception('A sessão do banco de dados está inativa.')

        total_accommodation = self.session.scalar(
            select(func.count()).select_from(GuestDB)
        )

        return total_accommodation or 0

    def create(self, guest: Guest) -> None:
        db_guest = GuestDB(
            country=guest.country,
            document=guest.document,
            name=guest.name,
            phone=guest.phone,
            surname=guest.surname,
        )

        self.session.add(db_guest)
        self.session.commit()

    def find_by_id(self, ulid: str) -> Guest | None:
        db_guest = self.session.get(GuestDB, ulid)

        if not db_guest:
            return None

        guest = Guest.from_db(db_guest)
        return guest

    def find_by_document(self, document: str) -> Guest | None:
        db_guest = self.session.scalar(
            select(GuestDB).where(GuestDB.document == document)
        )

        if not db_guest:
            return None

        guest = Guest.from_db(db_guest)
        return guest

    def list_all(self, page: int = 1, per_page: int = 10) -> list[Guest]:
        offset = (page - 1) * per_page

        db_guests = self.session.scalars(
            select(GuestDB)
            .limit(per_page)
            .offset(offset)
            .order_by(desc(GuestDB.ulid))
        ).all()

        guests = [Guest.from_db(db_guest) for db_guest in db_guests]

        return guests

    def update(self, ulid: str, data: GuestUpdateDTO) -> Guest:
        db_guest = self.session.get_one(GuestDB, ulid)

        for key, value in data.model_dump().items():
            if value:
                setattr(db_guest, key, value)

        self.session.commit()
        self.session.refresh(db_guest)
        guest = Guest.from_db(db_guest)
        return guest

    def delete(self, ulid: str):
        db_guest = self.session.get_one(GuestDB, ulid)

        self.session.delete(db_guest)
        self.session.commit()
