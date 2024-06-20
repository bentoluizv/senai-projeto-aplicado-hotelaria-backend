from datetime import date

from pydantic import Field

from app.utils.StrictModel import StrictModel


class GuestSchema(StrictModel):
    document: str
    name: str
    surname: str
    phone: str
    country: str


class GuestDB(GuestSchema):
    created_at: str = Field(default=date.today().isoformat())
