import enum


class BookingStatus(enum.Enum):
    PRE_RESERVA = 'pre-reserva'
    RESERVA = 'reservado'
    AGUARDANDO_CHECK_IN = 'aguardando check-in'
    ATIVA = 'active'
    AGUARDANDO_CHECK_OUT = 'aguardando check-out'
    FINALIZADA = 'finalizada'
    CANCELADA = 'cancelada'


class AccommodationStatus(enum.Enum):
    DISPONIVEL = 'disponivel'
    OCUPADO = 'ocupado'


class Role(enum.Enum):
    ADMIN = 'admin'
    USER = 'user'
    GUEST = 'guest'
