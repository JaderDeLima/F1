"""Validação e limpeza dos registros brutos."""

from datetime import datetime
from typing import Any

from f1.models import CarData

_INT_FIELDS = (
    "session_key",
    "meeting_key",
    "driver_number",
    "n_gear",
    "speed",
    "rpm",
    "throttle",
    "brake",
    "drs",
)


class InvalidRecordError(ValueError):
    """Registro de telemetria inválido."""


def parse_date(value: Any) -> datetime:
    """Converte data ISO 8601 em datetime."""
    if not isinstance(value, str):
        raise InvalidRecordError(f"data inválida: {value!r}")
    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise InvalidRecordError(f"data inválida: {value!r}") from exc


def to_car_data(record: dict[str, Any]) -> CarData:
    """Valida um registro bruto e o converte em ``CarData``."""
    values: dict[str, Any] = {"date": parse_date(record.get("date"))}
    for field in _INT_FIELDS:
        raw = record.get(field)
        if raw is None:
            raise InvalidRecordError(f"campo ausente: {field}")
        if isinstance(raw, bool) or not isinstance(raw, int):
            raise InvalidRecordError(f"campo {field} não é inteiro: {raw!r}")
        values[field] = raw
    if not 0 <= values["throttle"] <= 100:
        raise InvalidRecordError(f"throttle fora de 0-100: {values['throttle']}")
    if values["brake"] not in (0, 100):
        raise InvalidRecordError(f"brake deve ser 0 ou 100: {values['brake']}")
    return CarData(**values)


def clean(records: list[dict[str, Any]]) -> list[CarData]:
    """Converte registros, descartando os inválidos."""
    result = []
    for record in records:
        try:
            result.append(to_car_data(record))
        except InvalidRecordError:
            continue
    return result
