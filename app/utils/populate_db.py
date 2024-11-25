from datetime import datetime

from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from app.database.models import (
    AccommodationDB,
    AmenitieDB,
    BookingDB,
    GuestDB,
)


def populate_db(session: Session):
    guests = [
        GuestDB(
            document='1234325',
            name='John',
            surname='Doe',
            country='Brasil',
            phone='389201212',
        ),
        GuestDB(
            document='2345436',
            name='Jane',
            surname='Smith',
            country='Brasil',
            phone='389201213',
        ),
        GuestDB(
            document='3456547',
            name='Alice',
            surname='Johnson',
            country='Brasil',
            phone='389201214',
        ),
        GuestDB(
            document='4567658',
            name='Bob',
            surname='Brown',
            country='Brasil',
            phone='389201215',
        ),
        GuestDB(
            document='5678769',
            name='Charlie',
            surname='Davis',
            country='Brasil',
            phone='389201216',
        ),
        GuestDB(
            document='6789870',
            name='David',
            surname='Miller',
            country='Brasil',
            phone='389201217',
        ),
        GuestDB(
            document='7890981',
            name='Eve',
            surname='Wilson',
            country='Brasil',
            phone='389201218',
        ),
        GuestDB(
            document='8901092',
            name='Frank',
            surname='Moore',
            country='Brasil',
            phone='389201219',
        ),
        GuestDB(
            document='9012103',
            name='Grace',
            surname='Taylor',
            country='Brasil',
            phone='389201220',
        ),
        GuestDB(
            document='0123214',
            name='Hank',
            surname='Anderson',
            country='Brasil',
            phone='389201221',
        ),
        GuestDB(
            document='01234274',
            name='Levis',
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
            name='Beachfront Villa',
            total_guests=6,
            single_beds=2,
            double_beds=2,
            price=250.0,
            status='avaiable',
        ),
        AccommodationDB(
            name='Mountain Retreat',
            total_guests=4,
            single_beds=1,
            double_beds=1,
            price=180.0,
            status='avaiable',
        ),
        AccommodationDB(
            name='City Center Apartment',
            total_guests=2,
            single_beds=0,
            double_beds=1,
            price=120.0,
            status='avaiable',
        ),
        AccommodationDB(
            name='Luxury Penthouse',
            total_guests=8,
            single_beds=2,
            double_beds=3,
            price=500.0,
            status='avaiable',
        ),
        AccommodationDB(
            name='Cozy Cottage',
            total_guests=3,
            single_beds=1,
            double_beds=1,
            price=150.0,
            status='avaiable',
        ),
        AccommodationDB(
            name='Suburban Family Home',
            total_guests=10,
            single_beds=3,
            double_beds=4,
            price=300.0,
            status='avaiable',
        ),
        AccommodationDB(
            name='Modern Loft',
            total_guests=2,
            single_beds=0,
            double_beds=1,
            price=200.0,
            status='avaiable',
        ),
        AccommodationDB(
            name='Country Inn',
            total_guests=5,
            single_beds=2,
            double_beds=1,
            price=170.0,
            status='avaiable',
        ),
        AccommodationDB(
            name='Charming Bungalow',
            total_guests=4,
            single_beds=2,
            double_beds=0,
            price=140.0,
            status='avaiable',
        ),
        AccommodationDB(
            name='Seaside Cabin',
            total_guests=6,
            single_beds=3,
            double_beds=1,
            price=220.0,
            status='avaiable',
        ),
        AccommodationDB(
            name='Seaside Tent',
            total_guests=1,
            single_beds=1,
            double_beds=0,
            price=50.0,
            status='avaiable',
        ),
    ]

    accommodations[0].ulid = '01JAFQXR26049VNR64PJE3J1W4'
    guests[0].ulid = '01JB3HNWQ2D7XPPJ181G3YTH8T'

    session.add_all(accommodations)

    fixed_dates = [
        (
            datetime(2023, 5, 1, tzinfo=ZoneInfo('America/Sao_Paulo')),
            datetime(2023, 5, 10, tzinfo=ZoneInfo('America/Sao_Paulo')),
        ),
        (
            datetime(2023, 6, 15, tzinfo=ZoneInfo('America/Sao_Paulo')),
            datetime(2023, 6, 20, tzinfo=ZoneInfo('America/Sao_Paulo')),
        ),
        (
            datetime(2023, 7, 1, tzinfo=ZoneInfo('America/Sao_Paulo')),
            datetime(2023, 7, 5, tzinfo=ZoneInfo('America/Sao_Paulo')),
        ),
        (
            datetime(2024, 1, 1, tzinfo=ZoneInfo('America/Sao_Paulo')),
            datetime(2024, 1, 10, tzinfo=ZoneInfo('America/Sao_Paulo')),
        ),
        (
            datetime(2024, 12, 1, tzinfo=ZoneInfo('America/Sao_Paulo')),
            datetime(2024, 12, 15, tzinfo=ZoneInfo('America/Sao_Paulo')),
        ),
    ]

    bookings: list[BookingDB] = []

    for i, (check_in, check_out) in enumerate(fixed_dates):
        guest = guests[i + 1]
        accommodation = accommodations[i + 1]
        budget = (check_out - check_in).days * accommodation.price

        booking = BookingDB(
            status='booked',
            check_in=check_in,
            check_out=check_out,
            budget=budget,
            guest=guest,
            guest_ulid=guest.ulid,
            accommodation=accommodation,
            accommodation_ulid=accommodation.ulid,
        )
        bookings.append(booking)

    bookings[0].ulid = '01JB3HNXD570W7V12DSQWS2XMJ'
    bookings[0].locator = 'AD934934'
    session.add_all(bookings)
    session.commit()
