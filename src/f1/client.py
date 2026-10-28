"""Cliente HTTP da API OpenF1 (endpoint car_data)."""

from typing import Any

import requests

from f1.config import BASE_URL, CAR_DATA_ENDPOINT, TIMEOUT_SECONDS


class OpenF1Error(Exception):
    """Erro ao consultar a API OpenF1."""


def _get(endpoint: str, **params: Any) -> list[dict[str, Any]]:
    url = f"{BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, params=params, timeout=TIMEOUT_SECONDS)
        if response.status_code == 404 and "No results found" in response.text:
            # A OpenF1 usa 404 para consultas válidas sem dados.
            return []
        response.raise_for_status()
    except requests.RequestException as exc:
        raise OpenF1Error(f"Falha na requisição à OpenF1: {exc}") from exc
    try:
        data = response.json()
    except ValueError as exc:
        raise OpenF1Error("Resposta da OpenF1 não é JSON válido") from exc
    if not isinstance(data, list):
        raise OpenF1Error("Resposta da OpenF1 não é uma lista")
    return data


def get_car_data(
    session_key: int, driver_number: int, **filters: Any
) -> list[dict[str, Any]]:
    """Busca telemetria bruta de um piloto em uma sessão.

    Filtros extras usam a chave com operador, ex.: ``**{"speed>=": 315}``.
    Sem filtro de velocidade a API retorna milhares de leituras por sessão.
    """
    return _get(
        CAR_DATA_ENDPOINT,
        session_key=session_key,
        driver_number=driver_number,
        **filters,
    )


def get_laps(session_key: int) -> list[dict[str, Any]]:
    """Lista as voltas de todos os pilotos de uma sessão."""
    return _get("laps", session_key=session_key)


def get_meetings(year: int) -> list[dict[str, Any]]:
    """Lista os eventos (GPs e testes) de um ano."""
    return _get("meetings", year=year)


def get_sessions(meeting_key: int) -> list[dict[str, Any]]:
    """Lista as sessões de um evento."""
    return _get("sessions", meeting_key=meeting_key)


def get_race_sessions(year: int) -> list[dict[str, Any]]:
    """Lista as corridas (sessão ``Race``) de um ano, uma por circuito."""
    return _get("sessions", year=year, session_name="Race")


def get_drivers(session_key: int) -> list[dict[str, Any]]:
    """Lista os pilotos de uma sessão."""
    return _get("drivers", session_key=session_key)
