# Arquitetura

```
src/f1/
├── config.py     # BASE_URL, CAR_DATA_ENDPOINT e TIMEOUT_SECONDS (30 s)
├── client.py     # get_car_data/laps/meetings/sessions/race_sessions/drivers; OpenF1Error
├── models.py     # dataclass imutável CarData
├── transform.py  # parse_date, to_car_data, clean; InvalidRecordError
├── analysis.py   # max_speed, count_above_speed, drs_open_ratio, fastest_laps, format_lap_time
├── catalog.py    # rótulos e ordenação de provas, sessões e pilotos
├── cli.py        # linha de comando (python -m f1.cli)
└── app.py        # dashboard Streamlit
tests/            # testes unitários (sem rede)
docs/             # esta documentação
```

## Fluxo de dados

```
OpenF1 ──► client ──► transform ──► analysis ──► cli / app
          (JSON bruto) (CarData)   (métricas)
```

1. `client` faz a requisição e devolve a lista de dicionários da API.
2. `transform` valida cada leitura de telemetria (data ISO 8601, campos inteiros presentes, `throttle` entre 0 e 100, `brake` igual a 0 ou 100) e descarta as inválidas silenciosamente.
3. `analysis` agrega os dados limpos. `fastest_laps` trabalha direto sobre os dicionários de `laps` e `drivers`, sem passar por `transform`.
4. `cli` e `app` apresentam o resultado. `catalog` fornece os textos exibidos nos seletores.

## Tratamento de erros

- Falha de rede, timeout, status HTTP de erro, JSON inválido ou resposta que não seja lista levantam `OpenF1Error`.
- A OpenF1 responde **404 com "No results found"** para consultas válidas sem dados; o cliente trata isso como lista vazia.
- CLI e dashboard capturam `OpenF1Error` e mostram a mensagem (stderr com código 1 na CLI; `st.error` no dashboard).

## Decisões de projeto

- A telemetria é representada por dataclasses puras (`CarData`) nos módulos de domínio.
- `pandas` é usado **apenas** em `app.py`, para tabelas e gráficos. Não é dependência declarada: vem junto com o `streamlit`.
- Sem filtro de velocidade a API retorna milhares de leituras por sessão; prefira filtros.
