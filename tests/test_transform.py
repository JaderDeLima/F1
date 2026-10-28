from datetime import datetime

import pytest

from f1.transform import InvalidRecordError, clean, parse_date, to_car_data

RECORD = {
    "date": "2023-09-15T13:08:19.923000+00:00",
    "session_key": 9159,
    "meeting_key": 1219,
    "driver_number": 55,
    "n_gear": 8,
    "speed": 315,
    "rpm": 11141,
    "throttle": 99,
    "brake": 0,
    "drs": 12,
}


def test_to_car_data_normal():
    item = to_car_data(RECORD)
    assert item.speed == 315
    assert item.date == datetime.fromisoformat("2023-09-15T13:08:19.923+00:00")


@pytest.mark.parametrize("value", [None, 123, "ontem"])
def test_parse_date_invalid(value):
    with pytest.raises(InvalidRecordError):
        parse_date(value)


@pytest.mark.parametrize(
    "change",
    [
        {"speed": None},
        {"rpm": "alto"},
        {"drs": True},
        {"throttle": 101},
        {"throttle": -1},
        {"brake": 50},
        {"date": "xx"},
    ],
)
def test_to_car_data_invalid(change):
    with pytest.raises(InvalidRecordError):
        to_car_data({**RECORD, **change})


def test_missing_field():
    record = {k: v for k, v in RECORD.items() if k != "speed"}
    with pytest.raises(InvalidRecordError, match="speed"):
        to_car_data(record)


def test_clean_discards_invalid():
    result = clean([RECORD, {**RECORD, "brake": 7}])
    assert len(result) == 1
