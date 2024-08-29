from datetime import datetime
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Uuid,
    func,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)

from app.utils.generate_locator import generate_locator


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class UserDB(Base):
    __tablename__ = 'users'
    uuid: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    email: Mapped[EmailStr] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)


class GuestDB(Base):
    __tablename__ = 'guests'
    uuid: Mapped[UUID] = mapped_column(
        Uuid, primary_key=True, default_factory=uuid4, init=False
    )
    document: Mapped[str] = mapped_column(String, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), init=False
    )
    name: Mapped[str] = mapped_column(String)
    surname: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)


amenities_per_accommodation = Table(
    'amenities_per_accommodation',
    Base.metadata,
    Column(
        'accommodation_id', ForeignKey('accommodations.id', ondelete='CASCADE')
    ),
    Column('amenitie_id', ForeignKey('amenities.id', ondelete='CASCADE')),
)


class AccommodationDB(Base):
    __tablename__ = 'accommodations'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default_factory=func.now, init=False
    )
    name: Mapped[str] = mapped_column(String, unique=True)
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
    name: Mapped[str] = mapped_column(String)


class BookingDB(Base):
    __tablename__ = 'bookings'

    uuid: Mapped[UUID] = mapped_column(
        Uuid, primary_key=True, default_factory=uuid4, init=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default_factory=func.now, init=False
    )
    locator: Mapped[str] = mapped_column(
        String, unique=True, default_factory=generate_locator, init=False
    )
    status: Mapped[str] = mapped_column(String)
    check_in: Mapped[datetime] = mapped_column(DateTime)
    check_out: Mapped[datetime] = mapped_column(DateTime)
    budget: Mapped[int] = mapped_column(Float)
    guest_document: Mapped[str] = mapped_column(
        String, ForeignKey('guests.document', ondelete='RESTRICT'), init=False
    )
    accommodation_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('accommodations.id', ondelete='RESTRICT'),
        init=False,
    )
    guest: Mapped['GuestDB'] = relationship()
    accommodation: Mapped['AccommodationDB'] = relationship()
