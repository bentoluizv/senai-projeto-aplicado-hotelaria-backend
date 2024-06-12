from datetime import datetime

from pydantic import (
    Field,
    field_validator,
    model_validator,
)

from app.utils.StrictModel import StrictModel


class Accommodation(StrictModel):
    id: int | None = Field(default=None)
    name: str
    status: str = Field(default="Disponível")
    total_guests: int
    single_beds: int
    double_beds: int
    min_nights: int = Field(default=2)
    price: int
    created_at: str = Field(default=datetime.now().isoformat())
    amenities: list[str]

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return self.model_dump()

    def to_json(self):
        return self.model_dump_json()

    @model_validator(mode="after")
    def validade_name_is_not_an_empty_strings(self):
        if not self.name:
            raise ValueError("Name is probably empty")

        return self

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        expected_statuses = ["Disponível", "Reservado", "Aguardando Limpeza"]
        if value not in expected_statuses:
            raise ValueError(
                f"Invalid status! [{value}] does not match any expected status: {expected_statuses}"
            )
        return value

    @field_validator("min_nights")
    @classmethod
    def validate_min_nights(cls, value):
        if value <= 0:
            raise ValueError("Minimum number of nights must be greater than one")
        return value

    @field_validator("price")
    @classmethod
    def validate_price(cls, value):
        if value <= 0:
            raise ValueError("Invalid Price")
        return value

    @model_validator(mode="after")
    def validate_amount_of_beds(self):
        if (
            self.name != "Estacionamento para overlanders"
            and self.double_beds <= 0
            and self.single_beds <= 0
        ):
            raise ValueError(
                "Accommodation must have at least one type of bed available"
            )
        return self
