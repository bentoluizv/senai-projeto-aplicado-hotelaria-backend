from app.entities.schemas.Enums import BookingStatus


class ChangeStatusCommand:
    def __init__(self, old_status: str, new_status: str):
        self.old_status = old_status
        self.new_status = new_status

    def validate(self) -> bool:
        transitions = {
            'pre-reserva': ['reservado', 'cancelada'],
            'reservado': ['aguardando check-in'],
            'aguardando check-in': ['active'],
            'active': ['aguardando check-out'],
            'aguardando check-out': ['finalizada'],
        }

        if self.old_status in {'cancelada', 'finalizada'}:
            return False

        return self.new_status in transitions.get(self.old_status, [])


def validateStatusChange(
    new_status: BookingStatus, old_status: BookingStatus
) -> bool:
    command = ChangeStatusCommand(old_status.value, new_status.value)
    return command.validate()
