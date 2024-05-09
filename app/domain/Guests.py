from dataclasses import dataclass
from datetime import datetime

#TODO: Implementar a validação dos dados de entrada da classe.

@dataclass
class Guest:
    def __init__(self, document:str, name:str, surname:str, country:str, phone:str, created_at: str|None=None):
        self.document = document
        self.name = name
        self.surname = surname
        self.phone = phone
        self.country = country
        self.created_at = datetime.now().isoformat() if created_at is None else created_at

    def toObj(self):
        return self.__dict__