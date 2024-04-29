DROP TABLE IF EXISTS guest;
DROP TABLE IF EXISTS accommodation;
DROP TABLE IF EXISTS booking;
DROP TABLE IF EXISTS booking_with_special_request;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS amenities_per_accommodation;
DROP TABLE IF EXISTS phones_per_guest;

CREATE TABLE guest (
    uuid                    BLOB PRIMARY KEY,
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name                    TEXT NOT NULL,
    surname                 TEXT NOT NULL,
    country                 TEXT NOT NULL
);

CREATE TABLE accommodation (
    uuid                    BLOB PRIMARY KEY,
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status                  TEXT NOT NULL,
    name                    TEXT NOT NULL,
    total_guests            INTEGER NOT NULL,
    single_beds             INTEGER NOT NULL,
    double_beds             INTEGER NOT NULL,
    min_nights              INTEGER NOT NULL
);

CREATE TABLE booking (
    uuid                    BLOB PRIMARY KEY,
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status                  TEXT NOT NULL,
    check_in                TIMESTAMP NOT NULL,
    check_out               TIMESTAMP NOT NULL,
    guest_uuid              BLOB NOT NULL,
    accommodation_uuid      BLOB NOT NULL,
    FOREIGN KEY(guest_uuid) REFERENCES guest(uuid),
    FOREIGN KEY(accommodation_uuid) REFERENCES accommodation(uuid)
);

CREATE TABLE booking_with_special_request (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_uuid            BLOB NOT NULL,
    special_request         VARCHAR(500) NOT NULL,
    FOREIGN KEY(booking_uuid) REFERENCES booking(uuid)
);

CREATE TABLE amenities (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    amenitie                TEXT NOT NULL
);

CREATE TABLE amenities_per_accommodation (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    accommodation_uuid      BLOB NOT NULL,
    amenitie_id             INTEGER NOT NULL,
    FOREIGN KEY(accommodation_uuid) REFERENCES accommodation(uuid),
    FOREIGN KEY(amenitie_id) REFERENCES amenities(id)
);

CREATE TABLE phones_per_guest (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    guest_uuid              BLOB NOT NULL,
    phone                   TEXT NOT NULL,
    FOREIGN KEY(guest_uuid) REFERENCES guest(uuid)
);

