from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Uuid,
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


class GuestDB(Base):
    __tablename__ = 'guest'
    uuid: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    document: Mapped[str] = mapped_column(String, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    name: Mapped[str] = mapped_column(String)
    surname: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)


amenities_per_accommodation = Table(
    'amenities_per_accommodation',
    Base.metadata,
    Column(
        'accommodation_id', ForeignKey('accommodation.id', ondelete='CASCADE')
    ),
    Column('amenitie_id', ForeignKey('amenitie.id', ondelete='CASCADE')),
)


class AccommodationDB(Base):
    __tablename__ = 'accommodation'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime)
    name: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    total_guests: Mapped[int] = mapped_column(Integer)
    single_beds: Mapped[int] = mapped_column(Integer)
    double_beds: Mapped[int] = mapped_column(Integer)
    min_nights: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Float)
    amenities: Mapped[list['AmenitieDB']] = relationship(
        secondary=amenities_per_accommodation
    )


class AmenitieDB(Base):
    __tablename__ = 'amenitie'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )
    name: Mapped[str] = mapped_column(String)


class BookingDB(Base):
    __tablename__ = 'booking'

    uuid: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    locator: Mapped[str] = mapped_column(String, unique=True)
    status: Mapped[str] = mapped_column(String)
    check_in: Mapped[str] = mapped_column(DateTime)
    check_out: Mapped[datetime] = mapped_column(DateTime)
    budget: Mapped[int] = mapped_column(Float)
    guest_document: Mapped[str] = mapped_column(
        String, ForeignKey('guest.document', ondelete='RESTRICT')
    )
    accommodation_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('accommodation.id', ondelete='RESTRICT')
    )
    guest: Mapped['GuestDB'] = relationship()
    accommodation: Mapped['AccommodationDB'] = relationship()
