DROP TABLE IF EXISTS guest;
DROP TABLE IF EXISTS accommodation;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS amenities_per_accommodation;
DROP TABLE IF EXISTS booking;
DROP TABLE IF EXISTS requests_per_bookings;


CREATE TABLE IF NOT EXISTS guest (
    document,               TEXT PRIMARY KEY,
    created_at              TEXT NOT NULL,
    name                    TEXT NOT NULL,
    surname                 TEXT NOT NULL,
    country                 TEXT NOT NULL,
    phone                   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS accommodation (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at              TEXT NOT NULL,
    name                    TEXT NOT NULL,
    status                  TEXT NOT NULL,
    total_guests            INTEGER NOT NULL,
    single_beds             INTEGER NOT NULL,
    double_beds             INTEGER NOT NULL,
    min_nights              INTEGER NOT NULL,
    price                   INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS amenities (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    amenitie                TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS amenities_per_accommodation (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    accommodation_uuid      TEXT NOT NULL,
    amenitie_id             INTEGER NOT NULL,
    FOREIGN KEY(accommodation_uuid) REFERENCES accommodation(uuid) ON DELETE CASCADE,
    FOREIGN KEY(amenitie_id) REFERENCES amenities(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS booking (
    uuid                    TEXT PRIMARY KEY,
    created_at              TEXT NOT NULL,
    status                  TEXT NOT NULL,
    check_in                TEXT NOT NULL,
    check_out               TEXT NOT NULL,
    document              TEXT NOT NULL,
    accommodation_uuid      TEXT NOT NULL,
    FOREIGN KEY(document) REFERENCES guest(uuid),
    FOREIGN KEY(accommodation_uuid) REFERENCES accommodation(uuid)
);

CREATE TABLE IF NOT EXISTS requests_per_bookings (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_uuid            TEXT NOT NULL,
    special_request         TEXT NOT NULL,
    FOREIGN KEY(booking_uuid) REFERENCES booking(uuid)
);

