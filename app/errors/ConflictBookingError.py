from datetime import datetime

from fastapi import HTTPException

from app.entities.Booking import Booking


class ConflictBookingError(HTTPException):
    def __init__(
        self, booking: Booking, check_in: datetime, check_out: datetime
    ):
        detail = f"""
        Conflict!!! {booking.model_dump_json()}
        with {check_in.isoformat()} and {check_out.isoformat()}
        """
        super().__init__(status_code=409, detail=detail)
