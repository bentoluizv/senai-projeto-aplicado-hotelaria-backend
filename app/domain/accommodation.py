"""Accommodation class must validate data related to the entity when instantiating new objects"""
import uuid


class Accommodation:
    """class representing an Accommodation"""
    def __init__(self, params):
        self.uuid = params.uuid if params.uuid is not None else uuid.uuid4()
        self.created_at = params.created_at if params.created_at is not None else None
        self.status = params.status
        self.name = params.name
        self.total_guests = params.total_guests
        self.single_beds = params.double_beds
        self.min_ninghts = params.min_ninghts
        self.amenities = params.amenities


    # TODO: Criar função de validação para as propriedades da acomodação, pode ser um método que vai ser chamado pelo construtor passando 'params' e verificando se todas as propriedades esperadas existem e estão de acordo com os tipos esperados.