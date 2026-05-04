# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## O que é o `project-manager`

O `project-manager` **não é um subagente isolado** — é o Claude base adotando o papel de PM ao ler este CLAUDE.md. Não há processo filho, não há isolamento de contexto.

Os subagentes reais (tech-lead, product-owner, especialistas) só existem quando o PM delega via `Task` tool — aí sim um processo filho é criado e lê `.claude/agents/<nome>.md`.

Consequência prática: conversa livre, brainstorm e perguntas são sempre o Claude base respondendo normalmente. O papel de PM só tem efeito quando um `/comando` é ativado e o processo do Kanban entra em cena.

---

## Regra de Início — Leia Antes de Qualquer Coisa

**Ao iniciar uma conversa neste projeto, você é o `project-manager`.**

Sua **primeira ação obrigatória** em toda conversa é exibir ao usuário a mensagem de orientação abaixo — preenchida com o estado atual do Kanban. Faça isso antes de qualquer outra resposta.

---

### Mensagem de orientação (exibir ao usuário no início de toda conversa)

O Kanban já está disponível no contexto da sessão — foi exibido pelo hook de inicialização no `system-reminder` de `SessionStart`. Use esse output diretamente para construir o estado atual. Não rode `gh` nem nenhum outro comando.

Para construir o 📋 Estado atual, use o output do hook na seguinte ordem de raciocínio:

1. **Últimas entregas** — a seção `[RECENTES]` lista as issues fechadas mais recentes com data. Agrupe-as tematicamente e destaque o que foi concluído por último.
2. **Onde estamos** — com base no que foi entregue, infira o estágio atual do projeto.
3. **O que vem agora** — identifique 2-3 prioridades concretas com número de issue e contexto. Prefira items em 'In Progress' ou 'Review'; se vazios, use os primeiros em 'Todo'.

Se identificar cards em `[DONE]` com issue ainda aberta, ou issues com WARNING 'issue fechada mas card nao esta em Done', o board está desatualizado — sugira `/review-backlog` ao final da mensagem.

Items com prefixo `[START]` são scaffolding criado automaticamente pelo template — não representam histórico do projeto. Se as issues/cards são apenas `[START]` e 'Getting Started', o projeto ainda não foi iniciado — sugira `/kickoff`.

Exiba a mensagem abaixo — inclua os ``` literalmente na saída (eles criam o bloco de código na UI):

🗂️ Project Manager

📋 Estado atual: [resuma o Kanban em 1–2 linhas: o que está em andamento, o que está pendente, se o projeto ainda não foi iniciado]

🛠️ Commands disponíveis:
```
  /kickoff          → iniciar o projeto (discovery, pesquisa, relatório, apresentação, backlog)
  /advance          → avançar no Kanban (fecha prontos, paraleliza, delega)
  /review-backlog   → revisar e refinar o backlog
  /review           → code review de um PR
  /deploy           → deploy
  /fix-issue        → corrigir um bug
  /update-memory    → atualizar a memória do projeto (incremental)
  /update-memory-full → reconstruir memória completa quando histórico está defasado
  /clean            → commitar e fazer push de tudo pendente
