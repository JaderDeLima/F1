---
name: python-data-project-standards
description: Regras obrigatórias de desenvolvimento do projeto de dados em Python (Pyenv, Poetry, Ruff, Pytest com cobertura mínima de 50%, MkDocs Material). Usar ao criar, alterar, testar, validar ou documentar qualquer parte do projeto.
---

# SKILL.md — Padrões de desenvolvimento do projeto de dados (Python)

Referência permanente para humanos e agentes de IA. Aplica-se a criação, manutenção, execução, validação e documentação do projeto.

## 0. Convenções deste documento

- **OBRIGATÓRIO**: regra que deve ser cumprida. Descumprimento bloqueia a conclusão da tarefa.
- **RECOMENDADO**: boa prática; pode ser omitida com justificativa registrada.
- **`<pacote>`**: nome do pacote Python em `src/`. Neste repositório, **`<pacote>` = `f1`** (ver `[tool.poetry] packages` no `pyproject.toml`). Onde as especificações genéricas citam `src/projeto/`, leia **`src/f1/`**. Se o pacote for renomeado, atualize todos os comandos deste arquivo.
- Todos os comandos usam sintaxe de shell neutra e funcionam em PowerShell e Bash, salvo indicação contrária.

### Estado atual verificado do repositório (não presumir além disto)

| Item | Estado |
|---|---|
| `pyproject.toml` | Existe; formato PEP 621 (`[project]`), `requires-python = ">=3.12"`, `poetry-core>=2.0.0,<3.0.0` |
| Pacote | `src/f1/__init__.py` |
| Testes | `tests/__init__.py` (ainda sem testes) |
| `.python-version`, `poetry.lock`, `mkdocs.yml`, `docs/`, `README.md`, `.gitignore` | **Não existem**; criar conforme as seções abaixo quando necessário |
| Dependências, Ruff, Pytest, MkDocs | **Ainda não configurados** |

> `pyproject.toml` declara `readme = "README.md"`, e o arquivo não existe. Crie o `README.md` antes de `poetry install`, ou o build do pacote falhará.

---

## 1. Python com Pyenv — OBRIGATÓRIO

1. Ler a versão exigida em `pyproject.toml` (`requires-python`). Não alterá-la arbitrariamente.
2. Se a versão não estiver instalada, instalá-la com o Pyenv.
3. Fixar a versão no diretório do projeto (gera `.python-version`, que deve ser versionado).
4. Verificar a versão efetiva, tanto no shell quanto no Poetry.

```bash
pyenv --version
pyenv versions
pyenv install --list | grep "3.14"     # PowerShell: pyenv install --list | Select-String "3.14"
pyenv install 3.14.<patch>             # use a última 3.14.x listada
pyenv local 3.14.<patch>               # cria/atualiza .python-version
python --version
poetry run python --version            # deve coincidir com a versão acima
```

Notas:
- No Windows, o Pyenv equivalente é o `pyenv-win`; a sintaxe dos comandos acima é a mesma.
- Trocar de versão do Python exige avaliar a compatibilidade de todas as dependências e atualizar `requires-python` e `.python-version` em conjunto.
- Se `python --version` e `poetry run python --version` divergirem, corrigir com `poetry env use <caminho-ou-versão>` (seção 2) antes de prosseguir.

---

## 2. Poetry e ambiente virtual — OBRIGATÓRIO

### 2.1 Regras

- O Poetry é a única ferramenta de gerenciamento de dependências e do ambiente virtual.
- Dependências e configurações vivem no `pyproject.toml`; o `poetry.lock` é versionado e garante reprodutibilidade.
- Dependências de produção ficam em `[project].dependencies`; as de desenvolvimento ficam no grupo `dev`.
- **Proibido**: `pip install` de dependências do projeto, instalação no Python global, ambientes redundantes (`python -m venv`, `virtualenv`, `conda`) para este projeto.
- A instalação do próprio Poetry pode ser feita fora do ambiente do projeto (ex.: `pipx install poetry`); as dependências do projeto, nunca.
- Executar tudo com `poetry run <comando>` (ou dentro de `poetry shell`/ambiente ativado pelo Poetry).
- Antes de adicionar uma biblioteca: avaliar se é necessária, verificar compatibilidade com a versão do Python do projeto e com as demais dependências. O `poetry add` falha se não houver resolução compatível; não contornar com `--lock` forçado ou remoção de restrições sem justificativa.

### 2.2 Verificar a versão do Poetry (sempre, antes de usar a sintaxe)

