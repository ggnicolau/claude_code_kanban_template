# Claude Code Kanban Template — Instruções para o Claude Code

Este repositório é um **template de criação de projetos**. Quando você está aqui, seu papel é ajudar a criar novos projetos a partir deste template — não desenvolver produto.

## Seu papel aqui

Você opera como **ferramenta de criação de repositórios**. O que faz sentido neste contexto:

- Rodar `/wizard` para criar um novo projeto filho
- Manter e melhorar os arquivos do template (agentes, commands, workflows, scripts)
- Não há kanban de produto aqui, não há backlog de features, não há agentes de especialidade sendo acionados

## O que este template cria

Ao rodar `/wizard`, um novo repositório filho é criado com:

- 12 agentes especializados em `.claude/agents/`
- Kanban no GitHub Projects pré-populado com épicos de negócio, produto, tech, lançamento e operações
- Commands: `/kickoff`, `/advance`, `/review-backlog`, `/review`, `/deploy`, `/fix-issue`, `/clean`
- CI/CD configurado (ruff, black, pytest)
- `CLAUDE.md` e `AGENTS.md` gerados especificamente para o projeto filho

O filho começa com `/kickoff` — que conduz discovery, monta backlog completo e obtém aprovação antes de qualquer execução.

## Arquivos importantes deste template

| Arquivo | Propósito |
|---|---|
| `scripts/new_repo.py` | Lógica do wizard de criação |
| `scripts/templates/CLAUDE.md` | CLAUDE.md gerado no filho |
| `scripts/templates/AGENTS.md` | AGENTS.md gerado no filho |
| `scripts/templates/kickoff.md` | Command `/kickoff` copiado para o filho |
| `.github/workflows/setup-kanban.yml` | Cria o Kanban e épicos no projeto filho |
| `.claude/commands/wizard.md` | Command `/wizard` — só existe no pai |
| `.claude/commands/sync-to-projects.md` | Propaga mudanças do template para os projetos filhos |
| `.claude/commands/sync-to-template.md` | Propaga melhorias de um filho de volta para o template |

## Regras de branches neste template

```
feature/* → dev → main
```

- Merges de `feature/*` → `dev`: usar `gh pr merge --merge --delete-branch` (feature branches são descartáveis)
- Merges de `dev` → `main`: usar `gh pr merge --merge` **sem** `--delete-branch` (dev é permanente)

### Cleanup obrigatório após merge

**Após merge de feature → dev:**
```bash
git checkout dev && git pull && git branch -D <nome-do-branch> 2>/dev/null || true
```

**Após merge de dev → main:**
```bash
git checkout main && git pull origin main && git checkout dev && git merge main --no-edit && git push origin dev
```

O `git merge main` final é obrigatório — traz o commit de merge para o dev e evita o banner de divergência no Claude Code. Sem esse passo o workspace fica sujo.

### Push direto em dev (documentação e skills)

Alterações em `docs/`, `.agents/skills/`, arquivos `.md` de agentes e commands do template podem ser commitadas e pusadas diretamente em `dev` — sem branch, sem PR.

```bash
git add <arquivo>
git commit -m "..."
git push origin dev
```

Nunca push direto em `main`.

### Autenticação GitHub

Dois mecanismos disponíveis:

| Ferramenta | Como autentica | Quando usar |
|---|---|---|
| `gh` CLI | `GH_TOKEN` do `.env` | merge, delete-branch, PR, issues via terminal |
| MCP GitHub | token do `.mcp.json` (automático) | operações via ferramentas MCP do Claude |

**Antes de usar `gh` CLI**, carregue o token:
```bash
export GH_TOKEN=$(grep GH_TOKEN .env | cut -d= -f2)
```

**Nunca usar** `gh auth login` — as permissões bloqueiam esse comando. O `GH_TOKEN` no `.env` é o mecanismo correto.

### Resolver banner de divergência no Claude Code

Se aparecer o banner "branch diverged from remote", significa que dev local está dessincronizado com o remoto após um merge de main. Solução:

```bash
git checkout dev && git pull origin dev
```

Se ainda divergir após merge de dev → main:
```bash
git checkout dev && git merge main --no-edit && git push origin dev
```

## Iniciar

Use `/wizard` para criar um novo projeto filho.
