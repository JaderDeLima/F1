"""Modelos de dados."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CarData:
    """Uma leitura de telemetria do carro."""

    date: datetime
    session_key: int
    meeting_key: int
    driver_number: int
    n_gear: int
    speed: int
    rpm: int
    throttle: int
    brake: int
    drs: int
