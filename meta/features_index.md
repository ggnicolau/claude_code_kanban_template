# Features Index — Claude Code Web Automation
# Para uso do agente durante implementação. Fonte de verdade de IDs, status e arquivos.

## Legenda
# Tier 1 = commitado no repo, propaga automático
# Tier 2 = /wizard faz ao criar projeto
# Tier 3 = manual por conta, guiado por cloud_guide.md
# Tier 4 = por sessão, documentado em cloud_guide.md
# ✅ = já implementado como proposto | ❌ = não implementado | 🟡 = parcialmente

---

## TIER 1 — Hooks (arquivo: .claude/settings.json → seção "hooks")

| ID  | Feature                                         | Status | Fase | Arquivos a modificar                                                      |
|-----|-------------------------------------------------|--------|------|---------------------------------------------------------------------------|
| A1  | SessionStart → exibir kanban                    | ❌     | 1    | `.claude/settings.json`                                                   |
| A2  | PostToolUse Write *.py → ruff + black           | ❌     | 1    | `.claude/settings.json`                                                   |
| A3  | PostToolUse Write docs/**/*.md → generate_docs  | ❌     | 1    | `.claude/settings.json`                                                   |
| A4  | PostToolUse Write docs/**/*.md → valida refs    | ❌     | 1    | `.claude/settings.json` + `scripts/validate_refs.sh` (criar)              |
| A5  | PreToolUse Write data/raw/** → bloquear         | ❌     | 1    | `.claude/settings.json`                                                   |
| A6  | PreToolUse Bash git add *.csv/xlsx/db → bloquear| ❌     | 1    | `.claude/settings.json`                                                   |
| A7  | PreToolUse Write _vN → arquivar automático      | ❌     | 2    | `.claude/settings.json` + `scripts/archive_version.sh` (criar)            |
| A8  | PreToolUse Bash git push origin main → confirmar| ❌     | 1    | `.claude/settings.json`                                                   |
| G   | SessionStart → scripts/cloud_setup.sh           | ❌     | 1    | `.claude/settings.json` + `scripts/cloud_setup.sh` (criar)                |
| H   | Instrução session URL em agentes                | ❌     | 1    | `.claude/agents/academic-writer.md`, `data-engineer.md`, `peer-reviewer.md` |
| I5  | Instrução /compact vs /clear em cloud           | ❌     | 1    | Todos os agentes relevantes                                               |

## TIER 1 — Propagação automática (já funciona se arquivo existir)

| Item              | Status | Observação                                                                 |
|-------------------|--------|----------------------------------------------------------------------------|
| generate_docs.js  | ✅     | Existe em `scripts/`; copiado para filho pelo wizard                       |
| Commands .md      | ✅     | Copiados de `scripts/templates/commands/` para filho                       |
| Agent prompts     | ✅     | `.claude/agents/` copiado para filho                                       |
| CLAUDE.md         | ✅     | Gerado a partir de `scripts/templates/CLAUDE.md`                           |
| Plugins           | ❌     | Declarar em `.claude/settings.json` seção `enabledPlugins`                 |

---

## TIER 2 — Wizard (arquivo: scripts/new_repo.py + scripts/templates/)

| ID  | Feature                                          | Status | Fase | O que modificar                                                           |
|-----|--------------------------------------------------|--------|------|---------------------------------------------------------------------------|
| B1  | Criar labels GitHub via setup-kanban.yml         | ✅     | —    | Já funciona                                                               |
| B2  | Criar GitHub Project + Kanban                    | ✅     | —    | Já funciona                                                               |
| B3  | Criar .env com GH_TOKEN / secret GH_PAT          | ✅     | —    | Já funciona                                                               |
| B4  | npm install + pip install no projeto criado      | ❌     | 3    | `scripts/new_repo.py` → `cleanup_template_files()`                        |
| B5  | gh repo create + clone local                     | ✅     | —    | Já funciona                                                               |
| B6  | Gerar docs/setup/cloud_guide.md                  | ❌     | 3    | `scripts/new_repo.py` + `scripts/templates/cloud_guide.md.tpl` (criar)    |
| B7  | Configurar /remote-env                           | ❌     | 3    | `scripts/new_repo.py` → após clone, rodar `claude /remote-env`            |
| B8  | Apresentar GitHub App + /autofix-pr              | ❌     | 3    | `scripts/new_repo.py` → print no final do wizard                          |

---

## TIER 3 — Conteúdo do cloud_guide.md (arquivo: scripts/templates/cloud_guide.md.tpl)

| ID  | Feature                                              | Fase | O que documentar                                            |
|-----|------------------------------------------------------|------|-------------------------------------------------------------|
| D4  | /web-setup (pré-requisito de tudo)                   | 4    | `claude /web-setup` no terminal, uma vez por conta         |
| F1  | CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1               | 4    | Env var no ambiente cloud UI                               |
| F2  | CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70                   | 4    | Env var no ambiente cloud UI                               |
| F3  | CLAUDE_CODE_AUTO_COMPACT_WINDOW                      | 4    | Env var opcional                                           |
| F4  | GH_TOKEN no ambiente cloud                           | 4    | Env var no ambiente cloud UI                               |
| F5  | CCR_FORCE_BUNDLE=1                                   | 4    | Env var para repos privados sem GitHub App                 |
| I6  | /remote-env                                          | 4    | `claude /remote-env` no terminal                           |
| J   | Setup script: instalar gh CLI                        | 4    | UI cloud → campo Setup script                              |
| J2  | Níveis de acesso à rede (Trusted padrão)             | 4    | UI cloud → Network access                                  |
| J3  | Docker Compose para análise                          | 4    | Puxar imagens no setup script (cacheado)                   |
| D1  | Rotinas agendadas                                    | 4    | /schedule ou UI de routines                                |
| D2  | Rotina API-triggered                                 | 4    | Webhook externo → /advance                                 |
| D3  | GitHub App (instalar)                                | 4    | github.com/apps/claude, 1 clique                           |

---

## TIER 4 — Workflows documentados no cloud_guide.md

| ID  | Feature                                              | Fase | Comando / Como usar                                         |
|-----|------------------------------------------------------|------|-------------------------------------------------------------|
| I1  | --remote para rodar /advance em cloud                | 5    | `claude --remote "Run /advance"`                           |
| I2  | --remote paralelo (múltiplos agentes)                | 5    | Múltiplos `claude --remote` simultâneos                    |
| I3  | /autofix-pr                                          | 5    | Ativar após GitHub App instalado                           |
| I4  | --teleport / /teleport                               | 5    | `claude --teleport` ou `/teleport` dentro de sessão        |
| I7  | /tasks                                               | 5    | Monitorar sessões cloud do terminal                        |
| I8  | check-tools (debug cloud)                            | 5    | Rodar `check-tools` dentro de sessão cloud                 |
| I9  | --remote + plan mode / ultraplan                     | 5    | Planeja local, executa cloud autonomamente                 |
| I10 | Diff review com comentários inline                   | 5    | Web UI: comentar linha a linha no diff                     |
| I11 | Compartilhamento de sessão                           | 5    | Toggle visibilidade na sessão web                          |
| I12 | ultraplan                                            | 5    | Plano no browser, você revisa antes de executar            |
| I13 | ultrareview                                          | 5    | Code review multi-agente em sandbox cloud                  |
| I14 | --remote-control (máquina local acessível)           | 5    | `claude --remote-control` na máquina de casa               |
| D5  | Sessões em segundo plano (mobile)                    | 5    | App mobile Claude para monitorar                           |

---

## NÃO IMPLEMENTAR

| Feature                        | Motivo                                                    |
|--------------------------------|-----------------------------------------------------------|
| Auto-push via hook             | Risco de vazar dados sensíveis                            |
| MCP servers via hooks          | Gerenciado pelo .mcp.json — duplicar cria conflito        |
| SSO interativo (AWS SSO)       | Não suportado em cloud                                    |
| Substituir imagem base Docker  | Não suportado ainda                                       |
| Session artifacts além de H    | Overhead desnecessário                                    |

---

## Arquivos a criar ou modificar por fase

### Fase 1
- `.claude/settings.json` — adicionar seção `hooks` (A1-A6, A8, G)
- `scripts/cloud_setup.sh` — novo (G)
- `scripts/validate_refs.sh` — novo (A4)
- `.claude/agents/academic-writer.md` — adicionar instrução H e I5
- `.claude/agents/data-engineer.md` — adicionar instrução H e I5
- `.claude/agents/peer-reviewer.md` — adicionar instrução H e I5

### Fase 2
- `.claude/settings.json` — adicionar hook A7
- `scripts/archive_version.sh` — novo (A7)

### Fase 3
- `scripts/new_repo.py` — adicionar B4, B6, B7, B8
- `scripts/templates/cloud_guide.md.tpl` — novo template para B6

### Fase 4 e 5
- `scripts/templates/cloud_guide.md.tpl` — preencher conteúdo Tier 3 e Tier 4

---

## Arquivos que NÃO propagam para filho (TEMPLATE_ONLY_DIRS em new_repo.py)

```
scripts/templates/   ← já na lista
meta/                ← ADICIONAR (este relatório, features_index.md, XLS)
docs/process/        ← ADICIONAR ou mover conteúdo para meta/
```
