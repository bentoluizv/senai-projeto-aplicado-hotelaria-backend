from sqlalchemy import func, select
from sqlalchemy.orm import Session
from ulid import ULID

from app.infra.models import GuestDB
from app.schemas.Guest import Guest, GuestCreateDTO, GuestUpdateDTO
from app.schemas.Info import Info
from app.schemas.RepositorySettings import RepositorySettings


class GuestRepository:
    session: Session
    info: Info = Info()
    settings: RepositorySettings = RepositorySettings()

    def __init__(self, session: Session) -> None:
        self.session = session
        self._set_info()

    def _set_info(self):
        total = self.count()
        per_page = self.settings.pagination
        pages = (total + per_page - 1) // per_page
        self.info = Info(count=total, total_pages=pages)

    def count(self) -> int:
        if not self.session.is_active:
            raise Exception('A sessão do banco de dados está inativa.')

        total_accommodation = self.session.scalar(
            select(func.count()).select_from(GuestDB)
        )

        return total_accommodation or 0

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
