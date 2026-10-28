# Uso

## Atalhos

| Comando | Ação |
|---|---|
| `poetry run task dash` | Abre o [dashboard](dashboard.md) |
| `poetry run task docs` | Serve esta documentação em http://127.0.0.1:8000 |
| `poetry run task test` | Testes com cobertura |
| `poetry run task lint` | Verifica Ruff (lint e formatação) |
| `poetry run task format` | Corrige lint e formata |

## Linha de comando

Acessa a rede.

```bash
poetry run python -m f1.cli --driver 55 --session 9159 --min-speed 315
```

| Opção | Obrigatória | Descrição |
|---|---|---|
| `--driver` | sim | Número do piloto (`driver_number`) |
| `--session` | sim | Chave da sessão (`session_key`) |
| `--min-speed` | não | Filtra leituras com `speed >=` o valor (km/h) |

Para o exemplo acima a saída traz as leituras com `speed=315` e `n_gear=8`, seguidas do resumo `N registros; velocidade máxima: ...`. Em caso de erro da API, imprime `Erro: ...` no stderr e sai com código 1.

Sem `--min-speed` a API retorna milhares de leituras, e todas são impressas.

## Como biblioteca

```python
from f1.analysis import max_speed
from f1.client import get_car_data
from f1.transform import clean

raw = get_car_data(9159, 55, **{"speed>=": 315})
data = clean(raw)
print(max_speed(data))
```

Os filtros extras usam o operador na chave, como `"speed>="`.

## Dashboard

```bash
poetry run task dash
```

Abre em http://localhost:8501. Detalhes em [Dashboard](dashboard.md).
