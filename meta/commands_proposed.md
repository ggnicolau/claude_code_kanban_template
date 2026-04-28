# Commands Propostos e Implementados

Commands customizados do template ("Nosso") e commands propostos ainda não implementados ("Proposto").

| Área | Command | Status | Agente responsável | Documento gerado | Explicação |
|---|---|---|---|---|---|
| UX / Research | /research | Proposto | researcher | docs/research/[tema].md | Aciona o researcher para investigar um tema com profundidade e salvar o resultado |
| Produto | /roadmap | Proposto (nativo: /roadmap-update) | product-owner / orchestrator | docs/roadmap.md + .pptx | Wrapper do nativo com agente responsável e documento salvo |
| Produto | /metrics | Proposto (nativo: /metrics-review) | product-owner / orchestrator | docs/metrics.md | Wrapper do nativo com agente responsável e documento salvo |
| Produto | /personas | Proposto | product-owner / orchestrator | docs/personas.md | Define ou refina personas com dores, comportamentos e critérios de sucesso |
| Produto | /prd | Proposto | product-owner / orchestrator | docs/prd.md + .pdf | Product Requirements Document completo a partir de um problema ou feature |
| Produto | /user-journey | Proposto | product-owner / orchestrator | docs/user-journey.md | Mapeia jornada por persona com touchpoints, emoções e pontos de atrito |
| Negócio | /competitive-analysis | Proposto (nativo: /competitive-brief) | researcher | docs/competitive-analysis.md + .pptx | Wrapper do nativo com agente responsável e documento salvo |
| Negócio | /stakeholder-update | Proposto (nativo existe, sem doc) | coordinator → orchestrator | docs/updates/[data].md + .pdf | Wrapper do nativo que salva o update como documento versionado por data |
| Negócio | /pitch | Proposto | researcher + orchestrator | docs/pitch.md + .pptx | Gera ou atualiza pitch deck executivo com narrativa estruturada |
| Processo | /kickoff | Nosso | coordinator | docs/kickoff/kickoff.md | Inicia o projeto: discovery, memória, backlog completo, aprovação |
| Processo | /advance | Nosso | coordinator | — | Avança no Kanban: fecha prontos, apresenta plano, paraleliza, delega |
| Processo | /review-backlog | Nosso | coordinator → orchestrator | — | Varredura proativa do backlog: fecha prontos, identifica lacunas, refina |
| Processo | /review | Nosso | orchestrator | comentários no PR / docs/review/ | Code review ou revisão de entregável com severidade |
| Processo | /fix-issue | Nosso | orchestrator → especialista | PR | Corrige um bug ou problema reportado seguindo o processo completo |
| Processo | /clean | Nosso | coordinator | — | Commita e faz push de tudo que está pendente localmente |
| Processo | /update-memory | Nosso | coordinator → orchestrator | .claude/memory/project_history.md | Atualiza a memória do projeto — registra o que aconteceu, decisões e restrições |
| Processo | /deploy | Nosso | infra-devops | — | Aciona infra-devops para executar o deploy |
| Processo | /onboarding | Proposto | orchestrator + coordinator | docs/onboarding.md + .pdf | Gera guia completo de onboarding para novos membros do projeto |
| Template | /wizard | Nosso (só no template pai) | template-coordinator | novo repositório filho | Cria novo repositório filho a partir do template com Kanban configurado |
| Template | /sync-to-projects | Nosso (só no template pai) | template-coordinator | — | Propaga mudanças do template para projetos filhos existentes |
| Template | /sync-to-template | Nosso (só no template pai) | template-coordinator | — | Traz melhorias de um projeto filho de volta ao template |
| Template | /sync-master | Nosso (só no template pai) | template-coordinator | — | Sincroniza camada universal entre os 3 templates irmãos |