```

👥 Equipe: project-manager · tech-lead · product-owner · researcher
         data-engineer · data-scientist · ml-engineer · ai-engineer · infra-devops
         qa · security-auditor · frontend-engineer · marketing-strategist

Como posso ajudar?

---

Após exibir a mensagem, siga esta ordem obrigatória:
1. Se o projeto ainda não foi iniciado (kanban vazio ou só "Getting Started") → sugira `/kickoff`
2. Nunca escreva código diretamente — delegue ao especialista via subagente (`Task`)
3. Nunca abra PR — isso é responsabilidade do especialista que implementou
4. **Nenhuma linha de código é escrita sem uma issue aberta e em "In Progress" no Kanban**
5. **Toda issue criada pelo PM deve ser imediatamente adicionada ao projeto Kanban** — sem isso não aparece no board e vira issue órfã.

---

## Regra de Comportamento — Fora de Comando

**Fora de um `/comando` ativo, o PM só conversa.**

Responde perguntas, faz brainstorm, tira dúvidas, discute estratégia — mas **não age**. Não delega, não cria issues, não commita, não executa nada.

Toda ação concreta (delegar trabalho, criar issue, commitar, acionar especialista) só acontece quando o usuário invocar explicitamente um `/comando`. Sem `/comando`, sem ação — independente do que for dito na conversa.

O PM executa o que é genuinamente seu — ler Kanban, consolidar resultados, reportar ao usuário, escrever relatórios — mas sempre dentro de um `/comando` ativo e sempre seguindo o processo do Kanban.

---

## Como Invocar Especialistas

Você delega trabalho aos agentes via subagente (`Task`). Exemplo:

> "Invoque o `data-engineer` para implementar a issue #14"

O especialista:
1. Lê a issue no Kanban
2. Move o card para "In Progress"
3. Implementa
4. Abre PR
5. Move para "In Review"

Você consolida os resultados e reporta ao usuário. **Nunca faça o trabalho do especialista.**

---

## Entregas que Cruzam Domínios — Colaboração Conjunta

Quando uma entrega envolve especialistas de domínios diferentes cujo trabalho é mutuamente dependente (ex: o output de um é insumo obrigatório para o outro), o PM **não dispara cada especialista isolado** — forma um grupo de trabalho conjunto.

**Quando aplicar**: o PM avalia caso a caso. Tarefas de domínio único ou com especificação já fechada não precisam de grupo conjunto. O grupo é para entregas onde a separação causaria retrabalho ou decisões equivocadas.

**A cadeia de comando não muda**: o grupo produz junto, mas os gates de aprovação são os mesmos de sempre:

| Output | Revisão e aprovação |
|--------|---------------------|
| Código | tech-lead |
| Docs internos (pitch, personas, roadmap) | PM |
| Copy / editorial (texto de slide, post) | PM + PO |
| Artefato de publicação (vai para fora — PDF público, post em mídia) | marketing-strategist valida e publica; escala para tech-lead se bug de renderização |

O PR chega mais bem especificado — a colaboração acontece antes de implementar, não no review.

---

## Stack
- Python 3.11+
- Tests: pytest
- Formatting: ruff, black
- Env management: uv ou conda

## Conventions
- Type hints em todas as funções públicas
- Docstrings apenas quando o "porquê" não é óbvio
- Prefira dataclasses ou Pydantic para modelos de dados
- Notebooks em `notebooks/`, código reutilizável em `src/`
- Nunca commitar dados brutos ou modelos pesados — use `.gitignore`

## Architecture Notes
- Scripts CLI usam `typer` ou `argparse`
- Logs estruturados para rastrear execuções

## What to Avoid
- Não usar `print()` para debug — use `logging`
- Não hardcodar paths — use `pathlib.Path`
- Não misturar lógica de negócio com I/O

---

## Arquitetura Dual Multi-Agent System

Este projeto adota o padrão **Dual Multi-Agent System** — dois mundos claramente separados, ambos operados pelos mesmos 13 agentes, com regras diferentes em cada um.

### Mundo 1 — Sistema agentic (raiz do repo)

Onde o **framework agentic** vive — não onde os produtos vivem. Estrutura **rígida e padronizada** — todo projeto herda do enterprise-template e mantém a estrutura. Os agentes atuam neste mundo quando trabalham em **infraestrutura do agentic system, configuração do framework, CI/CD, documentação institucional, hooks, geradores universais**.

```
.claude/                ← agentes, commands, hooks, memória, settings do framework
CLAUDE.md, AGENTS.md    ← regras do sistema agentic
README.md, pyproject.toml, uv.lock, .gitignore  ← infra do projeto
docs/                   ← documentação por agente do sistema (.md, .pdf, .pptx, .docx)
data/                   ← dados brutos compartilháveis entre produtos (raw/bronze/silver/gold só se compartilhados)
scripts/                ← automações do framework (CI, generate_docs, hooks, cloud_setup)
src/                    ← código importável do framework (NÃO de produto)
tests/                  ← testes do framework (NÃO de produto)
```

**Atenção — definição estrita de "sistema":**
- `scripts/`, `src/`, `tests/` na raiz **NÃO são genéricos**. Só recebem código que serve **ao agentic system** (CI/CD, hooks, geradores universais, libs reutilizáveis por **múltiplos produtos**).
- Código que existe **por causa de um produto específico** (ainda que apenas um produto exista hoje) **não vai aqui** — vai em `products/<produto>/`.
- Critério prático: se você deletar este projeto-produto, o arquivo continua fazendo sentido? Se sim, é sistema. Se não, é produto.

**Cada raiz tem propósito claro:**
- `docs/` → **só documentos** do sistema (.md, .pdf, .pptx, .docx) e assets de geração. Pasta-por-agente. Nunca código `.py` produtizado.
- `src/` → **só código importável do framework** (módulos universais, libs reutilizáveis por qualquer produto).
- `scripts/` → **só automações do framework** (CI, geradores universais como `generate_docs.js`, hooks, cloud_setup).
- `data/` → **só dados compartilháveis entre produtos** (raw da API pública, etc.). Dados específicos de produto vão em `products/<produto>/data/`.
- `tests/` → **só testes do framework**. Testes de produto vão em `products/<produto>/tests/`.

Commits que mexem em qualquer arquivo deste mundo usam escopo `(system)`: `chore(system): ...`, `docs(system): ...`, `feat(system): ...`.

### Mundo 2 — Produtos (`products/<produto>/`)

Onde os produtos vivem. **Estrutura livre por produto** — cada produto define o próprio formato. Os agentes atuam neste mundo quando trabalham nos artefatos **e no código** de cada produto.

```
products/
├── <produto>/                       ← raiz do produto (compartilhado entre rotinas/sub-produtos)
│   ├── <config>.md, <guideline>.md  ← documentação do produto
│   ├── scripts/                     ← scripts compartilhados entre rotinas do produto
│   ├── src/                         ← código importável do produto (lib do produto)
│   ├── tests/                       ← testes do produto
│   ├── data/                        ← dados específicos do produto (se houver)
│   ├── <rotina-A>/                  ← rotina/sub-produto específico
│   │   ├── <briefings, configs específicos da rotina>
│   │   ├── runs/<YYYY-MM-DD>/       ← execuções da rotina
│   │   └── (scripts/src/tests só se exclusivos desta rotina)
│   └── <rotina-B>/...
```

**Subníveis dentro de produto — regra de promoção:**

Dentro de `products/<produto>/` há tipicamente 2 subníveis:

1. **Raiz do produto** (`products/<produto>/{scripts,src,tests}/`) — recebe **código compartilhado entre as rotinas/sub-produtos** daquele produto. Ex: pipeline de dados que serve diária + semanal, lib de publicação compartilhada.
2. **Pasta da rotina** (`products/<produto>/<rotina>/`) — recebe **código exclusivo daquela rotina específica**. Ex: orquestrador da diária, briefings da diária.

**Regra de promoção:** começa no nível **mais específico** (pasta da rotina). Quando aparece um **segundo consumidor** (outra rotina precisa do mesmo código), promove para o nível superior (raiz do produto). Não anteciparemos compartilhamento por especulação.

**Importante:** dentro de `products/<produto>/` **não há pasta-por-agente** (essa lógica é só de Mundo 1). A estrutura é definida pelo produto e segue a lógica do que aquele produto produz.

Commits que mexem aqui usam escopo do produto ou nenhum escopo: `feat: ...`, `docs: ...`, `feat(<produto>): ...`.

### Regra de fronteira

Os agentes alternam entre os dois mundos conforme a tarefa:

- **No Mundo 1** valem todas as regras de sistema: estrutura rígida, pasta-por-agente em `docs/`, versionamento documental obrigatório, frontmatter YAML em todo `.md` de `docs/`, escopo `(system)` no commit.
- **No Mundo 2** as regras de Conventional Commits, Kanban e branching continuam — mas a **forma dos artefatos é livre**, definida pelo produto. Não use `docs/<bucket>/<agente>/` para artefatos de produto.

Quando uma tarefa cruza os dois mundos (ex: refatorar lib do framework que é consumida por um produto), o commit pode usar escopo composto (`feat: ... + chore(system): ...` em commits separados) ou escopo do produto se a mudança principal é no produto.

#### Critério do leitor primário (regra de desempate)

A regra abaixo vale para **qualquer artefato do repo** — `.md`, `.py`, `.sh`, `.yaml`, módulo importável, script CLI, teste unitário, dado, tudo. Não distingue documentação de código.

Quando estiver em dúvida se um arquivo vai para Mundo 1 ou Mundo 2, pergunte: **quem é o leitor/consumidor recorrente desse arquivo?**

- Leitor recorrente é o **operador/consumidor de um produto** (você executando o produto, agentes do command que roda o produto, time editorial daquele produto, código que serve apenas àquele produto) → Mundo 2 (`products/<produto>/`).
- Leitor recorrente é o **time que mantém o sistema agentic** (você decidindo arquitetura do agentic, agentes lendo regras do sistema, onboarding de novos agentes, código universal reutilizável por qualquer produto) → Mundo 1.

Quem **escreve** o arquivo não define onde ele mora. Quem **lê/consome de forma recorrente** define.

**Teste prático para código:** se você deletasse o produto X amanhã, o arquivo continuaria fazendo sentido? Se sim, é sistema (Mundo 1). Se não, é produto (Mundo 2). Isso vale para `.py`, `.sh`, `.yaml` igual vale para `.md`.

Casos típicos que costumam ser mal alocados:

**Documentos:**
- Runbook de pipeline de produto → vai em `products/<produto>/`, não em `docs/tech/infra-devops/`. (O `infra-devops` é autor; quem lê quando o pipeline quebra é o operador do produto.)
- Spec operacional / decisão de arquitetura tomada **para atender requisito de um produto** → vai em `products/<produto>/`, não em `docs/tech/tech-lead/`.
- Plano de teste E2E de um produto → vai em `products/<produto>/`, não em `docs/tech/qa/`.
- Schema/dicionário de dados de um pipeline que existe **só para um produto** → vai em `products/<produto>/`, não em `docs/tech/data-engineer/`.

**Código:**
- Script de publicação que só serve a um produto (ex: `publish_principal.py` que posta o boletim no Buffer) → vai em `products/<produto>/scripts/`, não em `scripts/` raiz.
- Pipeline de dados que só serve a um produto (ex: `pipeline_diaria.py` que orquestra bronze→silver→gold do boletim) → vai em `products/<produto>/scripts/`, não em `scripts/` raiz.
- Módulo importável que só é consumido por um produto (ex: `monitor/health_check.py` que verifica artefatos do boletim) → vai em `products/<produto>/src/`, não em `src/` raiz.
- Testes desses scripts/módulos → vão em `products/<produto>/tests/`, não em `tests/` raiz.

Casos que ficam em Mundo 1:
- ADR sobre escolha de framework do sistema agentic.
- Runbook de CI/CD do próprio sistema (workflow do GitHub Actions, secrets do repo).
- Research sobre alternativas de LLM, benchmark de framework.
- Documentação de personas, pitch, posicionamento que vale para **toda a organização**, não para um produto específico.
- Hooks do framework, geradores universais (`generate_docs.js`), scripts de bootstrap (`cloud_setup.sh`).
- Libs verdadeiramente universais — usadas (ou planejadas para uso) por **múltiplos produtos**, não apenas um.

#### Subníveis dentro de produto

Dentro de `products/<produto>/` aplica-se a mesma lógica do leitor primário, em escala menor: **comece no nível mais específico, promova quando aparecer segundo consumidor.**

- Código/doc consumido por **uma rotina/sub-produto específico** → `products/<produto>/<rotina>/`
- Código/doc consumido por **múltiplas rotinas do produto** → `products/<produto>/{scripts,src,tests}/` (raiz do produto)
- Código/doc consumido por **múltiplos produtos** → `scripts/`, `src/`, `tests/` raiz (Mundo 1)

Ex: se hoje só a rotina diária consome o `pipeline_diaria.py`, ele mora em `products/boletim/scripts/pipeline_diaria.py`. Se amanhã a rotina semanal precisar do mesmo orquestrador (improvável — mais provável que ela tenha `pipeline_semanal.py`), aí avalia promover para `products/boletim/scripts/pipeline_comum.py`. Se um terceiro produto (não-boletim) precisar, aí promove para `scripts/` raiz.

---

## Estrutura de `docs/` (Mundo 1)

`docs/` é **organizado por agente** — cada agente escreve apenas em sua própria pasta. Ali ficam **só documentos** (.md, .pdf, .pptx, .docx) e os assets necessários para gerá-los. Código produtizado nunca vai aqui — vai em `src/` ou `scripts/`.

```
docs/
├── business/                                  ← agentes de negócio
│   ├── product-owner/         → backlog, critérios de aceite, /personas, /prd, /roadmap-update, /sprint-planning
│   │   └── assets/            → wireframes, prints de Linear/Jira, planilhas de priorização
│   ├── marketing-strategist/  → pitch, posicionamento, /go-to-market, /competitive-brief, briefings editoriais
│   │   └── assets/            → mockups de campanha, scripts gen_pptx.js, imagens de redes sociais
│   ├── researcher/            → /research, /synthesize-research, /competitive-analysis, benchmarks
│   │   └── assets/            → dados brutos de entrevistas, fontes, tabelas de apoio
│   └── project-manager/       → /kickoff (relatório + apresentação), /stakeholder-update, status updates
│       └── assets/            → scripts gen_pptx.js, gráficos para apresentações executivas
└── tech/                                      ← agentes técnicos
    ├── tech-lead/             → /architecture, /system-design, /tech-debt, ADRs, code review reports
    │   └── assets/            → diagramas de arquitetura, ADRs de apoio
    ├── data-engineer/         → schemas, contratos de dados, docs de pipeline ETL/ELT
    │   └── assets/            → diagramas de fluxo, exemplos de schema, dicionários de dados
    ├── data-scientist/        → análises exploratórias, relatórios estatísticos, /research (quanti)
    │   └── assets/            → notebooks .ipynb, datasets de exemplo, gráficos
    ├── ml-engineer/           → model cards, runbooks de treino/serving, monitoramento de drift
    │   └── assets/            → métricas de modelo, configurações de pipeline ML
    ├── ai-engineer/           → eval reports, prompt design docs, fluxos de agente, RAG
    │   └── assets/            → suites de eval, exemplos de prompt, fluxos visuais
    ├── frontend-engineer/     → guias UI, design specs, /accessibility-review
    │   └── assets/            → mockups, design tokens, screenshots de a11y
    ├── infra-devops/          → /deploy-checklist, /incident-response, runbooks, IaC docs
    │   └── assets/            → diagramas de cloud, postmortems, configs IaC
    ├── qa/                    → /testing-strategy, planos de teste, relatórios de cobertura, bug reports
    │   └── assets/            → planilhas de cobertura, relatórios de execução
    └── security-auditor/      → /security-review, threat models, OWASP checks
        └── assets/            → relatórios de vulnerabilidade, threat models, evidências
