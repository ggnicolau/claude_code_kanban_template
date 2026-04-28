# Commands Nativos do Claude Code

Commands disponíveis out-of-the-box no Claude Code, sem necessidade de implementação.

| Área | Command | Explicação | Casos de uso |
|---|---|---|---|
| Design | /accessibility-review | Audita interfaces para acessibilidade (WCAG, contraste, navegação por teclado) | Revisar UI antes de lançar, checar conformidade com WCAG 2.1 |
| Design | /design-critique | Crítica estruturada de um design: pontos fortes, problemas, sugestões | Feedback em wireframes, mockups, protótipos |
| Design | /design-handoff | Gera especificações técnicas de design para o dev implementar | Passagem de design para engenharia |
| Design | /design-system | Cria ou audita um design system: componentes, tokens, padrões | Criar biblioteca de componentes, padronizar UI |
| UX / Research | /user-research | Planeja ou sintetiza pesquisa com usuários: roteiros, personas, insights | Entrevistas, testes de usabilidade, surveys |
| UX / Research | /research-synthesis | Sintetiza dados qualitativos em padrões e insights acionáveis | Após entrevistas ou testes, antes de decisões de produto |
| UX / Research | /synthesize-research | Consolida múltiplas fontes de pesquisa | Desk research, benchmarks, dados mistos |
| UX / Research | /insights | Extrai insights de dados, métricas ou feedback | Análise de engajamento, churn, NPS |
| UX / Research | /ux-copy | Escreve e refina microcopy, textos de UI e comunicação com usuário | Botões, mensagens de erro, onboarding, tooltips |
| Produto | /product-brainstorming | Sessão estruturada de ideação de produto | Explorar novas features, resolver problemas de UX, pivotar |
| Produto | /product-management:brainstorm | Foco em gestão de produto: priorização, trade-offs, métricas | Decisões de roadmap, definição de MVP |
| Produto | /sprint-planning | Planeja sprint: seleciona issues, estima, distribui carga | Início de ciclo de desenvolvimento |
| Produto | /standup | Gera update diário de progresso | Daily sync, relatório de status |
| Produto / Eng | /write-spec | Escreve especificações técnicas ou de produto | Antes de implementar uma feature |
| Dados / Análise | /analyze | Análise genérica de código, dados, logs ou texto | Investigar bug, entender dataset |
| Dados / Análise | /explore-data | Exploração inicial de dataset: estrutura, distribuição, qualidade | EDA antes de modelar ou visualizar |
| Dados / Análise | /create-viz | Cria visualizações de dados | Relatórios, posts com dados, apresentações |
| Dados / Análise | /xlsx | Gera e edita planilhas Excel com formatação e fórmulas | Relatórios financeiros, tabelas de dados, frameworks |
| Dados / Análise | /validate-data | Valida qualidade e consistência de datasets | Antes de usar dados em análise ou modelo |
| Dados / Análise | /write-query | Escreve queries SQL ou equivalentes a partir de linguagem natural | Extração de dados, análise exploratória |
| Infra / Eng | /system-design | Projeta arquitetura de sistema: componentes, fluxos, trade-offs | Antes de implementar feature complexa |
| Infra / Eng | /architecture | Documenta ou revisa decisões arquiteturais (ADRs) | Onboarding, revisão técnica |
| Infra / Eng | /tech-debt | Mapeia e prioriza débito técnico | Sprint de qualidade, pós-MVP |
| Infra / Eng | /testing-strategy | Define estratégia de testes | Início de projeto, antes de lançar |
| Infra / Eng | /security-review | Audita código ou infra por vulnerabilidades | PRs com auth, secrets, dados sensíveis |
| Infra / Eng | /deploy-checklist | Checklist de deploy | Antes de qualquer deploy em produção |
| Infra / Eng | /incident-response | Guia resposta a incidentes | Pipeline quebrado, dados errados publicados |
| Processo | /skill-creator | Cria novos skills customizados para o projeto | Automatizar comportamentos recorrentes |
| Processo | /ultrareview | Code review aprofundado com análise de segurança, performance e design | PRs críticos, revisão pré-release |
| Processo | /schedule | Agenda tarefas recorrentes ou com delay | Automações periódicas, lembretes |
| Processo | /rewind | Reverte o contexto da sessão para um ponto anterior | Desfazer ações indesejadas na sessão |
| Processo | /wizard | Setup guiado de um novo projeto a partir do template | Inicializar repositório novo com o template |
| Sistema | /btw | Adiciona contexto lateral sem interromper o fluxo principal | Notas rápidas, avisos ao Claude sem mudar tarefa |
| Sistema | /mcp | Gerencia MCP servers conectados ao Claude Code | Listar, adicionar ou remover MCPs |
| Sistema | /model | Troca o modelo Claude em uso na sessão | Usar Opus para tarefas complexas, Haiku para rápidas |
| Sistema | /clear | Limpa o contexto da conversa atual | Reiniciar sessão sem fechar o terminal |
| Sistema | /export | Exporta o conteúdo da sessão atual | Salvar conversa, compartilhar resultado |
