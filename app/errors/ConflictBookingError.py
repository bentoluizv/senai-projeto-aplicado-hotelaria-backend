from datetime import datetime

from fastapi import HTTPException


class ConflictBookingError(HTTPException):
    def __init__(self, entity: str, check_in: datetime, check_out: datetime):
        detail = f"""
        Conflict {entity} with {check_in.strftime} and {check_out.strftime}
        """
        super().__init__(status_code=409, detail=detail)