```bash
poetry --version
```

O `pyproject.toml` do projeto exige `poetry-core>=2.0.0`, portanto use **Poetry 2.x**. Sintaxe de referência (Poetry 2.x):

- Dependências de produção: `poetry add <pacote>` (grava em `[project].dependencies`).
- Dependências de desenvolvimento: `poetry add --group dev <pacote>` (grava em `[dependency-groups]` ou `[tool.poetry.group.dev.dependencies]`).
- Atualizar o lock: `poetry lock` (no Poetry 2.x o lock é atualizado sem `--no-update`; para atualizar tudo use `poetry update`).
- Se `poetry --version` for 1.x, a sintaxe pode divergir (ex.: `poetry lock --no-update`, `poetry shell` nativo, `poetry export` nativo). Consultar `poetry <comando> --help` antes de executar.
- `poetry shell` e `poetry export` exigem plugins no Poetry 2.x; preferir `poetry run`.

### 2.3 Configuração e instalação do ambiente

```bash
poetry config virtualenvs.in-project true     # cria .venv dentro do projeto
poetry env use $(pyenv which python)          # Bash. PowerShell: poetry env use (pyenv which python)
poetry env info --path                         # caminho do ambiente virtual
poetry env info                                # versão do Python, caminho e validade
poetry install                                 # instala produção + grupos padrão (inclui dev)
poetry check                                   # valida o pyproject.toml
```

- Verificação: `poetry env info --path` deve apontar para `<projeto>/.venv` e `poetry run python --version` deve coincidir com `.python-version`.
- `.venv/` deve estar no `.gitignore`.
- Em CI ou produção, instalar sem dev: `poetry install --without dev`.

### 2.4 Adicionar dependências

```bash
poetry add pandas                       # produção (exemplo; só se for necessária)
poetry add --group dev ruff pytest pytest-cov mkdocs mkdocs-material
poetry show --tree                      # inspecionar a árvore de dependências
poetry show --outdated                  # RECOMENDADO: verificar versões desatualizadas
```

Após qualquer alteração de dependência: confirmar que `poetry.lock` foi atualizado e que `poetry install` seguido dos testes continua passando.

---

## 3. Qualidade de código com Ruff — OBRIGATÓRIO

- Ruff é a ferramenta oficial de lint **e** formatação. Não adicionar Black, isort, Flake8 ou Pylint sem justificativa técnica registrada.
- Instalado como dependência de desenvolvimento (`poetry add --group dev ruff`).
- Configuração em `pyproject.toml`, compatível com a versão instalada (`poetry run ruff --version`).
- Não desabilitar regras apenas para ocultar problemas. Qualquer `# noqa` ou `ignore` exige justificativa em comentário e deve ser o mais específico possível.

Configuração mínima de referência (ajustar à versão instalada):

```toml
[tool.ruff]
line-length = 88
target-version = "py312"
src = ["src", "tests"]

[tool.ruff.lint]
select = ["E", "F", "W", "I", "B", "UP", "N", "SIM"]
```

Documentar na página `docs/desenvolvimento.md` (ou equivalente) as regras escolhidas.

Comandos:

```bash
poetry run ruff check .              # lint
poetry run ruff check . --fix        # corrige o que for corrigível automaticamente
poetry run ruff format .             # formata
poetry run ruff format --check .     # verifica formatação sem modificar
```

**Critério de aprovação**: `ruff check .` e `ruff format --check .` terminam com código de saída 0.

---

## 4. Testes com Pytest e cobertura — OBRIGATÓRIO

### 4.1 Regras

- Pytest e pytest-cov instalados como dependências de desenvolvimento (`poetry add --group dev pytest pytest-cov`).
- Testes em `tests/`, arquivos `test_*.py`, funções `test_<comportamento_esperado>`.
- Testes unitários independentes, determinísticos e reproduzíveis. Sem rede (por exemplo, a API OpenF1 deve ser simulada com dados controlados/mocks), sem banco de dados e sem arquivos externos, salvo fixtures locais pequenas.
- Cobrir: caminho normal, valores ausentes (`None`/NaN/campos faltantes), entradas inválidas, limites e exceções relevantes de funções de transformação, limpeza, validação e processamento.
- Usar `pytest.fixture` e `pytest.mark.parametrize` quando melhorarem clareza e manutenção.
- Não alterar o comportamento da aplicação apenas para fazer testes passarem.
- Executar os testes após cada alteração relevante.

