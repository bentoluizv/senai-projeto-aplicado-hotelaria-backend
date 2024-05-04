"""Guest class must validate data related to the entity when instantiating new objects"""
import uuid


class Guest:
    """class representing an Guest"""
    def __init__(self, params):
        self.uuid = params.uuid if params.uuid is not None else uuid.uuid4()
        self.created_at = params.created_at if params.created_at is not None else None
        self.name = params.name
        self.surname = params.surname
        self.phones = params.phones


    # TODO: Criar função de validação para as propriedades do hóspede, pode ser um método que vai ser chamado pelo construtor passando 'params' e verificando se todas as propriedades esperadas existem e estão de acordo com os tipos esperados.