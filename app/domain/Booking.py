from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from app.domain.Accomodation import Accommodation
from app.domain.Guests import Guest

#TODO: Implementar a validação dos dados de entrada da classe.

@dataclass
class Booking:
    def __init__(self, status: str, check_in: str, check_out: str, guest: Guest, accommodation: Accommodation, uuid: str|None=None, created_at: str|None=None):
        self.uuid = str(uuid4()) if uuid is None else uuid
        self.created_at = datetime.now().isoformat() if created_at is None else created_at
        self.status = status
        self.check_in = check_in
        self.check_out = check_out
        self.guest = guest
        self.accommodation = accommodation
        self.requests = []

    def toObj(self):
        return self.__dict__

    def add_request(self, request):
        self.requests.append(request)