from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)

from app.schemas.Booking import Status
from app.schemas.User import Role


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class UserDB(Base):
    __tablename__ = 'users'
    ulid: Mapped[str] = mapped_column(String, primary_key=True)
    email: Mapped[EmailStr] = mapped_column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(String)
    role: Mapped[Role] = mapped_column(Enum(Role))


class GuestDB(Base):
    __tablename__ = 'guests'
    ulid: Mapped[str] = mapped_column(String, primary_key=True)
    document: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)
    surname: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)


amenities_per_accommodation = Table(
    'amenities_per_accommodation',
    Base.metadata,
    Column(
        'accommodation_ulid',
        ForeignKey('accommodations.ulid', ondelete='CASCADE'),
    ),
    Column('amenitie_id', ForeignKey('amenities.id', ondelete='CASCADE')),
)


class AccommodationDB(Base):
    __tablename__ = 'accommodations'

    ulid: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    status: Mapped[str] = mapped_column(String)
    total_guests: Mapped[int] = mapped_column(Integer)
    single_beds: Mapped[int] = mapped_column(Integer)
    double_beds: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)
    amenities: Mapped[list['AmenitieDB']] = relationship(
        secondary=amenities_per_accommodation
    )


class AmenitieDB(Base):
    __tablename__ = 'amenities'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )
    name: Mapped[str] = mapped_column(String, unique=True, index=True)


class BookingDB(Base):
    __tablename__ = 'bookings'

    ulid: Mapped[str] = mapped_column(String, primary_key=True)
    status: Mapped[Status] = mapped_column(
        Enum(Status), default=Status.BOOKED, init=False
    )
    check_in: Mapped[datetime] = mapped_column(DateTime, index=True)
    check_out: Mapped[datetime] = mapped_column(DateTime, index=True)
    budget: Mapped[float] = mapped_column(Float)
    guest: Mapped['GuestDB'] = relationship()
    guest_ulid: Mapped[str] = mapped_column(
        String, ForeignKey('guests.ulid', ondelete='RESTRICT'), init=False
    )
    accommodation: Mapped['AccommodationDB'] = relationship()
    accommodation_ulid: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('accommodations.ulid', ondelete='RESTRICT'),
        init=False,
    )