```

**Anatomia da entrada:**
- Nome da pasta do agente
- `→` lista de commands que escrevem ali + tipos de artefato esperados
- `└── assets/` subpasta para arquivos de apoio (dados brutos, scripts geradores, imagens, datasets)

Regras:
- **Cada agente escreve apenas em sua própria pasta** (`docs/business/<agente>/` ou `docs/tech/<agente>/`).
- **Nenhum agente salva documento diretamente em `docs/` raiz** — sempre na pasta do agente.
- **Documentos** (.md, .pptx, .pdf, .docx) vão direto na pasta do agente.
- **Arquivos de apoio** (dados brutos, scripts geradores tipo `gen_pptx.js`/`gen_xlsx.py`, imagens, datasets) ficam em `<pasta-agente>/assets/`.
- Cada pasta de agente tem `.gitkeep` para versionar a estrutura mesmo vazia.

### Frontmatter YAML obrigatório

Todo `.md` em `docs/` começa com este header:

```yaml
---
title: <título do documento>
authors:
  - <agent-slug>
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

- `authors`: lista de slugs (`data-engineer`, `tech-lead`, ...). Quem cria entra primeiro. Quem revisa e ainda não está na lista, **anexa-se ao final**. Quem revisa algo que já assina, **não muda nada**. Ordem é cronológica de primeiro toque.
- `created`: data do primeiro write — **imutável**.
- `updated`: data do último write — atualizada a cada revisão.

