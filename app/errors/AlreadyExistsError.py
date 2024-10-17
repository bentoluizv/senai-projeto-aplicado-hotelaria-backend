from fastapi import HTTPException


class AlreadyExistsError(HTTPException):
    def __init__(self, entity: str, field: str, value: str):
        detail = f"{entity} with {field} '{value}' already exists."
        super().__init__(status_code=409, detail=detail)
