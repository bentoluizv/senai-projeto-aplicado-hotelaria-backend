import pytest

from app.entities.schemas.Enums import BookingStatus
from app.utils.validateStatusChange import (
    ChangeStatusCommand,
    validateStatusChange,
)


@pytest.mark.parametrize(
    ('old_status', 'new_status', 'expected_result'),
    [
        # Transições válidas
        ('pre-reserva', 'reservado', True),
        ('pre-reserva', 'cancelada', True),
        ('reservado', 'aguardando check-in', True),
        ('aguardando check-in', 'active', True),
        ('active', 'aguardando check-out', True),
        ('aguardando check-out', 'finalizada', True),
        # Transições inválidas
        ('cancelada', 'pre-reserva', False),
        ('finalizada', 'pre-reserva', False),
        ('reservado', 'finalizada', False),
        ('active', 'reservado', False),
        ('aguardando check-in', 'finalizada', False),
        ('aguardando check-out', 'active', False),
        # Estados finais
        ('cancelada', 'reservado', False),
        ('finalizada', 'aguardando check-in', False),
    ],
)
def test_change_status_command(old_status, new_status, expected_result):
    command = ChangeStatusCommand(old_status, new_status)
    assert command.validate() == expected_result


@pytest.mark.parametrize(
    ('old_status', 'new_status', 'expected_result'),
    [
        # Casos válidos
        (BookingStatus('pre-reserva'), BookingStatus('reservado'), True),
        (
            BookingStatus('reservado'),
            BookingStatus('aguardando check-in'),
            True,
        ),
        # Casos inválidos
        (BookingStatus('cancelada'), BookingStatus('reservado'), False),
        (
            BookingStatus('aguardando check-in'),
            BookingStatus('finalizada'),
            False,
        ),
    ],
)
def test_validate_status_change(old_status, new_status, expected_result):
    assert validateStatusChange(new_status, old_status) == expected_result
