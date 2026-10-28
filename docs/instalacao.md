# Instalação

Requisitos: Pyenv, Python 3.12 e Poetry 2.x.

```bash
pyenv local 3.12.10
poetry config virtualenvs.in-project true
poetry env use $(pyenv which python)   # PowerShell: poetry env use (pyenv which python)
poetry install
poetry check
poetry run python --version
```

O ambiente virtual fica em `.venv/`. Execute tudo com `poetry run`; não use `pip install` nem outro gerenciador de ambientes.

A versão do Python está fixada em `.python-version` (`3.12.10`) e deve coincidir com `requires-python` do `pyproject.toml`.

## Dependências

| Grupo | Pacotes |
|---|---|
| Produção | `requests`, `streamlit` |
| Desenvolvimento | `ruff`, `pytest`, `pytest-cov`, `mkdocs`, `mkdocs-material`, `responses`, `taskipy` |

Para instalar sem as dependências de desenvolvimento: `poetry install --without dev`.

## Verificação

```bash
poetry run python -c "import f1"
poetry run task test
```