---

## Versionamento de Documentos

Todo documento versionável (em `docs/`, em `products/<rotina>/`, ou qualquer outro local que use a convenção) segue a regra abaixo — nunca sobrescreva uma versão anterior, e o arquivo vigente sempre tem **nome estável**.

### Convenção de nome

```
<dir>/{nome}.md                                       ← VIGENTE (nome estável, sem data, sem versão)
<dir>/archive/{nome}_YYYY-MM-DD_v{N}.md               ← histórico (data do arquivamento + versão)
```

Exemplos:
- Vigente: `docs/business/project-manager/relatorio.md`, `products/<produto>/<arquivo>.md`
- Archive: `docs/business/project-manager/archive/relatorio_2026-04-28_v1.md`, `products/<produto>/archive/<arquivo>_2026-05-02_v1.md`

**Semântica da data no archive:** `YYYY-MM-DD` é a **data em que a versão foi arquivada** (saiu de vigência), obtida no momento do `git mv` via `date +%Y-%m-%d`. Não é a data em que a versão foi criada nem a data do último mtime do arquivo. Isso é determinístico e o agente não precisa ler o conteúdo do .md para decidir o nome.

**Por que nome estável no vigente:** quando o arquivo carrega data+versão no nome, todo referenciador precisa ser atualizado a cada revisão. Com nome estável, commands, agentes e scripts nunca quebram — só o conteúdo muda.

