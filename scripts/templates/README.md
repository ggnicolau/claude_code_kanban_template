# {repo_name}

> Descrição curta do projeto — o que faz e para quem.

---

## Visão Geral

_(Preencher após o `/kickoff`: objetivo, problema que resolve, principais funcionalidades.)_

---

## Como Rodar

### Pré-requisitos

- Python 3.11+
- [`uv`](https://github.com/astral-sh/uv) instalado

### Instalação

```bash
git clone https://github.com/<org>/{repo_name}.git
cd {repo_name}
uv sync
```

### Variáveis de Ambiente

Copie o exemplo e preencha os valores:

```bash
cp .env.example .env
```

### Executar

```bash
uv run python -m src.main
```

---

## Desenvolvimento

```bash
# Testes
uv run pytest

# Linting e formatação
uv run ruff check .
uv run black .
```

Pull requests passam por CI automático (ruff + black + pytest).

---

## Estrutura

```text
src/          # código principal
tests/        # testes
notebooks/    # exploração e análise
.claude/
  agents/     # 13 agentes especializados
  commands/   # /kickoff, /advance, /review-backlog, /review, /deploy, /fix-issue, /clean
```

---

## Commands

| Command | O que faz |
|---|---|
| `/kickoff` | Inicia o projeto — discovery com você, pesquisa, relatório, apresentação, backlog completo |
| `/advance` | Avança no Kanban — fecha prontos, valida com PO, paraleliza issues independentes, delega |
| `/review-backlog` | Varredura proativa — fecha prontos, identifica lacunas, refina e cria novas issues |
| `/review` | Code review de um PR pelo tech-lead |
| `/deploy` | Deploy via infra-devops |
| `/fix-issue` | Corrige um bug ou problema reportado |
| `/clean` | Commita e faz push de tudo pendente localmente |

---

## Equipe de Agentes

O ponto de entrada é o `project-manager`. Rode `/kickoff` para iniciar o projeto ou continue pelo Kanban do GitHub Projects.

| Agente | Responsabilidade |
|---|---|
| `project-manager` | Ponto de entrada — delega, consolida |
| `tech-lead` | Orquestração técnica, code review |
| `product-owner` | Kanban, backlog, roadmap |
| `data-engineer` | Pipelines, ETL |
| `data-scientist` | Análise exploratória, modelagem estatística, insights |
| `ml-engineer` | Produtização de modelos validados pelo data-scientist |
| `ai-engineer` | LLMs, agentes, RAG |
| `infra-devops` | Cloud, CI/CD |
| `qa` | Testes e qualidade |
| `researcher` | Pesquisa técnica e de produto |
| `security-auditor` | Segurança |
| `frontend-engineer` | Web, UI, UX |
| `marketing-strategist` | Marketing, go-to-market, canais, publicidade |

---

## Mapa de Interações entre Agentes

| Agente | Responde a | Trabalha com |
|---|---|---|
| **project-manager** | Usuário | product-owner, tech-lead, researcher, marketing-strategist |
| **product-owner** | project-manager | researcher, marketing-strategist, kanban |
| **tech-lead** | project-manager | data-engineer, data-scientist, ml-engineer, ai-engineer, infra-devops, qa, security-auditor, frontend-engineer, researcher |
| **researcher** | PM / PO / TL (quem acionar) | todos os agentes que precisam de inteligência de mercado ou técnica |
| **marketing-strategist** | PM / PO (quem acionar) | researcher, data-scientist |
| **data-engineer** | tech-lead | data-scientist, researcher, qa |
| **data-scientist** | tech-lead | data-engineer, researcher, marketing-strategist |
| **ml-engineer** | tech-lead | data-scientist, data-engineer, researcher |
| **ai-engineer** | tech-lead | researcher, ml-engineer |
| **infra-devops** | tech-lead | security-auditor |
| **frontend-engineer** | tech-lead | infra-devops, researcher |
| **qa** | tech-lead | data-engineer, data-scientist |
| **security-auditor** | tech-lead / infra-devops | infra-devops |

---

## Ferramentas Disponíveis

| Ferramenta | Cobertura |
|---|---|
| `Bash(git:*)` | Todos os comandos git (exceto force push e reset hard) |
| `Bash(gh:*)` | gh CLI — issues, PRs, projects, workflows (exceto operações destrutivas) |
| `Bash(python/pytest/ruff/black/pip/uv:*)` | Desenvolvimento Python completo |
| `WebSearch` / `WebFetch` | Pesquisa web e leitura de URLs |
| MCP GitHub | Leitura e escrita de issues, PRs, branches, reviews |

Operações permanentemente bloqueadas: `git push --force`, `git reset --hard`, `git clean -f`, `gh repo delete`, `gh secret set/delete`, `gh auth login/token`.

---

## Status

Acompanhe o progresso no [GitHub Projects](https://github.com/<org>/{repo_name}/projects).
