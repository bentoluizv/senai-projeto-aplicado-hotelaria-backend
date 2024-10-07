from datetime import datetime


def calculate_budget(
    check_in: datetime, check_out: datetime, daily_rate: float
):
    num_days = (check_out - check_in).days
    budget = num_days * daily_rate

    return budget
