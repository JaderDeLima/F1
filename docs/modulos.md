# Módulos

Referência das funções públicas de `src/f1/`.

## `f1.config`

| Constante | Valor |
|---|---|
| `BASE_URL` | `https://api.openf1.org/v1` |
| `CAR_DATA_ENDPOINT` | `car_data` |
| `TIMEOUT_SECONDS` | `30` |

## `f1.client`

Todas as funções retornam `list[dict]` e levantam `OpenF1Error` em caso de falha.

| Função | Endpoint | Parâmetros |
|---|---|---|
| `get_car_data(session_key, driver_number, **filters)` | `car_data` | filtros com operador, ex.: `{"speed>=": 315}` |
| `get_laps(session_key)` | `laps` | voltas de todos os pilotos |
| `get_meetings(year)` | `meetings` | eventos do ano (GPs e testes) |
| `get_sessions(meeting_key)` | `sessions` | sessões de um evento |
| `get_race_sessions(year)` | `sessions` | `session_name=Race`, uma por circuito |
| `get_drivers(session_key)` | `drivers` | pilotos de uma sessão |

## `f1.models`

`CarData` (dataclass imutável): `date` (`datetime`), `session_key`, `meeting_key`, `driver_number`, `n_gear`, `speed`, `rpm`, `throttle`, `brake`, `drs`.

## `f1.transform`

| Função | Descrição |
|---|---|
| `parse_date(value)` | ISO 8601 → `datetime`; levanta `InvalidRecordError` se não for texto válido |
| `to_car_data(record)` | Valida e converte um registro em `CarData` |
| `clean(records)` | Converte a lista, descartando os inválidos |

Regras de validação: todos os campos inteiros presentes (booleanos são rejeitados), `throttle` entre 0 e 100 e `brake` igual a 0 ou 100.

## `f1.analysis`

| Função | Descrição |
|---|---|
| `max_speed(data)` | Maior velocidade (km/h) ou `None` sem dados |
| `count_above_speed(data, threshold)` | Leituras com `speed >= threshold` |
| `drs_open_ratio(data)` | Fração de leituras com DRS aberto (`0.0` sem dados) |
| `fastest_laps(laps, drivers, top=5)` | As `top` voltas mais rápidas, com posição, piloto, volta e tempo |
| `format_lap_time(seconds)` | `92.456` → `1:32.456` |

DRS é considerado aberto nos códigos **10, 12 e 14** (`DRS_OPEN_CODES`). Voltas sem `lap_duration` são ignoradas.

## `f1.catalog`

| Função | Exemplo de saída |
|---|---|
| `meeting_label` | `Singapore Grand Prix — Marina Bay, Singapore` |
| `session_label` | `Practice 2` |
| `driver_label` | `Carlos SAINZ (Ferrari)` (sem nome, usa `#<número>`) |
| `sort_meetings` | ordena por `date_start` |
| `sort_drivers` | ordena por `full_name` |
