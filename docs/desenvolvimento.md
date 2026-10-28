# Desenvolvimento

## Atalhos (taskipy)

Definidos em `[tool.taskipy.tasks]` no `pyproject.toml`:

| Comando | Ação |
|---|---|
| `poetry run task test` | `pytest` (com cobertura mínima de 50%) |
| `poetry run task lint` | `ruff check .` e `ruff format --check .` |
| `poetry run task format` | `ruff check . --fix` e `ruff format .` |
| `poetry run task docs` | `mkdocs serve` |
| `poetry run task dash` | dashboard Streamlit (`src/f1/app.py`) |

## Ruff

Lint e formatação com Ruff (`line-length = 88`, `target-version = "py312"`). Regras selecionadas: `E`, `F`, `W` (pycodestyle/pyflakes), `I` (imports), `B` (bugbear), `UP` (pyupgrade), `N` (nomes), `SIM` (simplificações).

```bash
poetry run ruff check .
poetry run ruff format --check .
```

## Testes e cobertura

Pytest com cobertura mínima de 50% de `src/f1/` (`--cov-fail-under=50`, configurado em `addopts`). Os testes não usam rede: o HTTP é simulado com `responses`.

```bash
poetry run pytest
poetry run pytest -o addopts="" tests/test_client.py   # teste isolado, sem cobertura
```

| Arquivo | Cobre |
|---|---|
| `tests/test_transform.py` | validação e limpeza de registros |
| `tests/test_client.py` | requisições, 404 sem dados, erros HTTP/JSON (via `responses`) |
| `tests/test_analysis.py` | agregações e voltas mais rápidas |
| `tests/test_catalog.py` | rótulos e ordenação |
| `tests/test_cli.py` | linha de comando |
| `tests/test_app.py` | dashboard, via `streamlit.testing.v1.AppTest` |

`app.py` aparece com 0% na cobertura porque o `AppTest` executa o script fora do processo medido; os módulos de domínio ficam próximos de 100%.

!!! warning "Estado atual"
    Na última execução, `tests/test_app.py::test_app_empty` e `test_app_no_drivers` falharam (`assert 0 == 1`). Os demais testes passaram e a cobertura total (~60%) atingiu o mínimo de 50%.

## Documentação

```bash
poetry run mkdocs serve
poetry run mkdocs build --strict
```

## Validação final

```bash
poetry check
poetry run ruff check .
poetry run ruff format --check .
poetry run pytest --cov=f1 --cov-report=term-missing --cov-fail-under=50
poetry run mkdocs build --strict
```
