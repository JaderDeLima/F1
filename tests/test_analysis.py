from datetime import UTC, datetime

from f1.analysis import count_above_speed, drs_open_ratio, max_speed
from f1.models import CarData


def make(speed, drs):
    when = datetime(2023, 9, 15, tzinfo=UTC)
    return CarData(when, 1, 2, 55, 8, speed, 11000, 99, 0, drs)


DATA = [make(300, 12), make(315, 8), make(320, 10), make(100, 0)]


def test_max_speed():
    assert max_speed(DATA) == 320


def test_max_speed_empty():
    assert max_speed([]) is None


def test_count_above_speed():
    assert count_above_speed(DATA, 315) == 2


def test_drs_open_ratio():
    assert drs_open_ratio(DATA) == 0.5


def test_drs_open_ratio_empty():
    assert drs_open_ratio([]) == 0.0
