from pydantic import BaseModel


class GuestUpdateDTO(BaseModel):
    document: str | None = None
    name: str | None = None
    surname: str | None = None
    phone: str | None = None
    country: str | None = None


class GuestCreateDTO(BaseModel):
    document: str
    name: str
    surname: str
    phone: str
    country: str


class Guest(BaseModel):
    document: str
    name: str
    surname: str
    phone: str
    country: str

    @classmethod
    def create(cls, dto: GuestCreateDTO):
        return cls(
            document=dto.document,
            name=dto.name,
            surname=dto.surname,
            phone=dto.phone,
            country=dto.country,
        )

    def update(self, dto: GuestUpdateDTO):
        dto_as_dict = dto.model_dump()

        for field, value in dto_as_dict.items():
            if value is not None:
                setattr(self, field, value)
