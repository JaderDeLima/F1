# OpenF1 API – `car_data`

Resumo da chamada:

```
https://api.openf1.org/v1/car_data?driver_number=55&session_key=9159&speed>=315
```

## 1. Visão geral

O endpoint `/v1/car_data` da API OpenF1 retorna a telemetria do carro (velocidade, rotação, marcha, acelerador, freio e DRS) para um piloto em uma sessão. A resposta é um array JSON, sem necessidade de autenticação.

## 2. Parâmetros usados

| Parâmetro | Valor | Significado |
|---|---|---|
| `driver_number` | 55 | Número do piloto |
| `session_key` | 9159 | Sessão específica (meeting_key 1219) |
| `speed>=315` | 315 | Filtro: apenas leituras com velocidade ≥ 315 km/h |

Os filtros são passados via query string e aceitam operadores de comparação (`>=`, `<=`, `>`, `<`).

## 3. Campos da resposta

| Campo | Tipo | Descrição |
|---|---|---|
| `date` | string (ISO 8601, UTC) | Momento da leitura |
| `session_key` | inteiro | Identificador da sessão |
| `meeting_key` | inteiro | Identificador do evento (GP) |
| `driver_number` | inteiro | Número do piloto |
| `n_gear` | inteiro | Marcha engatada |
| `speed` | inteiro | Velocidade (km/h) |
| `rpm` | inteiro | Rotação do motor |
| `throttle` | inteiro | Acelerador (0–100 %) |
| `brake` | inteiro | Freio (0 ou 100, tipo on/off) |
| `drs` | inteiro | Código de estado do DRS (ex.: 8 e 12; o projeto considera aberto nos códigos 10, 12 e 14) |

## 4. Resultado observado

A consulta retornou **2 registros**, ambos em 2023-09-15:

| date (UTC) | speed | n_gear | rpm | throttle | brake | drs |
|---|---|---|---|---|---|---|
| 13:08:19.923 | 315 | 8 | 11141 ou 11023* | 99 ou 57* | 0 ou 100* | 12 ou 8* |
| 13:35:41.808 | 315 | 8 | 11141 ou 11023* | 99 ou 57* | 0 ou 100* | 12 ou 8* |

\* A resposta resumida pela ferramenta de leitura não atribuiu de forma confiável cada valor a um registro; os intervalos observados foram: rpm 11023–11141, throttle 57–99, brake 0–100, drs 8–12. Para os valores exatos por registro, consulte a URL diretamente.

Em ambos: `speed` = 315, `n_gear` = 8, `meeting_key` = 1219, `driver_number` = 55, `session_key` = 9159. Intervalo entre as leituras: ~27 min 22 s.

## 5. Exemplo de uso

```bash
curl "https://api.openf1.org/v1/car_data?driver_number=55&session_key=9159&speed>=315"
```

```python
import requests

url = "https://api.openf1.org/v1/car_data"
params = {"driver_number": 55, "session_key": 9159, "speed>=": 315}
dados = requests.get(url, params=params).json()
print(len(dados), dados[0])
```

## 6. Observações

- Resposta em JSON; filtros combinam-se com `&`.
- Sem filtro de `speed`, o endpoint retorna milhares de leituras por sessão (alta frequência), então filtrar reduz muito o volume.
- Consultas válidas sem resultado retornam **HTTP 404** com "No results found"; o cliente (`f1.client`) trata isso como lista vazia.

## 7. Outros endpoints usados

Base: `https://api.openf1.org/v1`. Usados pelo dashboard e expostos em `f1.client`.

| Endpoint | Parâmetros | Função | Campos lidos |
|---|---|---|---|
| `meetings` | `year` | `get_meetings` | `meeting_key`, `meeting_name`, `location`, `country_name`, `date_start` |
| `sessions` | `meeting_key` | `get_sessions` | `session_key`, `session_name`, `date_start` |
| `sessions` | `year`, `session_name=Race` | `get_race_sessions` | `session_key`, `date_start`, `circuit_short_name`, `location` |
| `drivers` | `session_key` | `get_drivers` | `driver_number`, `full_name`, `team_name` |
| `laps` | `session_key` | `get_laps` | `driver_number`, `lap_number`, `lap_duration` (segundos) |

Os dados cobrem as temporadas a partir de 2023. `date_start` é ISO 8601 e é usado para ordenar e para ignorar sessões ainda não iniciadas.
