from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.database.models import GuestDB
from app.domain.errors.AlreadyExistsError import AlreadyExistsError
from app.domain.errors.NotFoundError import NotFoundError
from app.domain.Guest import Guest, GuestCreateDTO, GuestUpdateDTO


class GuestRepository:
    def __init__(self, database: Session):
        self.database = database

    def list(self):
        db_guests = self.database.scalars(select(GuestDB)).all()
        guests = [Guest.from_database(db_guest) for db_guest in db_guests]

        return guests

    def find_by_id(self, id: UUID):
        db_guest = self.database.get(GuestDB, id)

        if not db_guest:
            raise NotFoundError(id)

        guest = Guest.from_database(db_guest)

        return guest

    def insert(self, data: GuestCreateDTO):
        guest = Guest.create(data)
        exists = self.database.scalar(
            select(GuestDB).where(GuestDB.document == guest.document)
        )

        if exists:
            raise AlreadyExistsError(guest.document)

        db_guest = GuestDB(**guest.model_dump())
        self.database.add(db_guest)
        self.database.commit()

    def update(self, id: UUID, data: GuestUpdateDTO):
        db_guest = self.database.get(GuestDB, id)

        if not db_guest:
            raise NotFoundError(id)

        for key, value in data.model_dump().items():
            if value is not None:
                setattr(db_guest, key, value)

        self.database.commit()

    def delete(self, id: UUID):
        db_guest = self.database.get(GuestDB, id)

        if not db_guest:
            raise NotFoundError(id)

        self.database.delete(db_guest)
