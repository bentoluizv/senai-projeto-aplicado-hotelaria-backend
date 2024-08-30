from sqlalchemy.orm import Session

from app.schemas.Booking import BookingUpdateDTO


def update_booking(
    session: Session, id: str, booking_dto: BookingUpdateDTO
): ...


# TODO: Implementar regras para atualizar uma reserva.
