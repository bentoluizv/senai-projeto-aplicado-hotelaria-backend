from datetime import datetime

import pytest

from app.utils.time_in_range import time_in_range


@pytest.mark.parametrize(
    ('actual', 'expected_in_range'),
    [
        (datetime(2000, 2, 2, 2, 30), True),  # within range
        (datetime(2000, 2, 1, 8, 30), True),  # exactly at start
        (datetime(2000, 2, 3, 17, 30), True),  # exactly at end
        (datetime(2000, 2, 4, 10, 0), False),  # outside range
        (datetime(2000, 1, 31, 23, 59), False),  # before range
    ],
)
def test_time_in_range(actual, expected_in_range):
    start = datetime(2000, 2, 1, 8, 30)
    end = datetime(2000, 2, 3, 17, 30)
    is_in_range = time_in_range(start, end, actual)
    assert is_in_range == expected_in_range
