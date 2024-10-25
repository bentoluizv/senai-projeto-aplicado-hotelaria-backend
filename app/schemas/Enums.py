import enum


class BookingStatus(enum.Enum):
    PRE_BOOKED = 'pre-booked'
    BOOKED = 'booked'
    WAITING_CHECK_IN = 'waiting check-in'
    ACTIVE = 'active'
    WAITING_CHECK_OUT = 'waiting check-out'
    COMPLETED = 'completed'
    CANCELED = 'canceled'


class AccommodationStatus(enum.Enum):
    AVAIABLE = 'avaiable'
    OCUPIED = 'ocupied'


class Role(enum.Enum):
    ADMIN = 'admin'
    USER = 'user'
    GUEST = 'guest'
