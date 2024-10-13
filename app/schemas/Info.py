from pydantic import BaseModel


class Info(BaseModel):
    count: int = 0
    total_pages: int = 1
