from fastapi import HTTPException


class OutOfRangeError(HTTPException):
    def __init__(self, page: int, total_pages: int):
        detail = (
            f'Page {page} is out of range. There are only {total_pages} pages.'
        )
        super().__init__(status_code=400, detail=detail)