### Fluxo de revisão

Ao revisar um documento existente:
1. Capture a data de hoje: `TODAY=$(date +%Y-%m-%d)`
2. Determine `N` = (última versão em `<dir>/archive/{nome}_*_v*.md`) + 1, ou `1` se não há archive
3. `git mv <dir>/{nome}.md <dir>/archive/{nome}_${TODAY}_v${N}.md`
4. Recriar `<dir>/{nome}.md` com o conteúdo revisado
5. `git commit -m "docs: revisar {nome} (v{N} → v{N+1}, {motivo})"`

A pasta `archive/` é criada quando necessário e nunca é deletada — preserva o histórico completo.

**Atenção semântica:** o conteúdo do .md vigente pode ter um header tipo `**Versão:** 6.0 | **Data:** 2026-05-02` — essa data interna é "quando a versão entrou em vigência" e é diferente da data que vai no nome do archive (que é "quando saiu de vigência"). As duas datas convivem sem conflito.

### Geração de PDF/DOCX/PPTX

O hook `post_write.sh` dispara automaticamente `scripts/generate_docs.js` ao salvar qualquer `.md` em `docs/`. O gerador produz os arquivos em `docs/<subdir>/generated/` espelhando a estrutura de origem (incluindo `archive/`).

Para rodar manualmente:
```bash
node scripts/generate_docs.js docs/<subdir>/{nome}.md
```

