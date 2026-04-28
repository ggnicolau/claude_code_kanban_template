# Claude Code Web Features — Relatório de Automação do Template Acadêmico

> **Para quem é este arquivo:** você, o pesquisador e dono do template.
> Foco em POR QUÊ cada feature importa, o que ela resolve, e o que já existe.
> Para detalhes de implementação, veja `features_index.md`.

---

## O que este relatório cobre

Durante uma sessão de trabalho, mapeamos todas as features do Claude Code na Web que podem ser aproveitadas neste template. O objetivo é dois:

1. **Automatizar ao máximo** o que qualquer usuário do template recebe sem configurar nada
2. **Guiar o que não dá pra automatizar** (são por conta, não por repo) com um documento gerado automaticamente

---

## Seus interesses específicos — onde cada um se encaixa

### GitHub App + Claude (auto-fix de CI e comentários automáticos)
- O GitHub App precisa ser instalado uma vez por repo (1 clique em github.com/apps/claude)
- Depois disso, Claude monitora PRs e corrige falhas de CI sozinho — você ativa com `/autofix-pr`
- O wizard vai lembrar o usuário de instalar e vai explicar o comando
- **Status:** não implementado — entra na Fase 3 (wizard) e Fase 4 (cloud_guide.md)

### Celular + cloud (sessão rodando sem você, monitorar de longe)
- Depende de um passo único: `/web-setup` no terminal para sincronizar seu token `gh` com a conta Claude
- Depois disso, você abre `claude.ai/code` no celular e vê todas as sessões rodando
- Pode mandar mensagens, orientar Claude, aprovar coisas — tudo pelo celular
- **Status:** não implementado — entra na Fase 4 (cloud_guide.md) como checklist guiado

### Controle remoto da sua máquina em casa
- `--remote-control` é diferente de `--remote`: não usa a cloud da Anthropic, expõe sua sessão local para acesso externo
- Útil quando quer que Claude rode na sua máquina mas você está fora
- **Status:** não implementado — entra na Fase 5 como workflow documentado

### Sandbox isolada
- Toda sessão cloud do Claude Code já É uma sandbox (VM isolada gerenciada pela Anthropic)
- Você não está usando hoje porque não fez `/web-setup` ainda
- Quando fizer, automaticamente passa a ter sandbox sem configuração extra
- **Status:** automático — zero configuração adicional após `/web-setup`

### Tarefas paralelas
- `claude --remote` cria sessões independentes — você pode rodar `literature-reviewer` e `methodologist` ao mesmo tempo em VMs separadas
- Com `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` no ambiente cloud, agentes dentro de uma sessão também rodam em paralelo
- **Status:** F1 entra no cloud_guide.md; padrão de uso entra na Fase 5

---

## O que já existe no template (não reimplementar)

| Feature | O que já tem | O que falta |
|---|---|---|
| Gerar PDF/DOCX | `scripts/generate_docs.js` existe; CLAUDE.md instrui agentes | Hook `PostToolUse` que dispara automaticamente |
| ruff + black | `settings.json` tem `allow` para ruff e black | Hook `PostToolUse` que roda automaticamente ao editar `.py` |
| Proteções destrutivas | `settings.json` tem `deny` para `--force`, `reset --hard`, `clean -f` | Hooks específicos para `data/raw/`, `git add *.csv`, `push origin main` |
| Criar repo + Kanban | `new_repo.py` + `setup-kanban.yml` fazem tudo | — |
| Configurar GH_TOKEN | wizard lê de `.env` ou `.mcp.json` e configura secret `GH_PAT` | — |
| Criar branch dev | wizard faz | — |

---

## O que vai ser implementado e por quê

### Fase 1 — Hooks automáticos (Tier 1) — alto impacto, zero esforço do usuário

Todos os hooks ficam em `.claude/settings.json` commitado — chegam no filho e na cloud automaticamente.

