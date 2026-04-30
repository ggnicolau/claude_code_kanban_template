# Discovery — /kickoff

O kickoff é o ponto de partida de qualquer projeto. Ele conduz o discovery completo e monta o backlog antes de qualquer execução.

---

## Quando usar

- Ao iniciar um projeto novo (logo após o `/wizard`)
- Ao retomar um projeto que perdeu direção
- Ao pivotar e redefinir o escopo

---

## Fases do kickoff

```mermaid
sequenceDiagram
    participant User as Fundador
    participant PM as project-manager
    participant RES as researcher
    participant PO as product-owner
    participant TL as tech-lead

    User->>PM: /kickoff

    Note over PM: Fase 0a — IDs do Kanban
    PM->>PM: Descobre project-id, field-id e option-ids via GraphQL
    PM->>PM: Salva kanban_ids.md + injeta no product-owner.md

    Note over PM: Fase 0b — Perguntas narrativas
    PM->>User: Contexto do fundador, problema, ancoragens
    User->>PM: Respostas

    Note over PM: Fase 0c — Síntese + confirmação
    PM->>User: Síntese consolidada
    User->>PM: Aprovação

    Note over PM: Fase 0d — Persistência de memória
    PM->>PM: Cria .claude/memory/ (4 arquivos)

    Note over PM,RES: Fase 1 — Discovery
    PM->>RES: Task: pesquisa de mercado e técnica
    RES->>PM: Relatório de inteligência

    Note over PM: Fase 2 — Relatório
    PM->>PM: Consolida relatório + apresentação
    PM->>User: Relatório em docs/business/

    Note over PO: Fase 3 — Backlog
    PM->>PO: Task: criar backlog completo
    PO->>PO: Cria issues em 6 dimensões no Kanban
    PO->>PM: Backlog pronto

    Note over PM: Fase 4 — Aprovação
    PM->>User: Apresenta backlog
    User->>PM: Aprovação

    Note over TL: Fase 5 — Delegação
    PM->>TL: Task: delegação inicial
    TL->>TL: Seleciona primeiras issues
```

---

## Fase 0 — Setup e memória persistente

A Fase 0 é a mais importante. Ela configura a infraestrutura do projeto e cria a **memória** que persiste entre todas as sessões futuras.

### 0a — IDs do Kanban

Antes de qualquer conversa, o PM descobre os IDs do GitHub Project via GraphQL e os injeta no `product-owner.md`, habilitando o PO a mover cards sem configuração manual. Salva também em `.claude/memory/kanban_ids.md`.

### 0b — Perguntas narrativas

O PM faz perguntas abertas ao fundador:

1. Quem você é? (background, motivação, estilo de trabalho)
2. Qual problema este projeto resolve?
3. Para quem resolve? (ICP)
4. O que este projeto definitivamente **não** é?
5. Quais são suas ancoragens não-negociáveis?

### 0c — Síntese e confirmação

O PM consolida as respostas em uma síntese e pede confirmação antes de persistir.

### 0d — Persistência

Cria `.claude/memory/` com 4 arquivos:

```
.claude/memory/
├── MEMORY.md          # índice
├── kanban_ids.md      # IDs do GitHub Project (project-id, field-id, option-ids)
├── user_profile.md    # quem é o fundador
├── project_genesis.md # gênese e ancoragens
└── project_history.md # histórico (vazio no início)
```

---

## Backlog em 6 dimensões

O product-owner cria issues cobrindo todas as dimensões do projeto:

| Dimensão | Exemplos de épicos |
|---|---|
| **Discovery** | Validação de problema, entrevistas com usuários |
| **Negócio** | Modelo de receita, pitch, parcerias |
| **Produto** | MVP, UX, roadmap de features |
| **Tech** | Arquitetura, stack, pipelines de dados |
| **Lançamento** | GTM, comunicação, canais |
| **Operações** | Monitoramento, suporte, processos internos |

---

## Resultado do kickoff

Ao final do kickoff:

- IDs do Kanban injetados no `product-owner.md` e salvos em `.claude/memory/kanban_ids.md`
- Memória persistente criada em `.claude/memory/` (user_profile, project_genesis, project_history)
- Relatório de discovery em `docs/business/relatorio_YYYY-MM-DD_v1.md`
- Backlog completo no GitHub Projects (issues em todas as 6 dimensões)
- Branch `dev` criado e configurado
- Primeiras issues delegadas ao TL para execução
