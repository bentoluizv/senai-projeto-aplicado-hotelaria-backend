from datetime import datetime

from pydantic import BaseModel


class Pagination(BaseModel):
    page: int = 1
    per_page: int = 10


class ListFilter(BaseModel):
    check_in: datetime
    check_out: datetime


class ListSettings(BaseModel):
    pagination: Pagination
    filter: ListFilter | None = None
