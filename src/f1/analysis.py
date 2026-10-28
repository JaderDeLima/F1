"""Agregações simples sobre telemetria."""

from collections.abc import Sequence
from typing import Any

from f1.catalog import driver_label
from f1.models import CarData

# Códigos de DRS aberto (10, 12 e 14).
DRS_OPEN_CODES = frozenset({10, 12, 14})


def fastest_laps(
    laps: Sequence[dict[str, Any]], drivers: Sequence[dict[str, Any]], top: int = 5
) -> list[dict[str, Any]]:
    """As ``top`` voltas mais rápidas, com o piloto de cada uma."""
    names = {d["driver_number"]: driver_label(d) for d in drivers}
    timed = [lap for lap in laps if lap.get("lap_duration")]
    timed.sort(key=lambda lap: lap["lap_duration"])
    return [
        {
            "Posição": pos,
            "Piloto": names.get(lap["driver_number"], f"#{lap['driver_number']}"),
            "Volta": lap.get("lap_number"),
            "Tempo": format_lap_time(lap["lap_duration"]),
        }
        for pos, lap in enumerate(timed[:top], start=1)
    ]


def format_lap_time(seconds: float) -> str:
    """Ex.: ``1:32.456``."""
    minutes, rest = divmod(seconds, 60)
    return f"{int(minutes)}:{rest:06.3f}"


def max_speed(data: Sequence[CarData]) -> int | None:
    """Maior velocidade (km/h), ou ``None`` se não houver dados."""
    return max((d.speed for d in data), default=None)


def count_above_speed(data: Sequence[CarData], threshold: int) -> int:
    """Quantidade de leituras com velocidade >= ``threshold``."""
    return sum(1 for d in data if d.speed >= threshold)


def drs_open_ratio(data: Sequence[CarData]) -> float:
    """Fração de leituras com DRS aberto (0.0 se não houver dados)."""
    if not data:
        return 0.0
    return sum(1 for d in data if d.drs in DRS_OPEN_CODES) / len(data)
