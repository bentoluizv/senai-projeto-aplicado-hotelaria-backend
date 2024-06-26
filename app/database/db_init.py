import json

from sqlalchemy.orm import Session

from app.database.models import (
    AccommodationDB,
    AmenitieDB,
    BookingDB,
    GuestDB,
)


def db_init(session: Session):
    with open('app/database/json/guests.json', encoding='utf-8') as file:
        data = json.load(file)

        for guest in data['guests']:
            guest_db = GuestDB(**guest)
            session.add(guest_db)

    with open('app/database/json/amenities.json', encoding='utf-8') as file:
        data = json.load(file)

        for amenitie in data['amenities']:
            amenitie_db = AmenitieDB(amenitie['name'])
            session.add(amenitie_db)

    with open(
        'app/database/json/accommodations.json', encoding='utf-8'
    ) as file:
        data = json.load(file)

        for accommodation in data['accommodations']:
            accomodation_db = AccommodationDB(
                name=accommodation['name'],
                status=accommodation['status'],
                created_at=accommodation['created_at'],
                total_guests=accommodation['total_guests'],
                single_beds=accommodation['single_beds'],
                double_beds=accommodation['double_beds'],
                min_nights=accommodation['min_nights'],
                price=accommodation['price'],
                amenities=[],
            )

            for amenitie in accommodation['amenities']:
                amenitie_db = session.get(AmenitieDB, amenitie['id'])

                if amenitie_db:
                    accomodation_db.amenities.append(amenitie_db)

            session.add(accomodation_db)

    with open('app/database/json/bookings.json', encoding='utf-8') as file:
        data = json.load(file)

        for booking in data['bookings']:
            guest_db = session.get(GuestDB, booking['guest_document'])
            accommodation_db = session.get(
                AccommodationDB, booking['accommodation_id']
            )
            if guest_db and accommodation_db:
                booking_db = BookingDB(
                    **booking, guest=guest_db, accommodation=accommodation_db
                )

            session.add(booking_db)
