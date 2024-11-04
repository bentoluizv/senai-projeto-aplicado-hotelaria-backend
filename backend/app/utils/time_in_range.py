from datetime import datetime


def time_in_range(start: datetime, end: datetime, actual: datetime):
    if start <= end:
        return start <= actual <= end
    else:
        return start <= actual or actual <= end
