from datetime import datetime

from pydantic import Field, field_serializer, model_validator

from app.utils.is_valid_cpf import is_valid_cpf
from app.utils.strict_model import StrictModel


class Guest(StrictModel):
    document: str
    name: str
    surname: str
    phone: str
    country: str
    created_at: datetime = Field(default=datetime.now())

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return self.model_dump()

    def to_json(self):
        return self.model_dump_json()

    @model_validator(mode="before")
    def transform_created_at_isoformat_string_to_datetime(cls, data):
        data["created_at"] = datetime.fromisoformat(data["created_at"])

        return data

    @model_validator(mode="before")
    def validate_document_if_cpf(cls, data):
        if not is_valid_cpf(data["document"]):
            raise ValueError("The CPF used as a document is invalid")

        return data

    @model_validator(mode="after")
    def validade_properties_is_not_empty_strings(self):
        empty_attrs = []

        for attr, value in self.__dict__.items():
            if isinstance(value, str) and not value:
                empty_attrs.append(attr)

        if empty_attrs:
            raise ValueError(
                f"the following attributes are probably empty: {empty_attrs}"
            )

        return self

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: datetime):
        return created_at.isoformat()
