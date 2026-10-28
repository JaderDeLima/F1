# plan.md — Criação do projeto F1 (telemetria OpenF1)

## Context

Projeto de dados em Python que consome a API pública OpenF1 (`/v1/car_data`, ver `doc.md`) para obter telemetria de pilotos (speed, rpm, n_gear, throttle, brake, drs) e transformá-la em dados limpos e analisáveis. O desenvolvimento segue obrigatoriamente `SKILL.md` (Pyenv, Poetry, Ruff, Pytest com cobertura ≥ 50% de `src/f1/`, MkDocs Material).

### Estado verificado do repositório
- Existem: `pyproject.toml` (PEP 621, sem dependências), `src/f1/__init__.py`, `tests/__init__.py`, `.python-version` (= `3.12.10`), `SKILL.md`, `doc.md`. Branch `main`, um commit.
- **Não existem**: `poetry.lock`, `mkdocs.yml`, `docs/`, `README.md`, `.gitignore`; sem dependências, Ruff, Pytest ou MkDocs configurados.
- **Divergência a resolver**: `SKILL.md` diz `requires-python = ">=3.14"`, mas o `pyproject.toml` real tem `">=3.12"` e `.python-version` é `3.12.10`. Decisão: **manter 3.12** (não alterar arbitrariamente, conforme SKILL §1) e ajustar `target-version` do Ruff para `py312` (não `py314`). Atualizar a nota no `SKILL.md` na fase 0.
- `readme = "README.md"` aponta para arquivo inexistente → criar README antes de `poetry install`.

## Fases

### Fase 0 — Ambiente (SKILL §1–2)
1. `pyenv versions` / `python --version` — confirmar 3.12.10 ativo.
2. `poetry --version` (exigir 2.x).
3. Criar `README.md` mínimo e `.gitignore` (`.venv/`, `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`, `.coverage`, `htmlcov/`, `site/`).
4. `poetry config virtualenvs.in-project true`; `poetry env use <pyenv which python>`; `poetry install`; `poetry check`.
5. Verificar: `poetry env info --path` → `<projeto>/.venv`; `poetry run python --version` = 3.12.10.

### Fase 1 — Dependências (SKILL §2.4)
- Produção: `poetry add requests` (cliente HTTP; avaliar `httpx` só se houver necessidade de async). `pandas` apenas se a análise tabular for realmente usada — adicionar na fase 4, não antes.
- Dev: `poetry add --group dev ruff pytest pytest-cov mkdocs mkdocs-material` (+ `responses` ou `pytest-mock` para simular HTTP).
- Confirmar `poetry.lock` gerado e versionado.

### Fase 2 — Configuração de ferramentas no `pyproject.toml`
- `[tool.ruff]` line-length 88, `target-version = "py312"`, `src = ["src","tests"]`; `[tool.ruff.lint] select = ["E","F","W","I","B","UP","N","SIM"]`.
- `[tool.pytest.ini_options]`: `testpaths=["tests"]`, `pythonpath=["src"]`, `addopts="--cov=f1 --cov-report=term-missing --cov-fail-under=50"`; `[tool.coverage.run] source=["src/f1"], branch=true`.
- `mkdocs.yml`: `site_name: F1`, `theme.name: material`, `nav` só com páginas existentes.

### Fase 3 — Arquitetura do pacote `src/f1/`
Módulos pequenos e testáveis (sem rede nos testes):

| Módulo | Responsabilidade |
|---|---|
| `config.py` | `BASE_URL = "https://api.openf1.org/v1"`, timeout, constantes |
| `client.py` | `get_car_data(session_key, driver_number, **filtros)` — monta query (operadores `>=`, `<=`, `>`, `<` como chaves tipo `"speed>="`, conforme `doc.md` §5), trata HTTP/timeout/JSON inválido, levanta exceções próprias |
| `models.py` | `dataclass CarData` com campos `date, session_key, meeting_key, driver_number, n_gear, speed, rpm, throttle, brake, drs` |
| `transform.py` | Validação/limpeza: parse de `date` ISO 8601 UTC, tratamento de campos faltantes/`None`, limites (throttle 0–100, brake ∈ {0,100}), conversão para `CarData` |
| `analysis.py` | Agregações simples (velocidade máxima, tempo em ≥ N km/h, uso de DRS) |
| `cli.py` (opcional) | Ponto de entrada de linha de comando para a consulta do exemplo (`driver 55`, `session 9159`, `speed>=315`) |

Nota de domínio (de `doc.md`): sem filtro de `speed` o endpoint retorna milhares de leituras por sessão → o cliente deve exigir/encorajar filtros e documentar o volume.

### Fase 4 — Testes (SKILL §4) — meta ≥ 50% de `src/f1/`, ideal >80% nas regras de negócio
- `tests/test_transform.py`: caminho normal, campos ausentes/`None`, throttle/brake fora do limite, data inválida (`parametrize`).
- `tests/test_client.py`: HTTP mockado — resposta com os 2 registros do `doc.md` (fixture local pequena), lista vazia, HTTP 4xx/5xx, timeout, JSON inválido, montagem correta da query com operadores.
- `tests/test_models.py` / `test_analysis.py`: agregações com dados controlados.
- Proibido: rede real, reduzir limite de cobertura, testes sem asserções.

### Fase 5 — Documentação (SKILL §5)
`docs/` + `mkdocs.yml` com: `index.md` (objetivo), `arquitetura.md`, `instalacao.md`, `uso.md` (exemplos de comando), `api-openf1.md` (conteúdo migrado de `doc.md` **somente após aprovação; `doc.md` original não é apagado**), `desenvolvimento.md` (regras do Ruff, cobertura). Marcar como "planejado" o que não estiver implementado.

### Fase 6 — Validação final (SKILL §7) e commit
```bash
poetry check
poetry run ruff check .
poetry run ruff format --check .
poetry run pytest --cov=f1 --cov-report=term-missing --cov-fail-under=50
poetry run mkdocs build --strict
```
Todos devem sair com código 0; relatar arquivos alterados, comandos e resultados reais. Commitar por fase, em mudanças pequenas, somente quando o usuário pedir.

## Arquivos a criar/alterar
- Criar: `README.md`, `.gitignore`, `mkdocs.yml`, `docs/*.md`, `src/f1/{config,client,models,transform,analysis}.py`, `tests/test_*.py`, `poetry.lock` (gerado).
- Alterar: `pyproject.toml` (deps + Ruff/Pytest/coverage), `SKILL.md` (corrigir nota `>=3.14` → `>=3.12` e `py314` → `py312`).
- Não tocar: `doc.md`, `.python-version`.

## Critérios de aceitação (SKILL §10)
Python 3.12.10 fixado e coerente com `requires-python`; Poetry gerencia ambiente (`.venv`) e `poetry.lock` versionado; `import f1` funciona via `poetry run`; Ruff check/format limpos; Pytest passa com `Required test coverage of 50% reached`; `mkdocs build --strict` ok; procedimentos reproduzíveis do zero a partir do README/docs.

## Verificação ponta a ponta
1. `poetry install` em ambiente limpo → sucesso.
2. Rodar a sequência de validação final acima.
3. Teste manual opcional (rede real, fora da suíte): `poetry run python -m f1.cli --driver 55 --session 9159 --min-speed 315` deve retornar 2 registros com `speed=315`, `n_gear=8` (conforme `doc.md`).

## Decisões em aberto
- Usar `pandas` ou manter dataclasses puras? (padrão proposto: dataclasses; pandas só se a análise exigir).
- Migrar `doc.md` para `docs/` (padrão proposto: copiar, manter original).
