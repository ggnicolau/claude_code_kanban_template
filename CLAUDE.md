# Claude Code Kanban Template — Instruções para o Claude Code

Este repositório é um **template de criação de projetos**. Quando você está aqui, seu papel é ajudar a criar novos projetos a partir deste template — não desenvolver produto.

## Regra de Início

**Ao iniciar qualquer conversa neste repositório, exiba imediatamente esta mensagem — antes de qualquer outra resposta:**

```
🏭 claude-code-enterprise-template

Para criar um novo projeto enterprise:
  /wizard

Para manter ou melhorar o template, me diga o que precisa.
```

---

## Seu papel aqui

Você opera como **ferramenta de criação de repositórios**. O que faz sentido neste contexto:

- Rodar `/wizard` para criar um novo projeto filho
- Manter e melhorar os arquivos do template (agentes, commands, workflows, scripts)
- Não há kanban de produto aqui, não há backlog de features, não há agentes de especialidade sendo acionados

## O que este template cria

Ao rodar `/wizard`, um novo repositório filho é criado com:

- 12 agentes especializados em `.claude/agents/`
- Kanban no GitHub Projects pré-populado com épicos de negócio, produto, tech, lançamento e operações
- Commands: `/kickoff`, `/advance`, `/review-backlog`, `/review`, `/deploy`, `/fix-issue`, `/clean`, `/update-memory`
- Memória persistente (`.claude/memory/user_profile.md`, `project_genesis.md`, `MEMORY.md`) criada na Fase 0 do `/kickoff`
- Gerador `scripts/generate_docs.js` (PDF/DOCX/PPTX) + `package.json` + `styles/`
- Convenção de versionamento `{nome}_YYYY-MM-DD_v{N}.md` — agentes nunca sobrescrevem versão anterior
- CI/CD configurado (ruff, black, pytest)
- `CLAUDE.md` e `AGENTS.md` gerados especificamente para o projeto filho

O filho começa com `/kickoff` — que conduz discovery, monta backlog completo e obtém aprovação antes de qualquer execução.

## Arquivos importantes deste template

| Arquivo | Propósito |
|---|---|
| `scripts/new_repo.py` | Lógica do wizard de criação (copia templates + package.json + styles/ + generate_docs.js) |
| `scripts/generate_docs.js` | Gerador PDF/DOCX/PPTX a partir dos MDs em `docs/` |
| `scripts/templates/CLAUDE.md` | CLAUDE.md gerado no filho |
| `scripts/templates/AGENTS.md` | AGENTS.md gerado no filho |
| `scripts/templates/README.md` | README gerado no filho |
| `scripts/templates/package.json` | Deps do gerador (copiado para o filho) |
| `scripts/templates/styles/` | Estilos do PDF/DOCX (copiados para o filho) |
| `scripts/templates/commands/kickoff.md` | Command `/kickoff` (com Fase 0 narrativa) copiado para o filho |
| `.github/workflows/setup-kanban.yml` | Cria o Kanban e épicos no projeto filho |
| `.claude/commands/wizard.md` | Command `/wizard` — só existe no pai |
| `.claude/commands/sync-to-projects.md` | Propaga mudanças do template para os projetos filhos |
| `.claude/commands/sync-to-template.md` | Propaga melhorias de um filho de volta para o template |
| `.claude/commands/sync-master.md` | Sincroniza camada universal entre templates irmãos |

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

### Mensagens de commit — referenciar issue

Todo commit deve referenciar a issue correspondente no Kanban:

```bash
feat: expand cloud_guide.md (closes #42)
fix: wizard encoding issue (#50)
chore(system): sync commands from template (#38)
```

- Use `closes #N` quando o commit resolve a issue completamente
- Use `#N` quando é progresso parcial
- Commits sem issue associada (ex: typos, refactor menor) dispensam referência

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

## Sessões Cloud — Rastreabilidade

Ao abrir PR ou commitar em sessão cloud, incluir no corpo do PR o link da sessão:

```bash
[ -n "$CLAUDE_CODE_REMOTE_SESSION_ID" ] && echo "Sessão: https://claude.ai/code/${CLAUDE_CODE_REMOTE_SESSION_ID}"
```

Se `CLAUDE_CODE_REMOTE_SESSION_ID` não existir (sessão local), omitir.

## Contexto em Sessões Cloud

- `/compact` → disponível em cloud — resume e libera contexto
- `/clear` (comando interno do Claude) → **não disponível** em cloud — usar `/compact`
- `/clean` (command do projeto) → funciona em qualquer ambiente

---

## Iniciar

Use `/wizard` para criar um novo projeto filho.
