from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.errors.NotFoundError import NotFoundError
from app.infra.database.models import AccommodationDB, BookingDB, GuestDB
from app.schemas.Booking import BookingCreateDTO, BookingUpdateDTO


def register(session: Session, booking_dto: BookingCreateDTO):
    # TODO: Validar se existem outras reservas
    # no periodo de checkin/checkout escolhidos

    existing_guest = session.scalar(
        select(GuestDB).where(GuestDB.document == booking_dto.guest_document)
    )

    if not existing_guest:
        raise NotFoundError(booking_dto.guest_document)

    existing_accommodation = session.scalar(
        select(AccommodationDB).where(
            AccommodationDB.id == booking_dto.accommodation_id
        )
    )

    if not existing_accommodation:
        raise NotFoundError(booking_dto.accommodation_id)

    # TODO: Implementar calculo do custo de acomodação
    # baseado no periodo de estadia (budget)

    new_booking = BookingDB(
        accommodation=existing_accommodation,
        budget=0,
        check_in=booking_dto.check_in,
        check_out=booking_dto.check_out,
        guest=existing_guest,
    )

    session.add(new_booking)

    session.commit()


def list_all(session: Session):
    bookings = tuple(session.scalars(select(BookingDB)).all())

    return bookings


def find_by_id(session: Session, id: str):
    uuid = UUID(id)

    existing_booking = session.get(BookingDB, uuid)

    if not existing_booking:
        raise NotFoundError(uuid)

    return existing_booking


def update(session: Session, id: str, booking_dto: BookingUpdateDTO): ...


# TODO: Implementar regras para atualizar uma reserva.
