from fastapi import HTTPException


class AlreadyExistsError(HTTPException):
    def __init__(self, entity: str, field: str, value: str):
        detail = f"{entity} com {field} '{value}' já existe!"
        super().__init__(status_code=409, detail=detail)