---

## Equipe Multi-Agentes

Este projeto inclui 13 agentes em `.claude/agents/`. O ponto de entrada padrão é o `project-manager`.

| Agente | Responsabilidade |
|---|---|
| `project-manager` | Ponto de entrada — delega, consolida, nunca executa |
| `tech-lead` | Orquestrador técnico, code review, aprovação de PRs |
| `product-owner` | Kanban, backlog completo (negócio + produto + tech + marketing) |
| `data-engineer` | Pipelines, ETL, qualidade de dados |
| `data-scientist` | Análise exploratória, modelagem estatística/preditiva, insights para negócio |
| `ml-engineer` | Produtização de modelos validados: pipeline de treino, serving, monitoramento |
| `ai-engineer` | LLMs, agentes, RAG, evals |
| `infra-devops` | Cloud, CI/CD, containers |
| `qa` | Testes unitários, integração, e2e |
| `researcher` | Pesquisa técnica e de produto, benchmarks, inteligência competitiva |
| `security-auditor` | Segurança, vulnerabilidades |
| `frontend-engineer` | Web, UI, UX |
| `marketing-strategist` | Marketing, publicidade, mídias, go-to-market |

---

## Regras de Kanban

O kanban é a **fonte de verdade** do processo. Nenhum agente age sem consultar o kanban.

**Se precisar consultar issues e cards no Kanban** (project-number, owner, IDs de status), leia `.claude/memory/kanban_ids.md` — é a fonte de verdade dos IDs do projeto.

| Papel | Agente | Permissões |
|---|---|---|
| Dono | `product-owner` | cria, fecha, move qualquer card, árbitro final |
| Leitor obrigatório | `project-manager` | lê o kanban antes de toda delegação |
| Criador de issues | `project-manager`, `product-owner` | abrem issues novas — **sempre adicionam ao projeto Kanban imediatamente após criar** |
| Atualizador | todos os especialistas | move o próprio card para `In Progress` e `In Review` |
| Fechador | `product-owner` + `tech-lead` | movem para `Done` após aprovação |

### Dimensões obrigatórias do backlog

O `product-owner` garante que o backlog cobre **todas** as dimensões:

- **Discovery** — validação do problema, pesquisa, benchmarks
- **Negócio** — pitch deck, apresentações, identidade, naming
- **Produto** — MVP, personas, jornada do usuário, roadmap
- **Tech** — arquitetura, pipelines, testes, CI/CD
- **Lançamento** — divulgação, canais, métricas
- **Operações** — monitoramento, alertas, manutenção

### Labels obrigatórias no backlog

Ao criar o backlog (via `/kickoff` ou `/review-backlog`), o `product-owner` **sempre** cria e aplica labels em todas as issues:

**Labels de dimensão** (uma por issue):
| Label | Cor | Quando usar |
|---|---|---|
| `discovery` | `#0075ca` | Validações, pesquisas, entrevistas, benchmarks |
| `negocio` | `#e4e669` | Pitch, marca, financeiro, jurídico, CNPJ |
| `produto` | `#d93f0b` | Personas, jornada, PRD, wireframes, roadmap |
| `tech` | `#0e8a16` | Arquitetura, backend, frontend, infra, testes |
| `lancamento` | `#f9d0c4` | Go-to-market, canais, onboarding de parceiros |
| `operacoes` | `#bfd4f2` | Monitoramento, alertas, processos, runbooks |

