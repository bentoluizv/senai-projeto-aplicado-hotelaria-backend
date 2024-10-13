from datetime import datetime

from sqlalchemy.orm import Session

from app.database.models import (
    AccommodationDB,
    AmenitieDB,
    BookingDB,
    GuestDB,
    Role,
    UserDB,
)

users = [
    UserDB(
        ulid='01USER3ULID',
        email='johndoe@example.com',
        password='hashed_password3',
        role=Role.USER,
    ),
    UserDB(
        ulid='01USER4ULID',
        email='admin2@example.com',
        password='hashed_password4',
        role=Role.ADMIN,
    ),
    UserDB(
        ulid='01USER5ULID',
        email='guest@example.com',
        password='hashed_password5',
        role=Role.GUEST,
    ),
    UserDB(
        ulid='01USER6ULID',
        email='manager@example.com',
        password='hashed_password6',
        role=Role.ADMIN,
    ),
]

guests = [
    GuestDB(
        ulid='01GUEST3ULID',
        document='654321789',
        name='Alice',
        surname='Johnson',
        country='UK',
        phone='+447700900345',
    ),
    GuestDB(
        ulid='01GUEST4ULID',
        document='456789123',
        name='Bob',
        surname='Brown',
        country='Australia',
        phone='+61412345678',
    ),
    GuestDB(
        ulid='01GUEST5ULID',
        document='789456123',
        name='Carlos',
        surname='Garcia',
        country='Mexico',
        phone='+525512345678',
    ),
    GuestDB(
        ulid='01GUEST6ULID',
        document='987123456',
        name='Eve',
        surname='White',
        country='New Zealand',
        phone='+64211234567',
    ),
]
amenities = [
    AmenitieDB(name='Gym'),
    AmenitieDB(name='Air Conditioning'),
    AmenitieDB(name='Room Service'),
    AmenitieDB(name='Sauna'),
    AmenitieDB(name='Hot Tub'),
    AmenitieDB(name='Pet Friendly'),
]
accommodations = [
    AccommodationDB(
        ulid='01ACCOMMODATION3ULID',
        name='Cozy Cabin',
        total_guests=3,
        single_beds=2,
        double_beds=1,
        price=100.0,
        amenities=[
            AmenitieDB(name='Gym'),
            AmenitieDB(name='Air Conditioning'),
        ],
    ),
    AccommodationDB(
        ulid='01ACCOMMODATION4ULID',
        name='Modern Apartment',
        total_guests=2,
        single_beds=1,
        double_beds=1,
        price=80.0,
        amenities=[
            AmenitieDB(name='Hot Tub'),
            AmenitieDB(name='Pet Friendly'),
        ],
    ),
    AccommodationDB(
        ulid='01ACCOMMODATION5ULID',
        name='Beachside Bungalow',
        total_guests=5,
        single_beds=3,
        double_beds=1,
        price=250.0,
        amenities=[
            AmenitieDB(name='Room Service'),
            AmenitieDB(name='Sauna'),
        ],
    ),
    AccommodationDB(
        ulid='01ACCOMMODATION6ULID',
        name='Mountain Retreat',
        total_guests=6,
        single_beds=4,
        double_beds=1,
        price=300.0,
        amenities=[
            AmenitieDB(name='Sauna'),
            AmenitieDB(name='Hot Tub'),
            AmenitieDB(name='Pet Friendly'),
        ],
    ),
]


bookings = [
    BookingDB(
        ulid='01BOOKING3ULID',
        check_in=datetime(2024, 10, 20, 15, 0),
        check_out=datetime(2024, 10, 23, 11, 0),
        budget=300.0,
        guest_ulid='01GUEST3ULID',
        accommodation_ulid='01ACCOMMODATION3ULID',
    ),
    BookingDB(
        ulid='01BOOKING4ULID',
        check_in=datetime(2024, 11, 5, 15, 0),
        check_out=datetime(2024, 11, 10, 11, 0),
        budget=750.0,
        guest_ulid='01GUEST4ULID',
        accommodation_ulid='01ACCOMMODATION5ULID',
    ),
    BookingDB(
        ulid='01BOOKING5ULID',
        check_in=datetime(2024, 9, 12, 15, 0),
        check_out=datetime(2024, 9, 15, 11, 0),
        budget=240.0,
        guest_ulid='01GUEST5ULID',
        accommodation_ulid='01ACCOMMODATION2ULID',
    ),
    BookingDB(
        ulid='01BOOKING6ULID',
        check_in=datetime(2024, 12, 1, 15, 0),
        check_out=datetime(2024, 12, 5, 11, 0),
        budget=1200.0,
        guest_ulid='01GUEST6ULID',
        accommodation_ulid='01ACCOMMODATION6ULID',
    ),
]


def populate_database(session: Session):
    session.add_all(users)
    session.add_all(guests)
    session.add_all(amenities)
    session.add_all(accommodations)
    session.add_all(bookings)

    session.commit()
