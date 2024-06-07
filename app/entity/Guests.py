from datetime import datetime

from pydantic import Field, model_validator

from app.utils.is_valid_cpf import is_valid_cpf
from app.utils.StrictModel import StrictModel


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
