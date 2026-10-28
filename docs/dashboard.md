# Dashboard

Aplicativo Streamlit em `src/f1/app.py`. Executa-se com `poetry run task dash` (`streamlit run src/f1/app.py`) e abre em http://localhost:8501. Acessa a rede.

## Barra lateral

Os seletores são encadeados; cada um depende do anterior.

| Seletor | Origem | Observação |
|---|---|---|
| Temporada | ano atual até 2023 | A OpenF1 só tem dados a partir de 2023 |
| Prova | `meetings` do ano | Ordenadas por data; rótulo como "Singapore Grand Prix — Marina Bay, Singapore" |
| Sessão | `sessions` da prova | Só sessões que já começaram (ex.: "Practice 2") |
| Piloto | `drivers` da sessão | Ordenados por nome; rótulo como "Carlos SAINZ (Ferrari)" |
| Velocidade mínima (km/h) | campo numérico | `0` desativa o filtro; senão envia `speed>=` à API |

Os números `meeting_key`, `session_key` e `driver_number` são resolvidos automaticamente.

## Conteúdo principal

1. **5 voltas mais rápidas por circuito** da temporada selecionada: tabela com circuito, posição, piloto, volta e tempo (`m:ss.mmm`). Considera apenas corridas (`session_name=Race`) que já aconteceram, em ordem de calendário. Faz uma consulta de `laps` e `drivers` por corrida, então a primeira carga é lenta.
2. **Telemetria** do piloto escolhido:
    - métricas: velocidade máxima, leituras ≥ 300 km/h e percentual de DRS aberto;
    - gráficos de velocidade, acelerador, marcha e rotação ao longo do tempo;
    - expansor "Dados" com a tabela completa.

## Mensagens

| Situação | Mensagem |
|---|---|
| Erro na API (nos seletores, no ranking ou na telemetria) | `st.error` com o texto de `OpenF1Error` |
| Ranking sem voltas cronometradas | "Sem voltas cronometradas nesta temporada." |
| Sem piloto selecionado (prova futura ou sem dados) | "Selecione uma prova, sessão e piloto com dados disponíveis." |
| Telemetria vazia para os filtros | "Nenhum registro encontrado para esses filtros." |

## Cache

As consultas usam `st.cache_data`:

| Função | TTL |
|---|---|
| `load` (telemetria) | 10 min |
| `load_meetings`, `load_sessions`, `load_drivers`, `load_season_fastest` | 1 h |
