from pydantic import BaseModel, ConfigDict


class StrictModel(BaseModel):
    model_config = ConfigDict(
        frozen=True, str_strip_whitespace=True, strict=True
    )