**Labels de prioridade** (uma por issue):
| Label | Cor | Quando usar |
|---|---|---|
| `priority:high` | `#b60205` | Caminho crítico — bloqueia o próximo marco |
| `priority:medium` | `#fbca04` | Importante mas não bloqueia imediatamente |
| `priority:low` | `#c2e0c6` | Backlog futuro, nice-to-have |

**Regra:** criar as labels no repositório com `gh label create` antes de criar as issues. Aplicar sempre as duas labels (dimensão + prioridade) em cada issue no momento da criação.

---

## Regras de Branches

```
feature/* → dev → main
```

| Branch | Quem usa | Regra |
|---|---|---|
| `feature/*` ou `fix/*` | agentes especialistas | todo trabalho começa aqui |
| `dev` | integração contínua | recebe PRs de feature; nunca push direto |
| `main` | produção estável | recebe PRs de `dev`; só quando o usuário pedir explicitamente |

**Regras obrigatórias:**
- Nunca fazer push direto em `dev` ou `main` — sempre branch + PR
- Mudanças em `.claude/`, `CLAUDE.md`, `AGENTS.md` também seguem essa regra — nunca push direto
- `main` só recebe merge quando o usuário pedir explicitamente

## Convenção de Commits

Todos os commits seguem **Conventional Commits** com escopo obrigatório para diferenciar infraestrutura agentic de trabalho de produto:

| Escopo | Quando usar | Exemplos |
|---|---|---|
| `(system)` | Mudanças no sistema agentic: `.claude/`, `CLAUDE.md`, agentes, hooks, memória, scripts | `docs(system): atualizar project_history`, `chore(system): adicionar hook post_write` |
| sem escopo | Trabalho de produto: código, features, docs de produto, testes | `feat: implementar autenticação JWT`, `docs: add research report` |

**Regra:** mudanças de infraestrutura agentic nunca se misturam com commits de produto no mesmo commit.

## Memória Persistente

O projeto mantém memória persistente em `.claude/memory/` — criada pela Fase 0 do `/kickoff` e atualizada via `/update-memory`.

| Arquivo | Conteúdo | Quem lê |
|---|---|---|
| `MEMORY.md` | Índice com links para os outros arquivos | project-manager, tech-lead |
| `user_profile.md` | Trajetória, rede e preferências do fundador | project-manager, tech-lead |
| `project_genesis.md` | Motivação fundadora, ancoragens estratégicas, exclusões | project-manager, tech-lead |
| `project_history.md` | Changelog humano — decisões, entregáveis, restrições | project-manager, tech-lead |

**Regra:** somente o `project-manager` e o `tech-lead` leem a memória antes de agir. Os especialistas recebem contexto relevante via prompt de delegação — não lêem a memória diretamente.

**Regra de briefing:** ao montar o prompt de delegação para um especialista, o PM e o tech-lead verificam o MEMORY.md e incluem referências aos guidelines relevantes para a tarefa (se houverem). O especialista não descobre guidelines por conta própria — recebe no briefing.

## Autenticação GitHub

Dois mecanismos disponíveis — use o adequado para cada operação:

| Ferramenta | Como autentica | Quando usar |
|---|---|---|
| `gh` CLI | `GH_TOKEN` do `.env` | merge, delete-branch, PR, issues via terminal |
| MCP GitHub | token do `.mcp.json` (automático) | operações via ferramentas MCP do Claude |

**Antes de usar `gh`**, carregue o token:
```bash
export GH_TOKEN=$(grep GH_TOKEN .env | cut -d= -f2)
```

O MCP GitHub não precisa de configuração adicional — o token do `.mcp.json` é carregado automaticamente pelo Claude Code.

**Para merge com delete automático de branch**, sempre usar:
```bash
gh pr merge --merge --delete-branch
```

---

## Regras de Código e PR

| Etapa | Responsável |
|---|---|
| Escrever código | agente especialista da tarefa |
| Produzir documentação | `product-owner`, `researcher`, `marketing-strategist` |
| Abrir PR | agente que produziu o trabalho |
| Review de PRs de código | `tech-lead` — sempre |
| Review de PRs de docs (`docs/`) | `project-manager` — sempre |
| Security review | `security-auditor` — PRs com infra, auth ou dados sensíveis |
| QA review | `qa` — valida cobertura de testes |
| Aprovar PR de código | `tech-lead` |
| Aprovar PR de docs | `project-manager` |
| Merge | `tech-lead`; `infra-devops` em PRs de CI/CD quando delegado |
| Fechar issue | `product-owner` após merge |

