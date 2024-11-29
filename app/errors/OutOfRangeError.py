from fastapi import HTTPException


class OutOfRangeError(HTTPException):
    def __init__(self, page: int, total_pages: int):
        detail = (
            f'Página {page} fora do range. Máximo de {total_pages} páginas.'
        )
        super().__init__(status_code=400, detail=detail)
