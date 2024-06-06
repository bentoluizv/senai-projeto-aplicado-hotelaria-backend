from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from pydantic import (
    Field,
    field_serializer,
    field_validator,
    model_validator,
)

from app.utils.strict_model import StrictModel


class Accommodation(StrictModel):
    uuid: UUID = Field(default=uuid4())
    name: str
    status: str = Field(default="Disponível")
    total_guests: int
    single_beds: int
    double_beds: int
    min_nights: int = Field(default=2)
    price: int
    created_at: datetime = Field(default=datetime.now())
    amenities: List[str]

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return self.model_dump()

    def to_json(self):
        return self.model_dump_json()

    @model_validator(mode="before")
    def validate_input_data_params(cls, data):
        parsed_data = {
            "uuid": UUID(data["uuid"]),
            "name": data["name"],
            "status": data["status"],
            "total_guests": int(data["total_guests"]),
            "single_beds": int(data["single_beds"]),
            "double_beds": int(data["double_beds"]),
            "min_nights": int(data["min_nights"]),
            "price": int(data["price"]),
            "created_at": datetime.fromisoformat(data["created_at"]),
            "amenities": data["amenities"],
        }
        return parsed_data

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
        if self.double_beds <= 0 and self.single_beds <= 0:
            raise ValueError(
                "Accommodation must have at least one type of bed available"
            )
        return self

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: datetime):
        return created_at.isoformat()

    @field_serializer("uuid")
    def serialize_uuid(self, uuid):
        return str(uuid)

    @field_serializer(
        "total_guests", "single_beds", "double_beds", "min_nights", "price"
    )
    def serialize_interger_properties_to_str(self, value):
        return str(value)
