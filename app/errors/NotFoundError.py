from fastapi import HTTPException


class NotFoundError(HTTPException):
    def __init__(self, entity: str, entity_id: str):
        detail = f"{entity} with ID '{entity_id}' not found."
        super().__init__(status_code=404, detail=detail)
