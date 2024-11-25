from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    event,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)
from sqlalchemy.orm.session import object_session

from app.utils.generate_locator import generate_locator
from app.utils.generate_ulid import generate_ulid


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class UserDB(Base):
    __tablename__ = 'users'
    ulid: Mapped[str] = mapped_column(
        String, primary_key=True, init=False, default_factory=generate_ulid
    )
    email: Mapped[EmailStr] = mapped_column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)


class GuestDB(Base):
    __tablename__ = 'guests'
    ulid: Mapped[str] = mapped_column(
        String, primary_key=True, init=False, default_factory=generate_ulid
    )
    document: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)


amenities_per_accommodation = Table(
    'amenities_per_accommodation',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column(
        'accommodation_ulid',
        ForeignKey('accommodations.ulid', ondelete='CASCADE'),
    ),
    Column('amenitie_id', ForeignKey('amenities.id', ondelete='RESTRICT')),
)


class AccommodationDB(Base):
    __tablename__ = 'accommodations'

    ulid: Mapped[str] = mapped_column(
        String, primary_key=True, init=False, default_factory=generate_ulid
    )
    name: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    status: Mapped[str] = mapped_column(String, nullable=False)
    total_guests: Mapped[int] = mapped_column(Integer, nullable=False)
    single_beds: Mapped[int] = mapped_column(Integer, nullable=False)
    double_beds: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    amenities: Mapped[list['AmenitieDB']] = relationship(
        secondary=amenities_per_accommodation, default=[], init=False
    )


class AmenitieDB(Base):
    __tablename__ = 'amenities'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )
    name: Mapped[str] = mapped_column(String, index=True)


class BookingDB(Base):
    __tablename__ = 'bookings'

    ulid: Mapped[str] = mapped_column(
        String, primary_key=True, init=False, default_factory=generate_ulid
    )
    locator: Mapped[str] = mapped_column(
        String, index=True, unique=True, init=False, default=generate_locator
    )
    status: Mapped[str] = mapped_column(String, nullable=False)
    check_in: Mapped[datetime] = mapped_column(
        DateTime, index=True, nullable=False
    )
    check_out: Mapped[datetime] = mapped_column(
        DateTime, index=True, nullable=False
    )
    budget: Mapped[float] = mapped_column(Float, nullable=False)
    guest: Mapped['GuestDB'] = relationship()
    guest_ulid: Mapped[str] = mapped_column(
        String, ForeignKey('guests.ulid', ondelete='RESTRICT')
    )
    accommodation: Mapped['AccommodationDB'] = relationship()
    accommodation_ulid: Mapped[str] = mapped_column(
        String,
        ForeignKey('accommodations.ulid', ondelete='RESTRICT'),
    )


@event.listens_for(GuestDB, 'before_delete')
def prevent_delete_of_guest(mapper, connection, target):
    session = object_session(target)

    if not session:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='Cannot get Session, check database connection',
        )

    if (
        session.query(BookingDB)
        .filter(BookingDB.guest_ulid == target.ulid)
        .count()
        > 0
    ):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=f"""Cannot delete Guest {target.ulid} because it is
            referenced in bookings.""",
        )


@event.listens_for(AccommodationDB, 'before_delete')
def prevent_delete_of_accommodation(mapper, connection, target):
    session = object_session(target)

    if not session:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='Cannot get Session, check database connection',
        )
    if (
        session.query(BookingDB)
        .filter(BookingDB.accommodation_ulid == target.ulid)
        .count()
        > 0
    ):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=f"""Cannot delete Accommodation {target.ulid} because it is
            referenced in bookings.""",
        )
