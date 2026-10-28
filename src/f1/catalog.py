"""Rótulos legíveis para eventos, sessões e pilotos da OpenF1."""

from typing import Any


def meeting_label(meeting: dict[str, Any]) -> str:
    """Ex.: ``Singapore Grand Prix — Marina Bay, Singapore``."""
    name = meeting.get("meeting_name", "Evento")
    place = ", ".join(
        str(p) for p in (meeting.get("location"), meeting.get("country_name")) if p
    )
    return f"{name} — {place}" if place else name


def session_label(session: dict[str, Any]) -> str:
    return session.get("session_name", "Sessão")


def driver_label(driver: dict[str, Any]) -> str:
    """Ex.: ``Carlos SAINZ (Ferrari)``."""
    name = driver.get("full_name") or f"#{driver.get('driver_number')}"
    team = driver.get("team_name")
    return f"{name} ({team})" if team else name


def sort_meetings(meetings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(meetings, key=lambda m: m.get("date_start", ""))


def sort_drivers(drivers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(drivers, key=lambda d: d.get("full_name") or "")
