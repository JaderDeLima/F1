# F1

Projeto em Python que consome a API pública [OpenF1](https://openf1.org) para obter telemetria e voltas de pilotos de Fórmula 1, transformá-la em dados limpos e exibi-la em um dashboard.

## O que o projeto faz

- **Cliente HTTP** para cinco endpoints da OpenF1: `car_data`, `laps`, `meetings`, `sessions` e `drivers` (`f1.client`).
- **Validação e limpeza** da telemetria bruta, descartando registros inválidos (`f1.transform`).
- **Análises**: velocidade máxima, leituras acima de um limite, fração de DRS aberto e as voltas mais rápidas (`f1.analysis`).
- **Rótulos legíveis** para provas, sessões e pilotos (`f1.catalog`).
- **Linha de comando** para consultar a telemetria de um piloto (`f1.cli`).
- **Dashboard Streamlit** com seleção em cascata (temporada → prova → sessão → piloto), ranking das 5 voltas mais rápidas por circuito e gráficos de telemetria (`f1.app`).

## Stack

| Item | Escolha |
|---|---|
| Linguagem | Python 3.12 (`requires-python = ">=3.12,<4.0"`) |
| Gerenciamento | Pyenv + Poetry 2.x (`.venv/` no projeto) |
| Dependências de produção | `requests`, `streamlit` (traz `pandas` como dependência transitiva) |
| Qualidade | Ruff (lint e formatação) |
| Testes | Pytest, pytest-cov, `responses` e `streamlit.testing` (`AppTest`) |
| Documentação | MkDocs Material |
| Atalhos | taskipy (`poetry run task ...`) |

## Navegação

1. [Arquitetura](arquitetura.md): módulos e fluxo de dados
2. [Instalação](instalacao.md)
3. [Uso](uso.md): CLI, biblioteca e atalhos
4. [Dashboard](dashboard.md): funcionamento do painel Streamlit
5. [Módulos](modulos.md): referência das funções
6. [API OpenF1](api-openf1.md): endpoints e campos usados
7. [Desenvolvimento](desenvolvimento.md): Ruff, testes e cobertura
