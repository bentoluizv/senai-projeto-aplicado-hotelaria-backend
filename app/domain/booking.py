"""Booking class must validate data related to the entity when instantiating new objects"""
import uuid


class Booking:
    """class representing an Booking"""
    def __init__(self, params):
        self.uuid = params.uuid if params.uuid is not None else uuid.uuid4()
        self.created_at = params.created_at if params.created_at is not None else None
        self.status = params.status
        self.check_in = params.check_in
        self.check_out = params.check_out
        self.guest = params.guest
        self.accommodation = params.accommodation

    # TODO: Criar função de validação para as propriedades da reserva, pode ser um método que vai ser chamado pelo construtor passando 'params' e verificando se todas as propriedades esperadas existem e estão de acordo com os tipos esperados.