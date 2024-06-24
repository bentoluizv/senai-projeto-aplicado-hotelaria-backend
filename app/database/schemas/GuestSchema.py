from datetime import datetime

from pydantic import Field

from app.utils.StrictModel import StrictModel


class GuestCreationalSchema(StrictModel):
    document: str
    name: str
    surname: str
    phone: str
    country: str


class GuestDB(GuestCreationalSchema):
    created_at: str = Field(default=datetime.now().isoformat())