### 4.2 Configuração (`pyproject.toml`)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = "--cov=f1 --cov-report=term-missing --cov-fail-under=50"

[tool.coverage.run]
source = ["src/f1"]
branch = true
```

- `--cov=f1` mede o pacote instalado/importável `f1`, localizado em `src/f1/`.
- Se o pacote for renomeado, trocar `f1` em `--cov` e `source`.
- `addopts` faz com que **toda** execução de `pytest` meça cobertura e falhe abaixo de 50%. Para rodar um teste isolado durante depuração, usar `poetry run pytest -o addopts="" tests/test_x.py`; a validação final deve sempre usar o comando completo.

### 4.3 Cobertura mínima: 50% de `src/f1/` — OBRIGATÓRIO

- A meta se aplica ao código-fonte em `src/f1/`, com a execução falhando quando a cobertura total for inferior a 50%.
- **Proibido**: reduzir o limite, excluir módulos relevantes da medição (`omit`, `exclude`) para atingir a meta, ou criar testes sem asserções significativas apenas para elevar o percentual.
- Priorizar cobertura das regras de negócio e transformações de dados.
- Após a execução, apresentar o relatório e listar os módulos/linhas não cobertos que sejam relevantes.

Comandos:

```bash
poetry run pytest                                              # usa addopts (cobertura + limite de 50%)
poetry run pytest --cov=f1 --cov-report=term-missing --cov-fail-under=50   # comando explícito equivalente
poetry run pytest -v                                           # saída detalhada
poetry run pytest --cov=f1 --cov-report=html                   # RECOMENDADO: relatório em htmlcov/
```

Observação: com pacote vazio (apenas `__init__.py`), o `pytest` sai com erro 5 ("no tests collected") e o relatório de cobertura não é significativo. Só considerar esta etapa concluída quando houver testes reais executados e relatório mostrando `Required test coverage of 50% reached`.

**Verificação de descoberta do pacote**: se o relatório mostrar "No data was collected" ou "Module f1 was never imported", conferir `pythonpath`, `packages = [{include = "f1", from = "src"}]` e se `poetry install` foi executado. Ajustar apenas a configuração de descoberta, sem reorganizar a arquitetura.

---

## 5. Documentação com MkDocs Material — OBRIGATÓRIO

### 5.1 Regras

- Instalar `mkdocs` e `mkdocs-material` como dependências de desenvolvimento.
- Documentação em `docs/`, configuração em `mkdocs.yml`, página inicial em `docs/index.md`.
- Conteúdo mínimo: objetivo, arquitetura, estrutura de diretórios, instalação, configuração do ambiente, execução, testes e principais funcionalidades/módulos/transformações de dados, com exemplos de comandos.
- A documentação deve refletir a implementação **real**. Não descrever como existente o que não está implementado; marcar o que é planejado explicitamente como "planejado".
- Todo arquivo citado em `nav` deve existir. O build em modo estrito detecta links e referências quebrados.
- Existe `doc.md` na raiz (notas sobre o endpoint `car_data` da OpenF1). Ele não faz parte do MkDocs; se o conteúdo for relevante, migrá-lo para `docs/` somente com decisão explícita e sem apagar o original sem aprovação.

### 5.2 Configuração mínima de referência (`mkdocs.yml`)

```yaml
site_name: F1
docs_dir: docs
theme:
  name: material
nav:
  - Início: index.md
```

Ampliar `nav` somente com páginas que existam.

### 5.3 Comandos

```bash
poetry run mkdocs serve               # servidor local (http://127.0.0.1:8000)
poetry run mkdocs build --strict      # constrói em modo estrito; qualquer aviso vira erro
```

**Critério de aprovação**: `mkdocs build --strict` termina com código 0. O diretório `site/` gerado deve estar no `.gitignore`.

---

## 6. Estrutura do projeto

Estrutura de referência (não autoriza reorganizar automaticamente um projeto existente):

```
.
├── .python-version
├── .gitignore
├── pyproject.toml
├── poetry.lock
├── mkdocs.yml
├── README.md
├── SKILL.md
├── src/
│   └── f1/
│       ├── __init__.py
│       └── ...módulos
├── tests/
│   └── test_*.py
└── docs/
    ├── index.md
    └── ...páginas
