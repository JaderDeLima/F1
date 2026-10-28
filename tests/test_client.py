import pytest
import requests
import responses

from f1.client import (
    OpenF1Error,
    get_car_data,
    get_drivers,
    get_meetings,
    get_sessions,
)
from f1.config import BASE_URL

URL = f"{BASE_URL}/car_data"
RECORDS = [
    {"date": "2023-09-15T13:08:19.923000+00:00", "speed": 315},
    {"date": "2023-09-15T13:35:41.808000+00:00", "speed": 315},
]


@responses.activate
def test_get_car_data_builds_query_with_operator():
    responses.get(URL, json=RECORDS)
    data = get_car_data(9159, 55, **{"speed>=": 315})
    assert data == RECORDS
    query = responses.calls[0].request.params
    assert query["session_key"] == "9159"
    assert query["driver_number"] == "55"
    assert query["speed>="] == "315"


@responses.activate
def test_empty_list():
    responses.get(URL, json=[])
    assert get_car_data(1, 2) == []


@responses.activate
def test_404_no_results_is_empty():
    responses.get(URL, status=404, json={"detail": "No results found."})
    assert get_car_data(1, 2) == []


@responses.activate
@pytest.mark.parametrize("status", [404, 500])
def test_http_error(status):
    responses.get(URL, status=status)
    with pytest.raises(OpenF1Error):
        get_car_data(1, 2)


@responses.activate
def test_timeout():
    responses.get(URL, body=requests.Timeout("lento"))
    with pytest.raises(OpenF1Error):
        get_car_data(1, 2)


@responses.activate
def test_invalid_json():
    responses.get(URL, body="<html>")
    with pytest.raises(OpenF1Error, match="JSON"):
        get_car_data(1, 2)


@responses.activate
def test_non_list_json():
    responses.get(URL, json={"detail": "x"})
    with pytest.raises(OpenF1Error, match="lista"):
        get_car_data(1, 2)


@responses.activate
@pytest.mark.parametrize(
    ("func", "endpoint", "param"),
    [
        (get_meetings, "meetings", "year"),
        (get_sessions, "sessions", "meeting_key"),
        (get_drivers, "drivers", "session_key"),
    ],
)
def test_catalog_endpoints(func, endpoint, param):
    responses.get(f"{BASE_URL}/{endpoint}", json=[{"x": 1}])
    assert func(2023) == [{"x": 1}]
    assert responses.calls[0].request.params[param] == "2023"
