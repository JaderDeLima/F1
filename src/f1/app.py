"""Dashboard Streamlit: ``poetry run task dash``."""

from datetime import date, datetime, timezone

import pandas as pd
import streamlit as st

from f1.analysis import (
    count_above_speed,
    drs_open_ratio,
    fastest_laps,
    max_speed,
)
from f1.catalog import (
    driver_label,
    meeting_label,
    session_label,
    sort_drivers,
    sort_meetings,
)
from f1.client import (
    OpenF1Error,
    get_car_data,
    get_drivers,
    get_laps,
    get_meetings,
    get_race_sessions,
    get_sessions,
)
from f1.models import CarData
from f1.transform import clean


@st.cache_data(ttl=600, show_spinner="Consultando a OpenF1...")
def load(session: int, driver: int, min_speed: int) -> list[CarData]:
    filters = {"speed>=": min_speed} if min_speed > 0 else {}
    return clean(get_car_data(session, driver, **filters))


@st.cache_data(ttl=3600)
def load_meetings(year: int) -> list[dict]:
    return sort_meetings(get_meetings(year))


@st.cache_data(ttl=3600)
def load_sessions(meeting_key: int) -> list[dict]:
    now = datetime.now(timezone.utc)

    def started(session: dict) -> bool:
        if not session.get("date_start"):
            return True
        start = datetime.fromisoformat(session["date_start"])
        return start.replace(tzinfo=start.tzinfo or timezone.utc) <= now

    return [s for s in get_sessions(meeting_key) if started(s)]


@st.cache_data(ttl=3600)
def load_drivers(session_key: int) -> list[dict]:
    return sort_drivers(get_drivers(session_key))


@st.cache_data(ttl=3600, show_spinner="Consultando voltas de todas as corridas...")
def load_season_fastest(year: int) -> list[dict]:
    """Top 5 voltas de cada corrida já realizada do ano, em ordem de calendário."""
    now = datetime.now(timezone.utc)
    races = sorted(get_race_sessions(year), key=lambda s: s.get("date_start", ""))
    rows: list[dict] = []
    for race in races:
        start = datetime.fromisoformat(race["date_start"])
        if start.replace(tzinfo=start.tzinfo or timezone.utc) > now:
            continue
        top = fastest_laps(
            get_laps(race["session_key"]), get_drivers(race["session_key"])
        )
        circuit = race.get("circuit_short_name") or race.get("location", "")
        rows += [{"Circuito": circuit, **row} for row in top]
    return rows


def to_frame(data: list[CarData]) -> pd.DataFrame:
    frame = pd.DataFrame([vars(d) for d in data])
    return frame.set_index("date").sort_index()


def main() -> None:
    st.set_page_config(page_title="F1 Telemetria", layout="wide")
    st.title("F1 — Telemetria (OpenF1)")

    with st.sidebar:
        try:
            year = st.selectbox("Temporada", range(date.today().year, 2022, -1))
            meetings = load_meetings(year)
            meeting = st.selectbox("Prova", meetings, format_func=meeting_label)
            sessions = load_sessions(meeting["meeting_key"]) if meeting else []
            session = st.selectbox("Sessão", sessions, format_func=session_label)
            drivers = load_drivers(session["session_key"]) if session else []
            driver = st.selectbox("Piloto", drivers, format_func=driver_label)
        except OpenF1Error as exc:
            st.error(str(exc))
            return
        min_speed = st.number_input("Velocidade mínima (km/h)", min_value=0, value=0)

    st.header(f"5 voltas mais rápidas por circuito — {year}")
    try:
        ranking = load_season_fastest(year)
    except OpenF1Error as exc:
        st.error(str(exc))
        return
    if ranking:
        st.dataframe(pd.DataFrame(ranking), hide_index=True, height=400)
    else:
        st.info("Sem voltas cronometradas nesta temporada.")
    st.divider()
    st.header("Telemetria")

    if not driver:
        st.warning("Selecione uma prova, sessão e piloto com dados disponíveis.")
        return

    try:
        data = load(session["session_key"], driver["driver_number"], int(min_speed))
    except OpenF1Error as exc:
        st.error(str(exc))
        return
    if not data:
        st.warning("Nenhum registro encontrado para esses filtros.")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Velocidade máxima (km/h)", max_speed(data))
    col2.metric("Leituras ≥ 300 km/h", count_above_speed(data, 300))
    col3.metric("DRS aberto", f"{drs_open_ratio(data):.1%}")

    frame = to_frame(data)
    st.subheader("Velocidade (km/h)")
    st.line_chart(frame["speed"])
    st.subheader("Acelerador (%)")
    st.line_chart(frame["throttle"])
    st.subheader("Marcha")
    st.line_chart(frame["n_gear"])
    st.subheader("Rotação (rpm)")
    st.line_chart(frame["rpm"])
    with st.expander("Dados"):
        st.dataframe(frame)


main()
