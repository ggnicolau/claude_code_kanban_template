# Claude Code Kanban Template

Template base para criar novos projetos Python com Claude Code configurado, equipe multi-agentes e kanban no GitHub Projects.

**Este repositório é uma fábrica de projetos** — você usa o `/wizard` aqui para criar um novo repositório filho já configurado. O desenvolvimento acontece no filho, não aqui.

---

## O que o filho recebe ao ser criado

| Entregável | Detalhe |
|---|---|
| **12 agentes especializados** | `project-manager`, `tech-lead`, `product-owner`, `data-engineer`, `ml-engineer`, `ai-engineer`, `infra-devops`, `qa`, `researcher`, `security-auditor`, `frontend-engineer`, `marketing-strategist` — com organograma, cadeia de comando e protocolo de escalation |
| **Kanban pré-populado** | Épicos template em 6 dimensões: Discovery, Negócio, Produto, Tech, Lançamento, Operações |
| **`/kickoff`** | Inicia o projeto com **Fase 0 narrativa** (contexto do fundador, gênese, ancoragens, exclusões) → persiste memória → discovery → pesquisa (`researcher`) → relatório + apresentação (PM) → backlog completo (PO) → aprovação → delegação |
| **`/advance`** | Avança no Kanban: fecha prontos (PO), valida issues com PO, paraleliza issues independentes, delega via TL |
| **`/review-backlog`** | Varredura proativa: fecha prontos, identifica lacunas, refina e cria novas issues (PO + TL) |
| **`/review`, `/deploy`, `/fix-issue`** | Code review, deploy e correção de bugs |
| **`/clean`** | Limpeza de branches, arquivos temporários e estados inconsistentes |
| **`/update-memory`** | Registrar decisões de produto, restrições e entregáveis aprovados na memória persistente |
| **CI/CD** | GitHub Actions com ruff, black e pytest em todo PR |
| **`CLAUDE.md` e `AGENTS.md`** | Gerados com o nome do projeto, com regras de persona, kanban e delegação |
| **Permissões granulares** | Agentes operam sem prompts desnecessários; operações destrutivas bloqueadas |
| **Memória persistente** | `.claude/memory/user_profile.md`, `project_genesis.md`, `project_history.md` e `MEMORY.md` criados na Fase 0 do `/kickoff` — somente project-manager e tech-lead leem antes de agir |
| **Hook de sessão** | `session_start.sh` exibe automaticamente o Kanban ao iniciar cada sessão — últimas entregas, cards ativos, inconsistências board/issue |
| **Gerador PDF/DOCX/PPTX** | `scripts/generate_docs.js` — MDs em `docs/` ganham contraparte em `docs/<sub>/generated/` via hook `post_write.sh` |
| **Versionamento de documentos** | Convenção `{nome}_YYYY-MM-DD_v{N}.md` com pasta `archive/` — agentes nunca sobrescrevem versão anterior |
| **Convenção de commits** | Escopo `(system)` para infra agentic vs. sem escopo para trabalho de produto |
| **Skills de domínio** | 11 skills enterprise em `.agents/skills/` (product-management, code-review, data-engineering, ml-engineering, ai-engineering, frontend-engineering, security-audit, qa-testing, market-research, go-to-market, infra-devops) |

---

## Arquitetura Multi-Agentes

```mermaid
graph TD
    U(["👤 Usuário"]) --> PM["🗂️ Project Manager\nponto de entrada"]

    PM --> PO["📋 Product Owner\nkanban + roadmap"]
    PM --> TL["🧠 Tech Lead\norquestrador técnico + docs"]
    PM --> RES["🔍 Researcher\npesquisa técnica e de produto"]
    PM --> MKT["📣 Marketing Strategist\ngo-to-market + mídia"]

    PO --> RES
    PO --> MKT
    PO --> KB[("GitHub Kanban")]

    TL --> DE["🔧 Data Engineer\npipelines + ETL"]
    TL --> MLE["📊 ML Engineer\nmodelos + experimentos"]
    TL --> AIE["🤖 AI Engineer\nLLMs + agentes + RAG"]
    TL --> IDF["☁️ Infra & DevOps\ncloud + CI/CD"]
    TL --> QA["✅ QA\ntestes + qualidade"]
    TL --> RES
    TL --> SEC["🔒 Security Auditor\nsegurança + vulnerabilidades"]
    TL --> FE["🖥️ Frontend Engineer\nweb + UI + UX"]

    FE --> IDF
    FE --> RES
    MLE --> DE
    MLE --> RES
    AIE --> RES
    AIE --> MLE
    QA --> DE
    QA --> MLE
    IDF --> SEC
```

---

## Mapa de Interações entre Agentes

Cada agente sabe a quem responde e com quem colabora. O fluxo típico percorre coordenação → produto/técnica → execução → qualidade.

