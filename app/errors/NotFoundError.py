from fastapi import HTTPException


class NotFoundError(HTTPException):
    def __init__(self, entity: str, entity_id: str):
        detail = f"{entity} com o ID '{entity_id}' não encontrada!"
        super().__init__(status_code=404, detail=detail)
