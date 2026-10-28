from contextlib import ExitStack
from unittest.mock import patch

import streamlit as st
from streamlit.testing.v1 import AppTest

from f1.client import OpenF1Error

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
MEETINGS = [
    {
        "meeting_key": 1219,
        "meeting_name": "Singapore Grand Prix",
        "location": "Marina Bay",
        "country_name": "Singapore",
        "date_start": "2023-09-15",
    }
]
SESSIONS = [{"session_key": 9159, "session_name": "Practice 2"}]
DRIVERS = [{"driver_number": 55, "full_name": "Carlos SAINZ", "team_name": "Ferrari"}]


def run_app(car_data=None, car_error=None, drivers=DRIVERS, meetings_error=None):
    st.cache_data.clear()
    with ExitStack() as stack:
        stack.enter_context(
            patch(
                "f1.client.get_meetings",
                return_value=MEETINGS,
                side_effect=meetings_error,
            )
        )
        stack.enter_context(patch("f1.client.get_sessions", return_value=SESSIONS))
        stack.enter_context(patch("f1.client.get_drivers", return_value=drivers))
        stack.enter_context(patch("f1.client.get_race_sessions", return_value=[]))
        stack.enter_context(patch("f1.client.get_laps", return_value=[]))
        stack.enter_context(
            patch(
                "f1.client.get_car_data",
                return_value=car_data or [],
                side_effect=car_error,
            )
        )
        return AppTest.from_file("../src/f1/app.py", default_timeout=30).run()


def test_app_shows_metrics_and_friendly_labels():
    at = run_app(car_data=[RECORD])
    assert not at.exception
    assert at.metric[0].value == "315"
    labels = {s.label: s.format_func(s.value) for s in at.selectbox}
    assert labels["Prova"] == "Singapore Grand Prix — Marina Bay, Singapore"
    assert labels["Sessão"] == "Practice 2"
    assert labels["Piloto"] == "Carlos SAINZ (Ferrari)"


def test_app_shows_error():
    at = run_app(car_error=OpenF1Error("falhou"))
    assert at.error[0].value == "falhou"


def test_app_empty():
    at = run_app(car_data=[])
    assert len(at.warning) == 1


def test_app_no_drivers():
    at = run_app(drivers=[])
    assert len(at.warning) == 1


def test_app_catalog_error():
    at = run_app(meetings_error=OpenF1Error("sem rede"))
    assert at.error[0].value == "sem rede"