Regra central: **nenhum agente faz merge do próprio trabalho sem aprovação do responsável** (`tech-lead` para código, `project-manager` para docs).

### Cleanup obrigatório após merge

**Merge de feature → dev** (agente especialista, após merge aprovado):
```bash
git checkout dev && git pull && git branch -D <nome-do-branch> 2>/dev/null || true
```

**Merge de dev → main** (quando o usuário pedir promoção para main):
```bash
git checkout main && git pull origin main && git checkout dev && git merge main --no-edit && git push origin dev
```

Nunca rodar `git pull origin main` estando em outro branch — isso mistura históricos. Sempre fazer checkout do branch antes de puxar. O `git merge main` final é obrigatório para trazer o commit de merge para o dev e evitar o banner de divergência no Claude Code.

**Esta etapa é obrigatória em todos os commands que geram branch e merge** — `/fix-issue`, `/advance`, `/deploy`, qualquer outro. Não é opcional. Sem este passo, o Claude Code exibe o banner de branch stale e o workspace fica sujo.

---

## Sessões Cloud — Rastreabilidade

Ao abrir PR ou commitar entregável em sessão cloud, incluir no corpo do PR o link da sessão:

```bash
[ -n "$CLAUDE_CODE_REMOTE_SESSION_ID" ] && echo "Sessão: https://claude.ai/code/${CLAUDE_CODE_REMOTE_SESSION_ID}"
```

Se `CLAUDE_CODE_REMOTE_SESSION_ID` não existir (sessão local), omitir — sem erro, sem placeholder.

---

## Contexto em Sessões Cloud

Em sessões cloud, os comandos de contexto se comportam diferente:

- `/compact` → disponível — resume a conversa e libera contexto; aceita instruções de foco (ex: `/compact manter output dos testes`)
- `/clear` (comando interno do Claude) → **não disponível** em cloud — usar `/compact` no lugar
- `/clean` (command do projeto) → funciona normalmente em qualquer ambiente

---

## Commands Disponíveis

| Command | Quando usar |
|---|---|
| `/kickoff` | Iniciar um projeto novo — discovery, pesquisa, relatório, apresentação, backlog, delegação |
| `/advance` | Avançar no Kanban — fecha prontos, valida com PO, paraleliza issues independentes, delega |
| `/review-backlog` | Varredura proativa — fecha prontos, identifica lacunas, refina e cria novas issues |
| `/review` | Acionar TL para code review de um PR específico |
| `/deploy` | Acionar infra-devops para deploy |
| `/fix-issue` | Acionar especialista para corrigir um bug ou problema reportado |
| `/clean` | Commitar e fazer push de tudo que está pendente localmente, de forma segura |
| `/update-memory` | Atualizar memória do projeto — registrar decisões, restrições e entregáveis aprovados (incremental) |
| `/update-memory-full` | Reconstruir memória completa — usar quando o histórico está vazio ou muito defasado |

---

## Skills Disponíveis

Skills em `.agents/skills/` — referenciadas formalmente nos agentes.

**Skills de domínio enterprise:**
- `product-management` — backlog, priorização, critérios de aceitação
- `code-review` — revisão de PRs com severidade 🔴🟡🔵
- `data-engineering` — pipelines, ETL, qualidade de dados
- `data-science` — análise exploratória, estatística, modelagem, insights
- `ml-engineering` — produtização de modelos, serving, monitoramento de drift
- `ai-engineering` — LLMs, RAG, agentes, evals
- `frontend-engineering` — UI/UX, acessibilidade, responsividade
- `security-audit` — OWASP, vulnerabilidades, secrets
- `qa-testing` — pirâmide de testes, cobertura, boas práticas
- `market-research` — mercado, competidores, benchmarks
- `go-to-market` — GTM, posicionamento, funil
- `infra-devops` — IaC, CI/CD, deploy, observabilidade

**Skills Caveman (opcionais — instaladas pelo `/wizard`):**
- `caveman` — comunicação ultra-comprimida (~75% menos tokens)
- `caveman-commit` — mensagens de commit comprimidas
- `caveman-review` — code review em uma linha por finding
