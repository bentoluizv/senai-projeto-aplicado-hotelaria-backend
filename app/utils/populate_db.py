from datetime import datetime, timedelta
from random import choice, randint

from sqlalchemy.orm import Session
from ulid import ULID

from app.database.models import (
    AccommodationDB,
    BookingDB,
    BookingStatus,
    GuestDB,
)


def generate_random_checkin_checkout():
    """Gera check-in e check-out aleatórios sem parâmetros."""
    # Definindo uma data de início fixa
    start_date = datetime(2024, 1, 1)

    # Gera um número aleatório de dias até o check-in
    days_until_checkin = randint(
        0, 365
    )  # até 1 ano a partir da data de início
    checkin_date = start_date + timedelta(days=days_until_checkin)

    # Gera um número aleatório de noites para o check-out
    nights = randint(1, 7)  # entre 1 e 7 noites
    checkout_date = checkin_date + timedelta(days=nights)

    return checkin_date, checkout_date


def populate_db(session: Session):
    guests = [
        GuestDB(
            ulid=str(ULID()),
            document='1234325',
            name='John',
            surname='Doe',
            country='Brasil',
            phone='389201212',
        ),
        GuestDB(
            ulid=str(ULID()),
            document='2345436',
            name='Jane',
            surname='Smith',
            country='Brasil',
            phone='389201213',
        ),
        GuestDB(
            ulid=str(ULID()),
            document='3456547',
            name='Alice',
            surname='Johnson',
            country='Brasil',
            phone='389201214',
        ),
        GuestDB(
            ulid=str(ULID()),
            document='4567658',
            name='Bob',
            surname='Brown',
            country='Brasil',
            phone='389201215',
        ),
        GuestDB(
            ulid=str(ULID()),
            document='5678769',
            name='Charlie',
            surname='Davis',
            country='Brasil',
            phone='389201216',
        ),
        GuestDB(
            ulid=str(ULID()),
            document='6789870',
            name='David',
            surname='Miller',
            country='Brasil',
            phone='389201217',
        ),
        GuestDB(
            ulid=str(ULID()),
            document='7890981',
            name='Eve',
            surname='Wilson',
            country='Brasil',
            phone='389201218',
        ),
        GuestDB(
            ulid=str(ULID()),
            document='8901092',
            name='Frank',
            surname='Moore',
            country='Brasil',
            phone='389201219',
        ),
        GuestDB(
            ulid=str(ULID()),
            document='9012103',
            name='Grace',
            surname='Taylor',
            country='Brasil',
            phone='389201220',
        ),
        GuestDB(
            ulid=str(ULID()),
            document='0123214',
            name='Hank',
            surname='Anderson',
            country='Brasil',
            phone='389201221',
        ),
    ]

    accommodations = [
        AccommodationDB(
            ulid=str(ULID()),
            name='Beachfront Villa',
            total_guests=6,
            single_beds=2,
            double_beds=2,
            price=250.0,
        ),
        AccommodationDB(
            ulid=str(ULID()),
            name='Mountain Retreat',
            total_guests=4,
            single_beds=1,
            double_beds=1,
            price=180.0,
        ),
        AccommodationDB(
            ulid=str(ULID()),
            name='City Center Apartment',
            total_guests=2,
            single_beds=0,
            double_beds=1,
            price=120.0,
        ),
        AccommodationDB(
            ulid=str(ULID()),
            name='Luxury Penthouse',
            total_guests=8,
            single_beds=2,
            double_beds=3,
            price=500.0,
        ),
        AccommodationDB(
            ulid=str(ULID()),
            name='Cozy Cottage',
            total_guests=3,
            single_beds=1,
            double_beds=1,
            price=150.0,
        ),
        AccommodationDB(
            ulid=str(ULID()),
            name='Suburban Family Home',
            total_guests=10,
            single_beds=3,
            double_beds=4,
            price=300.0,
        ),
        AccommodationDB(
            ulid=str(ULID()),
            name='Modern Loft',
            total_guests=2,
            single_beds=0,
            double_beds=1,
            price=200.0,
        ),
        AccommodationDB(
            ulid=str(ULID()),
            name='Country Inn',
            total_guests=5,
            single_beds=2,
            double_beds=1,
            price=170.0,
        ),
        AccommodationDB(
            ulid=str(ULID()),
            name='Charming Bungalow',
            total_guests=4,
            single_beds=2,
            double_beds=0,
            price=140.0,
        ),
        AccommodationDB(
            ulid=str(ULID()),
            name='Seaside Cabin',
            total_guests=6,
            single_beds=3,
            double_beds=1,
            price=220.0,
        ),
    ]

    session.add_all(guests)
    session.add_all(accommodations)

    bookings = []
    for i in range(30):
        check_in, check_out = generate_random_checkin_checkout()
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