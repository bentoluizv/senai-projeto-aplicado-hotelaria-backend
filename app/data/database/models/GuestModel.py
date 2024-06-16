from typing import TypedDict


class GuestModel(TypedDict):
    document: str
    created_at: str
    name: str
    surname: str
    country: str
    phone: str
