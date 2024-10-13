from pydantic import BaseModel


class RepositorySettings(BaseModel):
    pagination: int = 10