| Agente | Responde a | Trabalha com |
|---|---|---|
| **project-manager** | Usuário | product-owner, tech-lead, researcher, marketing-strategist |
| **product-owner** | project-manager | researcher, marketing-strategist, kanban |
| **tech-lead** | project-manager | data-engineer, ml-engineer, ai-engineer, infra-devops, qa, security-auditor, frontend-engineer, researcher |
| **researcher** | PM / PO / TL (quem acionar) | todos os agentes que precisam de inteligência de mercado ou técnica |
| **marketing-strategist** | PM / PO (quem acionar) | researcher |
| **data-engineer** | tech-lead | researcher, qa |
| **ml-engineer** | tech-lead | data-engineer, researcher |
| **ai-engineer** | tech-lead | researcher, ml-engineer |
| **infra-devops** | tech-lead | security-auditor |
| **frontend-engineer** | tech-lead | infra-devops, researcher |
| **qa** | tech-lead | data-engineer, ml-engineer |
| **security-auditor** | tech-lead / infra-devops | infra-devops |

---

## Como criar um novo projeto

### Via wizard (recomendado)

Em uma conversa nova **neste repositório**, use:

```
/wizard
```

O wizard vai:
1. Perguntar nome, visibilidade e se instalar skills Caveman
2. Verificar se a pasta local já existe
3. Criar o repositório no GitHub a partir deste template
4. Clonar localmente
5. Configurar o secret `GH_PAT` (PAT com escopo: `repo`, `project`, `read:org`)
6. Disparar a workflow `Setup Kanban` — cria o board e os épicos template
7. Remover arquivos exclusivos do template (wizard, scripts de criação, etc.)
8. Gerar `CLAUDE.md` e `AGENTS.md` específicos do projeto filho

Após a criação, abra o projeto filho em uma nova conversa e rode `/kickoff`.

### Via script direto

```bash
python scripts/new_repo.py --name <nome> --visibility private --yes
```

Flags úteis:
- `--yes` — confirma tudo sem prompts
- `--skip-clone` — cria apenas no GitHub sem pasta local
- `--caveman` / `--skip-caveman` — instala ou pula as skills Caveman

### Via GitHub (manual)

1. Clique em **Use this template** no GitHub
2. Adicione o secret `GH_PAT` no repositório novo
3. Rode a workflow `Setup Kanban` manualmente
4. Clone localmente e abra no Claude Code

---

## Estrutura deste template

```text
.claude/
  agents/                    # definições dos 12 agentes
  commands/
    wizard.md                # /wizard — exclusivo do pai
    review.md                # /review — herdado pelo filho
    deploy.md                # /deploy — herdado pelo filho
    fix-issue.md             # /fix-issue — herdado pelo filho
    clean.md                 # /clean — herdado pelo filho
    sync-to-projects.md      # /sync-to-projects — propaga template → filhos (exclusivo do pai)
    sync-to-template.md     # /sync-to-template — propaga filho → template (exclusivo do pai)
    sync-master.md         # /sync-master — sincroniza camada universal entre templates irmãos
  settings.json              # permissões e operações bloqueadas
scripts/
  new_repo.py                # lógica do wizard
  generate_docs.js           # gerador PDF/DOCX/PPTX
  hooks/
    session_start.sh         # exibe kanban ao iniciar sessão
    post_write.sh            # ruff/black em .py; gera docs em .md de docs/
  templates/
    CLAUDE.md                # gerado no filho com regras de project-manager e commands
    AGENTS.md                # gerado no filho com equipe e fluxos
    README.md                # gerado no filho com overview do projeto
    agents/                  # 12 agentes copiados para .claude/agents/ do filho
    commands/
      kickoff.md             # /kickoff — discovery, pesquisa, relatório, backlog
      advance.md             # /advance — avança no kanban
      review-backlog.md      # /review-backlog — varredura proativa
      update-memory.md       # /update-memory — atualiza memória persistente
      (outros commands)
.agents/
  skills/                    # 11 skills enterprise + caveman x3
.github/
  workflows/
    setup-kanban.yml         # cria Kanban e épicos no projeto filho
    ci.yml                   # CI: ruff, black, pytest
src/
tests/
notebooks/
pyproject.toml
CLAUDE.md                    # instrui o Claude Code quando opera neste template
CLAUDE.local.md.example
.mcp.json.example
.gitignore
AGENTS.md
```

---

## Ferramentas disponíveis nos projetos filho

| Ferramenta | Cobertura |
|---|---|
| `Bash(git:*)` | Todos os comandos git (exceto force push e reset hard) |
| `Bash(gh:*)` | gh CLI — issues, PRs, projects, workflows (exceto operações destrutivas) |
| `Bash(python/pytest/ruff/black/pip/uv:*)` | Desenvolvimento Python completo |
| `WebSearch` / `WebFetch` | Pesquisa web e leitura de URLs |
| MCP GitHub | Leitura e escrita de issues, PRs, branches, reviews |

Operações permanentemente bloqueadas: `git push --force`, `git reset --hard`, `git clean -f`, `gh repo delete`, `gh secret set/delete`, `gh auth login/token`, `gh ssh-key add`.

---

## Observações

- No primeiro push do repo filho, a workflow pode rodar antes de `GH_PAT` existir — ela cria labels e issue inicial mas pula o board. Configure o secret e rode `Setup Kanban` manualmente.
- A view `Board` é criada via API, mas o agrupamento visual por `Status` pode precisar de ajuste manual na interface do GitHub.
- Para projetos com Docker, Terraform, npm ou conda, adicione as permissões no `settings.json` do filho — não estão no template por serem projeto-específicas.