```

- Antes de criar, mover ou renomear arquivos: inspecionar a estrutura atual e avaliar impactos (imports, `pyproject.toml`, testes, documentação).
- Código-fonte somente em `src/f1/`; testes em `tests/`; documentação em `docs/`.
- `.gitignore` mínimo recomendado: `.venv/`, `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`, `.coverage`, `htmlcov/`, `site/`.

---

## 7. Fluxo obrigatório de desenvolvimento

Para toda funcionalidade ou alteração de código:

1. Inspecionar a estrutura do projeto e as instruções existentes (`pyproject.toml`, este arquivo, `docs/`).
2. Verificar Python (`python --version`, `poetry run python --version`), ambiente (`poetry env info --path`) e dependências (`poetry check`, `poetry install`).
3. Analisar os módulos relacionados à alteração.
4. Implementar seguindo as convenções existentes, com mudanças pequenas e fáceis de revisar.
5. Criar ou atualizar os testes unitários correspondentes.
6. Executar o Ruff e corrigir lint e formatação.
7. Executar o Pytest e confirmar cobertura ≥ 50% de `src/f1/`.
8. Atualizar a documentação quando necessário.
9. Validar a documentação com `mkdocs build --strict`.
10. Relatar: arquivos alterados, comandos executados e resultados.

Se uma etapa falhar: apresentar o erro e a causa provável (quando identificável), e **não** declarar a validação como concluída.

### Sequência única de validação final

```bash
poetry check
poetry run ruff check .
poetry run ruff format --check .
poetry run pytest --cov=f1 --cov-report=term-missing --cov-fail-under=50
poetry run mkdocs build --strict
```

---

## 8. Resumo de comandos essenciais

**Ambiente e dependências**

```bash
pyenv local 3.14.<patch>
poetry config virtualenvs.in-project true
poetry env use $(pyenv which python)     # PowerShell: poetry env use (pyenv which python)
poetry install
poetry env info --path
poetry add <pacote>
poetry add --group dev <pacote>
```

**Qualidade**

```bash
poetry run ruff check .
poetry run ruff check . --fix
poetry run ruff format --check .
poetry run ruff format .
```

**Testes**

```bash
poetry run pytest
poetry run pytest --cov=f1 --cov-report=term-missing --cov-fail-under=50
```

**Documentação**

```bash
poetry run mkdocs serve
poetry run mkdocs build
poetry run mkdocs build --strict
```

---

## 9. Regras de comportamento para a IA — OBRIGATÓRIO

- Ler os arquivos de configuração antes de sugerir ou fazer mudanças.
- Preferir alterações pequenas, justificadas e fáceis de revisar; não substituir configurações existentes sem necessidade.
- Não instalar dependências sem avaliar necessidade e compatibilidade.
- Não executar tarefas do projeto fora do ambiente gerenciado pelo Poetry.
- Não reduzir a cobertura mínima nem ignorar falhas de lint, testes ou documentação.
- Não afirmar que um comando foi executado se não foi. Informar explicitamente quando uma validação não puder ser executada e por quê.
- Apresentar os comandos que permitem reproduzir cada verificação.
- Preservar a compatibilidade entre Pyenv, Python, Poetry e demais ferramentas.
- Não inventar arquivos, configurações ou funcionalidades inexistentes; verificar antes de citar.

---

## 10. Critérios de aceitação (verificáveis)

| # | Critério | Como verificar |
|---|---|---|
| 1 | Versão local do Python definida e compatível | `.python-version` existe; `python --version` satisfaz `requires-python` |
| 2 | Poetry gerencia dependências e ambiente | `poetry check` sem erros; `poetry.lock` presente e versionado |
| 3 | Dependências instaladas no ambiente virtual | `poetry env info --path` aponta para `.venv`; `poetry run python -c "import f1"` funciona |
| 4 | Ruff configurado para lint e formatação | `[tool.ruff]` no `pyproject.toml`; `ruff check .` e `ruff format --check .` com saída 0 |
| 5 | Pytest executa os testes unitários | `poetry run pytest` coleta e passa os testes em `tests/` |
| 6 | pytest-cov mede `src/f1/` | Relatório `term-missing` lista os módulos de `f1` |
| 7 | Falha quando a cobertura < 50% | `--cov-fail-under=50` presente (em `addopts` ou no comando); execução com cobertura menor retorna código ≠ 0 |
| 8 | MkDocs Material configurado | `mkdocs.yml` com `theme.name: material` e `docs/index.md` |
| 9 | Documentação inicia e constrói em modo estrito | `mkdocs serve` sobe; `mkdocs build --strict` com saída 0 |
| 10 | Procedimentos reproduzíveis | Seções 1–8 permitem a um novo desenvolvedor configurar, testar e documentar do zero |
