from f1.catalog import (
    driver_label,
    meeting_label,
    session_label,
    sort_drivers,
    sort_meetings,
)


def test_meeting_label():
    meeting = {
        "meeting_name": "Singapore Grand Prix",
        "location": "Marina Bay",
        "country_name": "Singapore",
    }
    assert meeting_label(meeting) == "Singapore Grand Prix — Marina Bay, Singapore"


def test_meeting_label_without_place():
    assert meeting_label({"meeting_name": "Teste"}) == "Teste"


def test_session_label():
    assert session_label({"session_name": "Race"}) == "Race"


def test_driver_label():
    driver = {"full_name": "Carlos SAINZ", "team_name": "Ferrari"}
    assert driver_label(driver) == "Carlos SAINZ (Ferrari)"


def test_driver_label_fallback_to_number():
    assert driver_label({"driver_number": 55}) == "#55"


def test_sorting():
    assert [
        m["date_start"]
        for m in sort_meetings([{"date_start": "2023-03"}, {"date_start": "2023-01"}])
    ] == ["2023-01", "2023-03"]
    assert [
        d["full_name"] for d in sort_drivers([{"full_name": "B"}, {"full_name": "A"}])
    ] == ["A", "B"]
