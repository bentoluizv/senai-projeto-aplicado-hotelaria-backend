from sqlalchemy import select
from sqlalchemy.orm import Session
from ulid import ULID

from app.infra.database.models import GuestDB
from app.schemas.Guest import Guest, GuestCreateDTO, GuestUpdateDTO


class GuestRepository:
    session: Session

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, dto: GuestCreateDTO) -> None:
        db_guest = GuestDB(
            ulid=str(ULID()),
            country=dto.country,
            document=dto.document,
            name=dto.name,
            phone=dto.phone,
            surname=dto.surname,
        )

        self.session.add(db_guest)
        self.session.commit()

    def find_by_id(self, ulid: str) -> Guest | None:
        db_guest = self.session.get(GuestDB, ulid)

        if not db_guest:
            return None

        guest = Guest.from_db(db_guest)
        return guest

    def list_all(self, page: int = 1, per_page: int = 10) -> list[Guest]:
        offset = (page - 1) * per_page
        db_guests = self.session.scalars(
            select(GuestDB).limit(per_page).offset(offset)
        ).all()

        guests = [Guest.from_db(db_guest) for db_guest in db_guests]

        return guests

    def update(self, ulid: str, data: GuestUpdateDTO) -> None:
        db_guest = self.session.get(GuestDB, ulid)

        for key, value in data.model_dump().items():
            if value:
                setattr(db_guest, key, value)

        self.session.commit()

    def delete(self, ulid: str):
        db_guest = self.session.get(GuestDB, ulid)

        if not db_guest:
            return None

        self.session.delete(db_guest)
        self.session.commit()
