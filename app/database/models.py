from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import (
    Column,
    DateTime,
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


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class UserDB(Base):
    __tablename__ = 'users'
    ulid: Mapped[str] = mapped_column(String, primary_key=True)
    email: Mapped[EmailStr] = mapped_column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)


class GuestDB(Base):
    __tablename__ = 'guests'
    ulid: Mapped[str] = mapped_column(String, primary_key=True)
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
    Column(
        'accommodation_ulid',
        ForeignKey('accommodations.ulid', ondelete='RESTRICT'),
    ),
    Column('amenitie_id', ForeignKey('amenities.id', ondelete='RESTRICT')),
)


class AccommodationDB(Base):
    __tablename__ = 'accommodations'

    ulid: Mapped[str] = mapped_column(String, primary_key=True)
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

    ulid: Mapped[str] = mapped_column(String, primary_key=True)
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