| Hook | Problema que resolve |
|---|---|
| `SessionStart` → exibe kanban | Hoje o CLAUDE.md instrui o agente a exibir, mas depende do agente ler a instrução. Hook dispara antes de tudo. |
| `PostToolUse` (Write `.py`) → ruff + black | Hoje é allow (permissão), não automático. Agente pode esquecer. |
| `PostToolUse` (Write `docs/**/*.md`) → generate_docs.js | Hoje CLAUDE.md instrui — agente frequentemente esquece. Hook garante. |
| `PostToolUse` (Write `docs/**/*.md`) → valida referências | Problema recorrente: referências mencionadas no texto que não estão na lista. Hook detecta antes do commit. |
| `PreToolUse` (Write `data/raw/**`) → bloquear | Regra existe no CLAUDE.md mas pode ser ignorada. Hook torna impossível. |
| `PreToolUse` (Bash `git add *.csv/xlsx`) → bloquear | Sem hook, dados brutos podem entrar no repo acidentalmente. |
| `PreToolUse` (Bash `git push origin main`) → confirmar | Hoje só tem deny para `--force`. Push direto na main sem `--force` passa. |
| `SessionStart` → `cloud_setup.sh` | Instala deps e inicia PostgreSQL/Redis automaticamente em sessões cloud. Usa `CLAUDE_CODE_REMOTE=true` para não rodar local. |

Além dos hooks, os agentes `academic-writer`, `data-engineer` e `peer-reviewer` vão receber instrução para incluir a URL da sessão cloud no corpo de PRs — trilha de auditoria de quem produziu o quê.

### Fase 2 — Hook de arquivamento automático (Tier 1, complexo)

Antes de sobrescrever qualquer arquivo `docs/**/*_vN.md`, move o anterior para `archive/` automaticamente. Hoje isso é regra no CLAUDE.md — agentes frequentemente pulam.

### Fase 3 — Wizard: o que falta (Tier 2)

O wizard já faz bastante (repo, Kanban, labels, clone, branch dev). O que falta:
- Rodar `npm install` + `pip install` no projeto criado
- Gerar `docs/setup/cloud_guide.md` — checklist personalizado de todos os passos manuais
- Configurar `/remote-env` para o projeto
- Apresentar link do GitHub App e explicar `/autofix-pr`

### Fase 4 — `cloud_guide.md`: passos manuais guiados (Tier 3)

Coisas que vivem na conta da pessoa, não no repo. O wizard gera o documento, o usuário segue:
1. `/web-setup` — sincronizar token (pré-requisito de tudo)
2. Variáveis de ambiente no ambiente cloud: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70`, `GH_TOKEN`
3. Setup script do ambiente cloud: instalar `gh` CLI (resultado é cacheado 7 dias)
4. Níveis de acesso à rede (padrão `Trusted` já cobre tudo necessário)
5. Docker Compose para ambientes de análise reprodutíveis
6. Rotinas agendadas (ex: toda segunda `/review-backlog`)
7. Instalar GitHub App (1 clique)

### Fase 5 — Workflows documentados (Tier 4)

O que não é automatizável, mas deve estar documentado para o usuário não precisar descobrir:
- `claude --remote "Run /advance"` — kanban na cloud, persiste sem browser
- `--remote` paralelo — múltiplos agentes ao mesmo tempo
- `/autofix-pr` — Claude corrige CI automaticamente
- `--teleport` — puxar sessão cloud de volta ao terminal
- `/tasks` — monitorar sessões do terminal
- Diff review com comentários inline — workflow para revisão com orientador
- Compartilhamento de sessão — orientador revisa sem instalar nada
- `ultraplan` e `ultrareview` — planejar e revisar em cloud
- `--remote-control` — sua máquina acessível de fora

---

## Distinção crítica: Setup script vs. Hook SessionStart

Esta distinção importa para não implementar a coisa errada no lugar errado:

| | Setup script (UI cloud) | Hook SessionStart (commitado) |
|---|---|---|
| Onde configurar | UI do claude.ai/code | `.claude/settings.json` no repo |
| Quando roda | Antes do Claude iniciar, só se não há cache | Toda sessão, inclusive retomadas |
| Resultado é cacheado? | ✅ ~7 dias | ❌ roda sempre |
| Propaga para filhos? | ❌ por conta | ✅ automático |
| Usar para | Instalar `gh`, Docker images pesadas | `npm install`, `pip install`, iniciar serviços |

---

## O que não implementar e por quê

| Feature | Motivo |
|---|---|
| Auto-push após todo commit | Risco de vazar dados sensíveis |
| MCP servers via hooks | Já gerenciado pelo `.mcp.json` — duplicar cria conflito |
| SSO interativo (AWS SSO) | Não suportado em cloud — requer login baseado em browser |
| Substituir imagem base Docker | Não suportado ainda |
| Session artifacts além da URL | Overhead desnecessário além da URL de sessão já prevista |
