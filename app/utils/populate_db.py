from datetime import datetime
from random import choice

from sqlalchemy.orm import Session
from ulid import ULID

from app.database.models import (
    AccommodationDB,
    AmenitieDB,
    BookingDB,
    BookingStatus,
    GuestDB,
)


def populate_db(session: Session):
    guests = [
        GuestDB(
            ulid='01JAFQSB29MRH1AH1J6Z8GR8KR',
            document='1234325',
            name='John',
            surname='Doe',
            country='Brasil',
            phone='389201212',
        ),
        GuestDB(
            ulid='01JAFQT8BNX2K4SXH1TH6ESQFX',
            document='2345436',
            name='Jane',
            surname='Smith',
            country='Brasil',
            phone='389201213',
        ),
        GuestDB(
            ulid='01JAFQTH6ETC71168EYY8JX4WE',
            document='3456547',
            name='Alice',
            surname='Johnson',
            country='Brasil',
            phone='389201214',
        ),
        GuestDB(
            ulid='01JAFQTXX5RXZ83NVKXVGTVQTM',
            document='4567658',
            name='Bob',
            surname='Brown',
            country='Brasil',
            phone='389201215',
        ),
        GuestDB(
            ulid='01JAFQV5SFYNHFP2CTT5WY727M',
            document='5678769',
            name='Charlie',
            surname='Davis',
            country='Brasil',
            phone='389201216',
        ),
        GuestDB(
            ulid='01JAFQVDY5RXWRXJ17C23NM6QK',
            document='6789870',
            name='David',
            surname='Miller',
            country='Brasil',
            phone='389201217',
        ),
        GuestDB(
            ulid='01JAFQVNWESMWR4WZ1P49ZEJ7Z',
            document='7890981',
            name='Eve',
            surname='Wilson',
            country='Brasil',
            phone='389201218',
        ),
        GuestDB(
            ulid='01JAFQVWY54SDCAQQ7Y1JDBD8Y',
            document='8901092',
            name='Frank',
            surname='Moore',
            country='Brasil',
            phone='389201219',
        ),
        GuestDB(
            ulid='01JAFQW49ZQTK6AH73HYFP9AQE',
            document='9012103',
            name='Grace',
            surname='Taylor',
            country='Brasil',
            phone='389201220',
        ),
        GuestDB(
            ulid='01JAFQWATY7XHSFGFJQV1SYDB4',
            document='0123214',
            name='Hank',
            surname='Anderson',
            country='Brasil',
            phone='389201221',
        ),
    ]

    session.add_all(guests)

    amenities = [
        AmenitieDB(name='WiFi'),
        AmenitieDB(name='Toalhas'),
        AmenitieDB(name='Banheira'),
        AmenitieDB(name='Ducha'),
        AmenitieDB(name='TV'),
        AmenitieDB(name='Aquecedor'),
    ]

    session.add_all(amenities)

    accommodations = [
        AccommodationDB(
            ulid='01JAFQWJ3C8F7E0M2T5FHKY3YB',
            name='Beachfront Villa',
            total_guests=6,
            single_beds=2,
            double_beds=2,
            price=250.0,
        ),
        AccommodationDB(
            ulid='01JAFQWRHH5BA96R43F0TEBQM3',
            name='Mountain Retreat',
            total_guests=4,
            single_beds=1,
            double_beds=1,
            price=180.0,
        ),
        AccommodationDB(
            ulid='01JAFQWZ7FFJFMD0406F29YQRZ',
            name='City Center Apartment',
            total_guests=2,
            single_beds=0,
            double_beds=1,
            price=120.0,
        ),
        AccommodationDB(
            ulid='01JAFQX8E203Y0CNK1KYPPV5RK',
            name='Luxury Penthouse',
            total_guests=8,
            single_beds=2,
            double_beds=3,
            price=500.0,
        ),
        AccommodationDB(
            ulid='01JAFQXR26049VNR64PJE3J1W4',
            name='Cozy Cottage',
            total_guests=3,
            single_beds=1,
            double_beds=1,
            price=150.0,
        ),
        AccommodationDB(
            ulid='01JAFQY09Z7ABD18R5MHWTPWJS',
            name='Suburban Family Home',
            total_guests=10,
            single_beds=3,
            double_beds=4,
            price=300.0,
        ),
        AccommodationDB(
            ulid='01JAFQY731PWBTCC9CW7B2AVTJ',
            name='Modern Loft',
            total_guests=2,
            single_beds=0,
            double_beds=1,
            price=200.0,
        ),
        AccommodationDB(
            ulid='01JAFQYSG41JAFWYT1SF9E8W6Y',
            name='Country Inn',
            total_guests=5,
            single_beds=2,
            double_beds=1,
            price=170.0,
        ),
        AccommodationDB(
            ulid='01JAFQZ30EFSA1JHMKF1QYW67K',
            name='Charming Bungalow',
            total_guests=4,
            single_beds=2,
            double_beds=0,
            price=140.0,
        ),
        AccommodationDB(
            ulid='01JAFR5W4HAZYDFV4300P9CE7T',
            name='Seaside Cabin',
            total_guests=6,
            single_beds=3,
            double_beds=1,
            price=220.0,
        ),
    ]

    session.add_all(accommodations)

    fixed_dates = [
        (datetime(2023, 5, 1), datetime(2023, 5, 10)),
        (datetime(2023, 6, 15), datetime(2023, 6, 20)),
        (datetime(2023, 7, 1), datetime(2023, 7, 5)),
        (datetime(2024, 1, 1), datetime(2024, 1, 10)),
        (datetime(2024, 12, 1), datetime(2024, 12, 15)),
    ]

    bookings = []

    for check_in, check_out in fixed_dates:
        guest = choice(guests)
        accommodation = choice(accommodations)
        budget = (check_out - check_in).days * accommodation.price

        booking = BookingDB(
            ulid=str(ULID()),
            status=BookingStatus.BOOKED,
            check_in=check_in,
            check_out=check_out,
            budget=budget,
            guest=guest,
            guest_ulid=guest.ulid,
            accommodation=accommodation,
            accommodation_ulid=accommodation.ulid,
        )
        bookings.append(booking)

    session.add_all(bookings)
    session.commit()
