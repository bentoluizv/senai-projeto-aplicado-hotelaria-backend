from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.database.sqlalchemy.models import GuestDB
from app.domain.Guest import Guest
from app.errors.AlreadyExists import AlreadyExistsError
from app.errors.NotFoundError import NotFoundError


class GuestRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_many(self) -> list[Guest]:
        statement = select(GuestDB)
        db_guests = self.session.scalars(statement).all()

        return [Guest(**db_guest.__dict__) for db_guest in db_guests]

    def find(self, document: str) -> Guest:
        db_guest = self.session.get(GuestDB, document)

        if not db_guest:
            raise NotFoundError()

        return Guest(**db_guest.__dict__)

    def find_by_name(self, name: str) -> list[Guest]:
        statement = select(GuestDB).where(GuestDB.name == name)
        db_guests = self.session.scalars(statement).all()

        return [Guest(**db_guest.__dict__) for db_guest in db_guests]

    def create(self, data: Guest) -> None:
        exists = self.session.get(GuestDB, data.document)

        if exists:
            raise AlreadyExistsError()

        guest = GuestDB(**data.model_dump())
        self.session.add(guest)

    def update(self, data: Guest) -> None:
        exists = self.session.get(GuestDB, data.document)

        if not exists:
            raise NotFoundError()

        statement = (
            update(GuestDB)
            .where(GuestDB.document == data.document)
            .values(
                name=data.name,
                surname=data.surname,
                phone=data.phone,
                country=data.country,
            )
        )

        self.session.execute(statement)

    def delete(self, document: str) -> None:
        exists = self.session.get(GuestDB, document)

        if not exists:
            raise NotFoundError()

        self.session.delete(exists)
        self.session.commit()
