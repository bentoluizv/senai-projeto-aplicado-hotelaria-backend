CREATE TABLE IF NOT EXISTS guest (
    uuid                    BLOB PRIMARY KEY,
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name                    TEXT NOT NULL,
    surname                 TEXT NOT NULL,
    country                 TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS accommodation (
    uuid                    BLOB PRIMARY KEY,
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status                  TEXT NOT NULL,
    name                    TEXT NOT NULL,
    total_guests            INTEGER NOT NULL,
    single_beds             INTEGER NOT NULL,
    double_beds             INTEGER NOT NULL,
    min_nights              INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS booking (
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

CREATE TABLE IF NOT EXISTS booking_with_special_request (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_uuid            BLOB NOT NULL,
    special_request         VARCHAR(500) NOT NULL,
    FOREIGN KEY(booking_uuid) REFERENCES booking(uuid)
);

CREATE TABLE IF NOT EXISTS amenities (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    amenitie                TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS amenities_per_accommodation (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    accommodation_uuid      BLOB NOT NULL,
    amenitie_id             INTEGER NOT NULL,
    FOREIGN KEY(accommodation_uuid) REFERENCES accommodation(uuid),
    FOREIGN KEY(amenitie_id) REFERENCES amenities(id)
);

CREATE TABLE IF NOT EXISTS phones_per_guest (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    guest_uuid              BLOB NOT NULL,
    phone                   TEXT NOT NULL,
    FOREIGN KEY(guest_uuid) REFERENCES guest(uuid)
);

