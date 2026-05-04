# [EPIC] Encapsular Dual Multi-Agent System como produto web B2B com UI controlada, runtime privado e GitHub do cliente como source of truth

## Índice

1. [Contexto e tese de produto](#contexto)
2. [Diferenciação e hipótese de mercado](#diferenciação-e-hipótese-de-mercado)
3. [Template atual e capacidades existentes](#o-que-o-template-atual-já-entrega)
4. [Objetivo e arquitetura alvo](#objetivo)
5. [Separação system/platform/project](#separação-de-domínios)
6. [Dual-plane: construção e execução](#dual-plane-support-construção-e-execução)
7. [UI, executor e ferramentas avaliadas](#avaliação-de-opções-reais-de-ui-e-executor)
8. [API, fluxos, isolamento e GitHub](#backendapi-própria)
9. [Infraestrutura beta](#infraestrutura-beta)
10. [Modelo comercial e posicionamento](#modelo-comercial-beta)
11. [Cronograma, riscos e critérios de aceite](#estimativa-de-prazo)
12. [Resultado esperado](#resultado-esperado)

---

## Contexto

O Dual Multi-Agent System atualmente roda via Claude Code.

Ele nasceu como uma arquitetura operacional codificada em arquivos `.md`, acumulando experiência prática de engenharia, gestão de projetos, produto, coordenação, governança, TI e IA.

O valor do sistema não está apenas nos arquivos em si, mas na metodologia operacional que eles codificam: papéis claros, cadeia de comando, Kanban como memória operacional, gates de aprovação, rastreabilidade por issues, PRs e commits, separação entre construção e execução, agentes especializados, commands, hooks, skills, memória persistente, feedback loop execução -> construção e adaptação por domínio/cliente.

O Claude Code funciona bem como ambiente de desenvolvimento porque permite carregar `CLAUDE.md`, `AGENTS.md` e agents especializados; executar hooks como `session_start`; usar commands; consultar memória persistente; operar sobre GitHub/Kanban; executar pipelines de construção e execução; conversar livremente com o usuário; e acionar subagentes e tools.

Porém, esse modelo não é adequado para distribuição comercial. A UI do Claude Code é fechada, não permite adaptação suficiente, não permite remover painéis ou restringir superfícies e não permite criar uma experiência controlada para cliente. Além disso, o runtime pressupõe acesso completo ao workspace: o usuário pode ver arquivos internos, copiar arquivos de sistema, modificar regras do sistema e operar sem uma fronteira clara entre operador e cliente.

Por fim, o produto não deve ser entregue como executável, template ou repositório. O valor está na arquitetura, nos agentes, nas regras, nos workflows e na governança. A forma correta de distribuição é um serviço web/SaaS controlado, em que o cliente não recebe os `.mds` privados nem o sistema base.

Objetivo desta epic:

> Transformar o sistema atual, operado localmente via Claude Code, em um produto web beta B2B com runtime privado, interface controlada, metodologia agentic proprietária encapsulada e operação sobre o GitHub do cliente.

---

## Tese de produto

O produto não é apenas um template. Ele é uma fábrica/sistema operacional multi-agente para criar, evoluir e operar produtos digitais com governança, memória, Kanban, gates e rastreabilidade.

Em termos de mercado, o produto deve ser entendido como uma plataforma gerenciada que productiza a função de uma consultoria/COE de produto, engenharia e gestão, operando diretamente no GitHub do cliente.

Não é apenas uma ferramenta de chat, nem apenas uma UI para Claude Code/Codex, nem apenas um framework de agentes. O ativo central é a metodologia operacional codificada nos `.mds`, agents, commands, hooks, gates, policies, templates e workflows. O cliente não compra horas, não recebe um template e não instala o sistema: compra acesso contínuo a uma capacidade operacional para criar, organizar, construir, revisar, operar, auditar e evoluir produtos digitais com um sistema de agentes governado.

### Categoria comercial

A categoria mais precisa para o beta é:

> Service-as-a-Product entregue como Product-as-a-Service / plataforma gerenciada.

`Service-as-a-Product` significa que uma função normalmente consultiva, artesanal e dependente de especialistas foi transformada em uma oferta padronizada, repetível e vendável como produto.

No caso do Dual Multi-Agent System, a função productizada é parecida com a de uma consultoria, COE interno ou time autossuficiente de produto/engenharia: entender contexto, estruturar discovery, criar projeto e backlog, organizar Kanban, priorizar, executar desenvolvimento, gerar issues, PRs e commits, aplicar gates, operar rotinas, registrar decisões e transformar falhas em trabalho rastreável.

`Product-as-a-Service` significa que o cliente acessa a capacidade do produto como serviço contínuo, sem possuir o sistema, sem receber os `.mds` privados, sem acessar o runtime e sem controlar a infraestrutura.

O termo `SaaS` pode ser usado como forma de entrega, desde que com precisão: o beta não é um SaaS self-service genérico, mas uma plataforma gerenciada/hosted managed platform, com onboarding, configuração, ponto focal treinado do cliente, login/permissões e sistema hospedado, privado e operado pela infraestrutura própria.

!!! note
    A categoria de negócio é Service-as-a-Product. A forma de entrega é plataforma gerenciada. A função automatizada é parecida com consultoria/COE, mas o ativo vendido não é hora: é capacidade operacional contínua.

Formulação curta:

> Não vendemos horas. Não entregamos template. Não entregamos repo. Vendemos uma capacidade operacional contínua: delivery de produto com método, agentes, governança e rastreabilidade.

Ele pode atender dois tipos de produto digital.

### 1. Produtos digitais tradicionais

Produtos em que os agentes ajudam a construir, mas não são necessariamente o produto final:

- websites;
- SaaS;
- dashboards;
- apps internos;
- APIs;
- pipelines de dados;
- pipelines de ML;
- automações;
- integrações;
- sistemas internos;
- ferramentas digitais B2B.

### 2. Produtos agentic-native

Produtos em que os próprios agentes são parte essencial da operação:

- pipelines editoriais;
- sistemas de pesquisa recorrente;
- agentes analíticos;
- operações de inteligência;
- pipelines que geram outputs;
- workflows que se auto-monitoram;
- produtos que transformam falhas em backlog;
- sistemas operados continuamente por agentes.

PDFs, PPTX, relatórios e posts são apenas exemplos de artefatos possíveis do plano de execução. O sistema deve ser capaz de produzir qualquer artefato digital compatível com o produto do cliente.

---

## Diferenciação e hipótese de mercado

O produto não compete diretamente com ferramentas individuais de desenvolvimento assistido por IA, nem com frameworks de agentes genéricos.

O padrão observado no mercado é:

1. Desenvolvedores usam Claude Code, Cursor, Copilot e ferramentas similares para resolver tarefas técnicas em formato livre.
2. Usuários de negócio usam chats e agentes para resolver demandas pontuais, normalmente sem processo estruturado.
3. Frameworks como CrewAI, LangGraph, AutoGen, Dify, Flowise e Langflow oferecem blocos para construir sistemas agentic, mas exigem muito esforço de engenharia para entregar workflows completos, governados e auditáveis.
4. Runtimes agentic oferecem infraestrutura, mas não entregam uma metodologia de produto, gestão, Kanban, gates, papéis, commands e operação ponta a ponta pronta para adaptar a clientes.

O diferencial do Dual Multi-Agent System é tratar agentes não como assistentes soltos, mas como uma organização operacional codificada. A arquitetura combina papéis claros, cadeia de comando, PM, PO, TL, QA e especialistas; usa o Kanban como fonte de verdade, issues como memória e canal entre agentes, PRs e commits como trilha técnica; preserva gates de aprovação, feedback loop execução -> construção, adaptação por domínio/cliente, operação sobre o GitHub do cliente e isolamento da metodologia privada.

O risco competitivo existe: outras empresas ou desenvolvedores podem construir partes semelhantes. Porém, a maioria dos usos atuais de IA permanece em dois extremos:

- uso individual, livre e pouco governado;
- frameworks técnicos que exigem montar toda a governança do zero.

Além disso, a alternativa real em muitas empresas não é apenas "comprar uma ferramenta de IA". Frequentemente a decisão está entre contratar uma consultoria tradicional, montar um COE interno, formar um time de produto/engenharia dedicado, entregar Claude Code/Codex solto para profissionais internos ou contratar automações pontuais sem governança de delivery.

O beta deve se posicionar entre esses mundos:

```text
consultoria/COE
  +
produto hospedado
  +
agentes de IA governados
  +
GitHub como trilha operacional
```

A experiência esperada não é de um usuário avulso conversando com um chatbot genérico. A experiência esperada é de um ponto focal treinado do cliente interagindo com uma unidade de entrega digital governada, como faria com uma consultoria ou COE, mas com parte relevante da operação encapsulada em software.

Este produto ocupa uma camada diferente:

> um sistema operacional agentic governado para construir, operar e evoluir produtos digitais.

O defensivo inicial não é o segredo absoluto dos arquivos `.md`, mas a combinação entre velocidade de execução, metodologia acumulada, qualidade da adaptação por cliente, biblioteca crescente de agents/commands/templates, casos reais, histórico operacional, SaaS privado com isolamento e evolução contínua do sistema base.

A estratégia do beta deve priorizar validação em clientes reais para transformar a vantagem metodológica em prova de mercado.

---

## O que o template atual já entrega

O template pai `claude-code-enterprise-template` é uma fábrica de projetos.

Ele cria projetos filhos com:

- agentes especializados para coordenação, produto, engenharia, dados, IA, infraestrutura, QA, segurança, pesquisa e go-to-market;
- `CLAUDE.md` e `AGENTS.md` gerados para o projeto filho;
- commands como `/kickoff`, `/advance`, `/review-backlog`, `/review`, `/deploy`, `/fix-issue`, `/clean`, `/update-memory`;
- GitHub Project/Kanban criado por workflow;
- labels, issues iniciais, CI/CD e convenções de branch/commit;
- memória persistente em `.claude/memory/`;
- hooks como `session_start.sh` e `post_write.sh`;
- geração de PDF/DOCX/PPTX a partir de documentos markdown;
- skills enterprise para produto, engenharia, dados, IA, QA, segurança, pesquisa e go-to-market.

O projeto filho começa com `/kickoff`.

O `/kickoff`:

- conduz uma Fase 0 narrativa sobre fundador, contexto, origem, rede, ancoragens e exclusões;
- grava memória persistente;
- conduz discovery;
- aciona pesquisa;
- gera relatório;
- gera backlog;
- obtém aprovação antes de execução.

O `/advance`:

- lê o GitHub Project;
- fecha itens prontos com PO;
- resolve bloqueios;
- valida próximas issues;
- paraleliza quando possível;
- delega via TL;
- reporta estado do Kanban.

O centro de gravidade do sistema não é uma UI local. O centro de gravidade é:

```text
CLAUDE.md / AGENTS.md / agents / commands / memory / hooks / skills
  +
GitHub Projects / issues / PRs / commits
  +
dual-plane construção/execução
```

Qualquer UI escolhida para o beta deve preservar isso.

---

## Objetivo

Criar uma versão beta comercial do Dual Multi-Agent System baseada em:

- runtime/orquestrador privado, inicialmente baseado no executor que já funciona melhor para o sistema atual;
- Claude Code como executor inicial preferencial, se mantiver maior qualidade e menor risco;
- Codex como executor alternativo/pluggable;
- Aider como executor alternativo especializado para edição de código, se fizer sentido;
- runtime alternativo futuro apenas se trouxer ganho real sobre o executor atual;
- UI web controlada, adaptada a partir de base open-source ou construída como superfície enxuta;
- Monitor/Dashboard reaproveitado parcialmente para observabilidade;
- API própria como camada intermediária obrigatória;
- GitHub do cliente como fonte de verdade operacional;
- arquivos `.md` de sistema isolados e privados;
- execução via LLM API ou CLI/SDK privado permitido pelos termos aplicáveis;
- infraestrutura própria em VM única para o beta;
- adaptação da arquitetura multi-agente dual ao contexto de cada cliente.

---

## Arquitetura alvo

```text
Cliente
  ↓
UI Web controlada
  ↓
API própria
  ↓
job runner privado
  ↓
executor agentic interno
  ↓
system/ privado + platform/ privada + project/ do cliente
  ↓
GitHub do cliente
```

A UI expõe apenas a superfície permitida: chat/comandos, status/eventos públicos, diff/PR/preview do `project/`, board espelhado do GitHub Projects e componentes parciais de monitor.

A API própria concentra os endpoints públicos do beta: `/chat`, `/command`, `/status`, `/events`, `/metrics`, `/history`, `/project/changes` e `/project/artifacts`.

O executor agentic interno deve começar pelo caminho que já funciona melhor, hoje Claude Code, mantendo Codex/Aider como alternativas ou complementos. O desenho deve evitar dependência irreversível de qualquer executor específico.

O GitHub do cliente concentra issues, PRs, commits, Kanban, código, documentação e artefatos.

!!! note
    Arquitetura alvo descreve camadas. A seção de encapsulamento do executor, mais adiante, descreve a transição do estado atual para esse estado alvo. Elas se complementam: uma mostra a forma final; a outra mostra como sair do uso local sem perder comportamento.

---

## Princípio arquitetural central

O cliente não recebe o sistema.

O cliente recebe acesso a:

> uma interface web que aciona um sistema de agentes hospedado e controlado pela infraestrutura própria.

A inteligência permanece privada.

O GitHub do cliente permanece como superfície operacional visível do projeto/produto.

---

## Separação de domínios

### 1. Sistema privado

O sistema privado contém a lógica do Dual Multi-Agent System.

Conteúdo:

```text
system/
  CLAUDE.md ou SOUL.md
  AGENTS.md
  agents/*.md
  memory/*.md
  hooks/
  commands/
  skills/
  settings.json
  templates/
  policies/
  sanitizer/
```

Regras:

- não pode ser acessado pelo cliente;
- não pode ser listado pela UI;
- não pode ser exposto por API;
- não pode ser commitado no GitHub do cliente;
- não pode ser acessado por tools genéricas;
- não pode aparecer em logs visíveis;
- não pode ser mencionado em respostas externas;
- não pode ser exposto por WebSocket, Gateway, file explorer ou endpoint.

### 2. Plataforma privada

A plataforma é a aplicação SaaS em si.

Conteúdo:

```text
platform/
  frontend/
  backend/
  runner/
  adapters/
  sanitizer/
  auth/
  deploy/
  observability/
```

Regras:

- cliente não acessa o código da plataforma;
- agente conversando com o cliente não pode ler nem modificar `platform/`;
- UI não pode expor rotas internas da plataforma;
- mudanças em plataforma ocorrem por deploy/control plane do operador.

### 3. Projeto/produto do cliente

O GitHub do cliente é a superfície operacional visível.

Conteúdo:

```text
GitHub do cliente/
  issues
  PRs
  commits
  Kanban
  código do projeto
  documentação do produto
  artefatos produzidos
  logs sanitizados
  comentários operacionais
```

Funções:

- memória operacional do projeto;
- canal de comunicação entre agentes e cliente;
- rastreabilidade;
- backlog;
- histórico de entregas;
- registro de falhas;
- fonte de verdade visível.

### 4. Configuração vertical/domínio do cliente

Além do sistema base, pode existir camada de domínio:

```text
domain/
  vocabulário especializado
  agents de domínio
  workflows específicos
  templates de output
  critérios de qualidade
```

Essa camada deve permanecer privada quando fizer parte da propriedade intelectual do sistema.

---

## Decisão sobre Kanban

Não haverá Kanban interno do sistema na versão beta.

O Kanban relevante é o Kanban do projeto/produto do cliente.

O sistema deve:

- ler o Kanban do cliente;
- interpretar estado;
- criar issues;
- comentar issues;
- abrir PRs;
- mover cards;
- registrar entregas;
- registrar falhas sanitizadas;
- conectar execução e construção.

O sistema não deve expor:

- lógica interna;
- regras dos agentes;
- raciocínio completo;
- nomes ou estrutura dos arquivos de sistema;
- paths internos;
- prompts;
- memória raw.

Se uma UI como Vibe Kanban ou Nimbalyst trouxer board próprio, esse board não deve virar fonte de verdade. Ele deve ser:

```text
GitHub Projects/issues
  ↓
API própria
  ↓
UI board espelhado/cache
```

Regra:

> GitHub vence. UI espelha, aciona e exibe.

---

## Dual-plane support: construção e execução

O produto beta deve preservar a arquitetura dual original.

### 1. Plano de construção

Responsável por desenvolvimento e evolução do produto.

Inclui:

- discovery;
- criação e refinamento de issues;
- priorização de backlog;
- abertura de branches;
- escrita de código;
- abertura de PRs;
- code review;
- testes;
- QA;
- correção de bugs;
- deploy;
- documentação;
- evolução do produto.

Comandos esperados:

```text
/kickoff
/advance
/fix-issue
/review
/review-backlog
/deploy
/clean
/update-memory
/sync-template
```

### 2. Plano de execução

Responsável por operar o produto.

Inclui:

- rotinas agendadas;
- execução de pipelines;
- coleta de dados;
- transformação de dados;
- análise;
- geração de artefatos;
- publicação;
- monitoramento;
- registro de falhas;
- geração de issues a partir de falhas.

Comandos esperados:

```text
/run-editorial-diaria
/run-report
/run-pipeline
/publish
/retry-failed-run
```

Os nomes acima são exemplos. O produto deve permitir commands específicos por cliente/domínio.

---

## Feedback loop: execução -> construção

Quando uma rotina do plano de execução falhar, o sistema deve transformar a falha em item rastreável do plano de construção.

Fluxo esperado:

```text
Pipeline falha
  ↓
Sistema captura estágio da falha
  ↓
Sistema sanitiza erro
  ↓
Sistema cria issue no GitHub do cliente
  ↓
Issue recebe contexto reproduzível
  ↓
Issue recebe critério de aceite
  ↓
/advance pode tratar a issue posteriormente
```

Exemplo:

```text
Título:
Corrigir falha na geração de PPTX do pipeline editorial

Contexto:
A falha ocorreu após a análise estatística e antes da renderização final do artefato.

Critério de aceite:
- pipeline deve gerar PPTX válido;
- artefato final deve ser salvo;
- execução deve registrar status concluído;
- falha não deve se repetir nos dados de teste.
```

---

## Gates de aprovação

O sistema deve preservar gates antes de entregas relevantes.

### Gates mínimos

1. Gate técnico
   - valida execução;
   - valida testes;
   - valida consistência com issue;
   - valida ausência de erro crítico.

2. Gate de produto/editorial
   - valida aderência ao objetivo;
   - valida clareza do output;
   - valida adequação ao público;
   - valida consistência narrativa.

3. Gate visual/artefato
   - valida PPTX;
   - valida PDF;
   - valida gráficos;
   - valida layout;
   - valida publicação final.

4. Gate de QA
   - valida regressão;
   - valida critérios de aceite;
   - valida comportamento esperado;
   - valida fluxo ponta a ponta.

No beta, os gates podem ser automáticos ou semi-automáticos, mas devem gerar registro resumido no GitHub do cliente ou no Monitor.

---

## Avaliação de opções reais de UI e executor

A UI escolhida deve respeitar os invariantes do template:

- o GitHub Project do cliente é o source of truth;
- `/kickoff` e `/advance` são fluxos centrais;
- o cliente vê `project/`, nunca `system/`;
- o cliente precisa ver diff, PR, status, artefatos e eventos;
- a UI não pode expor agentes internos, memory raw, settings, MCP amplo, file explorer amplo ou shell irrestrito;
- qualquer execução precisa passar pela API própria, policy e sanitizer.

### Observação sobre Claude Code/Codex

Claude Code Desktop e Codex Desktop são interfaces fechadas. Elas não podem ser "capadas" diretamente para virar UI do cliente.

O que pode ser usado no beta é:

- Claude Code/Codex como executor interno, via CLI/SDK/processo privado, se isso for permitido pelos termos de uso aplicáveis;
- uma UI open-source ou própria por cima, sempre chamando a API própria;
- um job runner que trate Claude Code/Codex como implementação interna, não como superfície do cliente.

### Avaliação local consolidada dos repositórios inspecionados

Repositórios analisados localmente:

- `aider`;
- `claudecodeui`;
- `cline`;
- `fazm`;
- `happy`;
- `nimbalyst`;
- `opcode`;
- `yume`;
- `yume-inspect`.

Também permanecem na avaliação os candidatos já mapeados:

- Vibe Kanban;
- OpenCovibe;
- OpenADE;
- OpenClaw + WebChat + Monitor/Control UI;
- OpenCowork;
- Friendly Terminal;
- Localforge;
- OpenACP;
- ClawTab;
- CrewAI;
- LangGraph;
- AutoGen;
- n8n com agentes;
- Dify;
- Flowise;
- Langflow;
- Cursor;
- GitHub Copilot;
- Devin;
- Replit Agent.

| Opção | Licença/base observada | O que oferece | Como acelera o beta | Risco/desaceleração | Conclusão |
|---|---|---|---|---|---|
| Vibe Kanban | Apache 2.0 | Kanban, workspaces, branch por tarefa, terminal, dev server, diff, comentários inline, preview/browser, PRs e múltiplos agentes. | É a base mais pragmática para tarefa -> workspace -> agente -> diff -> PR. Combina bem com o modo como o sistema já opera por issue/PR. | O board próprio/local não deve virar source of truth; precisa espelhar GitHub Projects/issues. Terminal/file access precisam passar por API e allowlist. O projeto também está em sunset, então o fork precisa ser tratado como base congelada. | Melhor base pragmática para o beta, desde que GitHub Projects continue mandando e o Vibe vire UI/espelho operacional. |
| Nimbalyst | MIT por padrão; `packages/collabv3` é AGPL-3.0 ou licença comercial separada | Workspace visual para Codex/Claude Code, sessões paralelas, kanban, tarefas, editores visuais, markdown, mockups, Mermaid, Excalidraw, CSV, data models, Monaco, worktrees, mobile e permissões por projeto. | É o candidato mais forte conceitualmente para "fábrica de produtos digitais", porque não pensa só em código; pensa em artefatos, sessões, tarefas e edição visual. | Monorepo grande, Electron, runtime próprio, partes colaborativas com licença separada e maior custo de adaptação. Pode ser pesado para beta de 30 dias. | Melhor referência estratégica e possível base se houver tempo para investigação profunda; talvez superior ao Vibe no longo prazo. |
| OpenCovibe | Apache 2.0 | Chat visual, tool cards, run history/replay, fork/resume, permissões inline, usage/cost, activity monitor, MCP, memory editor, agent editor, marketplace e file explorer. | Melhor referência para a UX de "ver o agente trabalhando": tool cards, eventos, histórico e monitor. | Expõe exatamente o que precisa ser escondido: memory, agents, settings, MCP, file explorer amplo e detalhes de tool calls. Capar no frontend não basta; precisa API própria e backend sanitizado. | Excelente fonte de componentes de execução/monitor; perigoso como base direta sem reescrever fronteira de backend. |
| ClaudeCodeUI / CloudCLI UI | AGPL-3.0-or-later | Web/mobile UI para Claude Code, Cursor CLI, Codex e Gemini CLI; shell terminal, file explorer, git explorer, sessões, plugins, REST API, sandbox experimental. | Acelera uma UI web remota para Claude/Codex com chat, arquivos, git e sessões. É próximo do que se imagina como "Claude Code em browser". | É genérico e muito exposto: terminal, file explorer, git, plugins e configuração nativa do executor. A licença AGPL pesa se for base de SaaS fechado. Reforça que UI genérica está comoditizada. | Bom candidato técnico para acelerar web UI, mas exige corte forte e decisão jurídica. Não é o diferencial do produto. |
| Cline | Apache 2.0 | Extensão VSCode com agente, edição de arquivos, terminal, browser, checkpoints, diffs, MCP, múltiplos provedores e human-in-the-loop. | Referência muito forte de permissões, checkpoints, browser testing, diff e aprovação humana. | É IDE/VSCode-first, não SaaS web controlado. Não resolve isolamento `system/project` sem construir plataforma em volta. | Referência obrigatória de UX, permissões e auditoria; não é base principal para o beta web. |
| OpenADE | MIT | Cockpit dev com Plan -> Revise -> Execute, HyperPlan, comentários em arquivos/diffs/mensagens, terminal, file browser, process manager, snapshots e worktrees. | Bom para fluxo de planejamento/revisão/execução e cockpit técnico. | Muito orientado a operador dev; expõe terminal, files, processos e worktrees. Menos natural para cliente B2B não técnico. | Boa referência de cockpit e planejamento; segunda linha como base. |
| Yume / `yume-inspect` | Freeware/proprietário; licença permite uso, mas proíbe modificar, distribuir, fazer engenharia reversa e criar derivados | UI nativa para Claude Code oficial como subprocesso; orchestration flow, agentes built-in, background agents, worktree isolation, plugins/skills, rate limit, crash recovery, multi-provider e painéis. | Excelente benchmark de UX Claude Code-native. Confirma que spawnar o Claude Code oficial e preservar hooks/skills/MCP é uma abordagem real. | O repo local é site/releases; código-fonte real não está disponível. A licença declara closed source e proíbe derivados. O clone `yume` ficou incompleto; `yume-inspect` mostra a distribuição/site. | Não usar como base. Usar como benchmark competitivo e inspiração de UX. |
| Aider | Apache 2.0 | CLI madura de pair programming, repo map, git integration, lint/test loop, multi-modelo, voz e grande adoção. | Pode ser runner alternativo para tarefas de código, especialmente edição cirúrgica, testes e commits. | Não é UI, não é sistema operacional de projeto, não preserva sozinho PM/PO/TL/Kanban/gates. | Bom runner alternativo futuro; não é base de produto. |
| Happy | MIT | Web/mobile client para Claude Code e Codex com wrapper CLI, E2E encryption, push notifications, troca entre devices, Happy Agent e Happy Server. | Inspira mobile, notificações, controle remoto e continuidade de sessão. | Foco é controle remoto pessoal, não governança B2B com GitHub Projects, PRs, gates e isolamento de `system/`. | Referência útil para mobile/remote control; não é base principal. |
| Opcode | AGPL-3.0 | Tauri desktop para Claude Code: projetos/sessões, custom agents, background execution, usage analytics, MCP, timeline/checkpoints e editor de instruções. | Boa referência de dashboard de operador, agentes, analytics e checkpoints. | Muito voltado a mexer no universo interno do Claude Code: agentes, MCP, instruções e configs. Para cliente, expõe demais. Licença AGPL pesa. | Referência de operador/admin, não UI cliente. |
| Fazm | README indica MIT; não havia `LICENSE` na raiz local | Agente de computador macOS, browser, docs, Google Apps, voz, ACP bridge, rotinas via launchd, cron jobs e histórico em SQLite. | Inspira plano de execução, rotinas recorrentes, voice UX e automação de desktop/browser. | É macOS/computer-agent, não UI de projeto GitHub/Kanban. Pouca aderência ao isolamento SaaS proposto. | Lateral. Útil como referência de rotinas e agent-as-product, não base da UI. |
| OpenClaw + WebChat + Monitor/Control UI | MIT | Runtime/control plane, Gateway, WebChat, monitor/dashboard, sessões, cron, eventos e agentes. | Pode ser valioso se a decisão for adotar OpenClaw como runtime estruturado. | Exige migrar/reescrever o que já funciona no Claude Code; WebChat/Monitor não podem conectar direto ao Gateway no navegador do cliente. | Manter como opção futura de runtime; não escolher apenas pela UI. |
| UI própria simples + Claude Code executor | Código próprio; termos Claude Code a verificar | Chat, comandos, status, history, eventos, diff e monitor mínimo criados sob medida. | Menor superfície e isolamento mais limpo; preserva executor que já foi validado. | Exige construir UI, diff, stream e monitor, mesmo que enxutos. | Melhor fallback se adaptar bases existentes ficar mais caro que criar a superfície mínima. |
| OpenCowork | MIT | Desktop/local com Claude Code, OpenAI, Gemini, DeepSeek, MCP, skills e sandbox por WSL2/Lima. | Pode inspirar sandbox/empacotamento. | Não resolve SaaS web; foco local/desktop. | Referência secundária. |
| Friendly Terminal | GPL-3.0 | UI amigável para Claude Code/Gemini/Codex, Windows-first e voltada a não-devs. | Pode inspirar onboarding para cliente menos técnico. | GPL e foco local/consumer; pouca aderência a B2B isolado. | Referência de onboarding, não base. |
| Localforge / OpenACP / ClawTab | Licenças a confirmar no `LICENSE` de cada repo | Família de local agent management, ACP/bridges ou interfaces auxiliares. | Podem inspirar integração e bridges. | Menos centrais para Kanban/GitHub/PR/gates. | Referência futura, fora do caminho crítico. |
| CrewAI | Projeto/framework de agentes | Orquestra agentes em Python. | Útil para protótipos agentic específicos. | Recria governança do zero; aumenta overhead que o template justamente evitou. | Concorrente/framework, não base. |
| LangGraph | Projeto/framework de agentes | Grafos, estado e workflows agentic. | Útil para fluxos determinísticos e state machines. | Alto custo para replicar PM/PO/TL, Kanban, issues, PRs, memory e gates. | Concorrente técnico, não substituto do sistema. |
| AutoGen | Projeto/framework de agentes | Conversas multi-agente programáveis. | Útil para pesquisa/protótipo. | Exige muita engenharia de orquestração, parsing e estado. | Fora do caminho crítico. |
| n8n com agentes | Automação/workflows | Bom para integrações e automações de negócio. | Pode inspirar conectores e rotinas. | Não entrega governança de produto, PRs, code review e dual-plane. | Complementar, não base. |
| Dify | App builder/LLMOps | UI para apps LLM, datasets, workflows e deploy. | Útil para apps conversacionais/LLM. | Não resolve fábrica de produto com GitHub Projects/PRs/gates. | Concorrente adjacente. |
| Flowise | Builder visual LLM | Montagem visual de flows. | Ajuda protótipos de RAG/chains. | Não entrega processo enterprise de construção/execução. | Fora do caminho crítico. |
| Langflow | Builder visual LLM | Interface visual para LangChain-like flows. | Pode ajudar demonstrações e workflows de IA. | Mesmo problema: blocos, não metodologia operacional. | Fora do caminho crítico. |
| Cursor | Produto fechado/IDE | Dev assistido por IA. | Referência competitiva de edição e UX dev. | Não é capável como UI controlada do cliente; fechado. | Concorrente/benchmark. |
| GitHub Copilot | Produto fechado/IDE | Autocomplete, chat e agentes no ecossistema GitHub. | Benchmark por integração com GitHub. | Não encapsula metodologia privada nem dual-plane. | Concorrente/benchmark. |
| Devin | Produto fechado | Agente de software autônomo. | Benchmark de promessa comercial. | Não é base técnica; concorre em percepção de mercado. | Benchmark competitivo. |
| Replit Agent | Produto fechado | Geração e edição de apps no Replit. | Benchmark de UX de criação. | Não resolve B2B privado com GitHub do cliente e system isolado. | Benchmark competitivo. |

### Ranking completo para adaptação ao beta

Ranking considerando: aderência ao template, velocidade de beta, capacidade de mostrar diff/status, compatibilidade com Claude Code/Codex, risco de exposição de `system/`, custo de capar e coerência com GitHub Projects como source of truth.

| Rank | Candidato | Por quê |
|---:|---|---|
| 1 | Vibe Kanban | Melhor base pragmática para beta: tarefa, workspace, diff, PR, preview e agentes. Requer transformar o board em espelho do GitHub Projects. |
| 2 | Nimbalyst | Melhor visão estratégica: tarefas, sessões, kanban, artefatos visuais, editores e permissões. Pode ser superior no longo prazo, mas é mais pesado para adaptar. |
| 3 | ClaudeCodeUI / CloudCLI UI | Mais perto de uma web UI genérica para Claude Code/Codex. Acelera bastante, mas expõe terminal/files/config e tem AGPL. |
| 4 | OpenCovibe | Melhor fonte de execution trace, tool cards, replay e monitor. Muito bom para componentes, perigoso como base direta. |
| 5 | Cline | Melhor referência de human-in-the-loop, permissões, browser, checkpoints e diff. Forte para aprender, fraco como base SaaS web. |
| 6 | OpenADE | Bom cockpit Plan -> Revise -> Execute, com diffs e worktrees. Mais operador/dev do que cliente B2B. |
| 7 | Aider | Bom runner alternativo de código, não UI. Pode entrar atrás da API para tarefas específicas. |
| 8 | Happy | Bom para mobile, push e controle remoto de sessões. Não resolve governança GitHub/Kanban. |
| 9 | Opcode | Referência de dashboard/admin para Claude Code, mas expõe internals demais. |
| 10 | OpenClaw + WebChat + Monitor | Só sobe no ranking se a decisão for migrar para OpenClaw como runtime. Como UI isolada, não justifica o risco agora. |
| 11 | UI própria simples | Pode ser a opção mais segura se as bases acima exigirem cortes demais; perde em velocidade visual. |
| 12 | Fazm | Referência lateral para rotinas, computer use e voz; não é base para a UI do projeto. |
| 13 | Yume / `yume-inspect` | Excelente benchmark, mas closed source/proprietário; não é base adaptável. |
| 14 | OpenCowork | Inspiração de sandbox/desktop, não base SaaS. |
| 15 | Friendly Terminal | Inspiração de onboarding, mas GPL/local/consumer. |
| 16 | Localforge / OpenACP / ClawTab | Referências auxiliares; pouca aderência ao core GitHub/PR/Kanban. |
| 17 | n8n com agentes | Complementar para integrações, não substitui o sistema. |
| 18 | Dify | Complementar/concorrente de app LLM, não substitui a governança. |
| 19 | LangGraph | Framework forte, mas recria overhead e processo do zero. |
| 20 | CrewAI | Framework de agentes, não produto pronto para este caso. |
| 21 | AutoGen | Framework/pesquisa; custo alto para governança. |
| 22 | Flowise | Builder visual, não sistema operacional de produto. |
| 23 | Langflow | Builder visual, não sistema operacional de produto. |
| 24 | Cursor | Benchmark fechado, não base capável. |
| 25 | GitHub Copilot | Benchmark fechado, não base capável. |
| 26 | Devin | Benchmark comercial, não base técnica. |
| 27 | Replit Agent | Benchmark comercial, não base técnica. |

### Ranking por tipo de uso

**Base mais provável para o beta**

1. Vibe Kanban.
2. Nimbalyst.
3. ClaudeCodeUI / CloudCLI UI.
4. OpenCovibe.

**Melhores fontes de UX para execução visível**

1. OpenCovibe.
2. Yume.
3. Cline.
4. ClaudeCodeUI / CloudCLI UI.
5. Opcode.

**Melhores fontes para tarefas, board, diff e PR**

1. Vibe Kanban.
2. Nimbalyst.
3. OpenADE.
4. Cline.

**Melhores fontes para isolamento/permissões**

1. Nimbalyst.
2. Cline.
3. ClaudeCodeUI sandbox.
4. Vibe Kanban workspaces.
5. Yume como benchmark de worktree/background agents, mas não como código reutilizável.

**Melhores opções de runner/executor interno**

1. Claude Code, porque o sistema atual já foi validado nele.
2. Codex, como executor alternativo/pluggable.
3. Aider, como runner especializado para edição de código.
4. Runtime alternativo futuro, apenas se o ganho de orquestração superar o custo de troca.

### Decisão operacional

Para o beta, a melhor direção é:

> Vibe Kanban ou Nimbalyst como base visual principal, OpenCovibe/Cline/Yume como referências de execution trace e permissões, API própria como fronteira obrigatória, Claude Code como executor interno inicial e GitHub Projects/issues/PRs como source of truth.

Essa decisão usa a arquitetura alvo definida anteriormente: UI controlada, API própria, policy/sanitizer, allowlist de `project/`, bloqueio de `system/` e `platform/`, runner privado e GitHub do cliente como trilha operacional.

Runtimes alternativos não devem ser removidos da tese técnica, mas também não devem ser dependência obrigatória do beta se Claude Code já entrega melhor qualidade e menor risco.

Vibe Kanban deve continuar como o caminho mais rápido se o objetivo for beta vendável em até 30 dias. Nimbalyst deve ser investigado em paralelo como candidato mais ambicioso para a plataforma definitiva. OpenCovibe deve ser tratado como biblioteca de ideias de UX, não como fonte de verdade operacional.

---

## Encapsulamento do executor agentic

### Estado atual

```text
Usuário
  ↓
Claude Code
  ↓
arquivos locais
  ↓
sistema + projeto
```

Problemas:

- UI fechada;
- operador tem acesso total;
- cliente poderia acessar lógica interna;
- não há camada de controle;
- não é produto distribuível.

### Estado alvo

```text
Usuário
  ↓
UI controlada
  ↓
API própria
  ↓
runtime privado / executor agentic interno
  ↓
sistema privado + GitHub do cliente
```

O executor agentic passa a ser:

> processo interno de execução, não interface direta do cliente.

### Estratégia de encapsulamento

O beta não precisa migrar para outro runtime se Claude Code já executa bem o sistema atual. O problema principal não é qualidade de execução: é isolamento, UI controlada, fronteira entre `system/`, `platform/` e `project/`, sanitização e acesso seguro do cliente.

A prioridade é encapsular o comportamento que já funciona em um executor interno controlado por API. Qualquer runtime alternativo só deve entrar se trouxer ganho real, sem enfraquecer a arquitetura dual.

!!! note
    Decisão do beta: preservar Claude Code como executor interno inicial e resolver isolamento por arquitetura de produto. Trocar o executor não é objetivo em si.

O contrato que precisa ser preservado é comportamental:

- PM/PO/TL continuam existindo como papéis operacionais;
- `/kickoff` e `/advance` continuam sendo fluxos centrais;
- GitHub/Kanban continua sendo fonte de verdade;
- gates continuam obrigatórios;
- nenhum agente faz merge do próprio trabalho;
- falhas de execução viram issues;
- outputs externos são sanitizados.

### Decisão para o beta

Para reduzir risco, a decisão recomendada para o beta é:

- manter Claude Code como executor interno inicial, se continuar sendo o caminho de maior qualidade;
- permitir Codex como executor alternativo;
- permitir Aider como executor especializado para código, se útil;
- desenhar o job runner para aceitar runtime alternativo futuramente, sem acoplamento desnecessário;
- não expor nenhum executor diretamente ao cliente;
- tratar todos os executores como implementação interna atrás da API própria.

---

## Uso da UI web

### Decisão

Usar uma UI web controlada baseada em Vibe Kanban, Nimbalyst ou outra base equivalente, com componentes de execution trace inspirados em OpenCovibe/Cline/Yume.

WebChats de runtimes agentic podem continuar como referência, mas não devem ser premissa obrigatória do beta.

### Motivo

A UI principal precisa suportar:

- conversa livre;
- comandos;
- histórico sanitizado;
- status de execução;
- eventos públicos de execução;
- diffs do projeto;
- PR previews;
- artefatos;
- board espelhado do GitHub;
- fluxo próximo ao uso atual via Claude Code;
- menor superfície de exposição que Control UI, Dashboard completo ou file explorer amplo.

### Adaptações obrigatórias

Remover ou substituir:

- conexão direta com Gateway/runtime interno;
- WebSocket direto do navegador para o runtime;
- autodiscovery de agentes;
- exposição de sessões internas;
- acesso a arquivos;
- views de sistema;
- referências a memory raw;
- settings expostos;
- agent listing;
- tool listing sensível;
- MCP/config editor visível ao cliente;
- shell irrestrito;
- file explorer amplo.

Substituir por:

```text
UI Web controlada
  ↓
API própria
  ↓
runtime privado / executor agentic interno
```

Endpoints esperados:

```http
POST /chat
POST /command
GET /status
GET /history
GET /events
GET /metrics
GET /project/changes
GET /project/artifacts
```

### Diff e mudanças do projeto

O cliente precisa conseguir ver diffs e mudanças propostas no projeto dele. Isso é parte da confiança operacional do produto e aproxima a experiência de Claude Code/Codex Desktop.

Regra central:

```text
pode ver diff do project/
não pode ver nada do system/
não pode ver nada do platform/
```

A UI pode ter uma área de `Changes`, `Diff`, `PR Preview` ou equivalente, mas ela nunca deve ler o filesystem diretamente.

Fluxo permitido:

```text
UI
  ↓
GET /project/changes
  ↓
API própria
  ↓
git diff limitado ao project/
  ↓
sanitizer
  ↓
UI renderiza diff público
```

---

## Uso do Monitor/Dashboard

### Decisão

Reaproveitar parcialmente componentes de Monitor/Dashboard, não como aplicação principal.

O Monitor serve para observabilidade e confiança operacional.

Deve mostrar:

- status de execução;
- progresso do pipeline;
- eventos resumidos;
- erros sanitizados;
- latência;
- custo aproximado;
- última execução;
- artefatos gerados;
- links para issues/PRs/outputs;
- histórico operacional resumido;
- gates executados;
- versão do sistema usada, por exemplo `system@v0.3.1`.

### Exemplo de visualização permitida

```text
Pipeline Editorial - Execução diária

Status: concluído
Tempo total: 2m14s
Custo aproximado: R$ X
Sistema: system@v0.3.1

Etapas:
- Coleta de dados: concluída
- Transformação: concluída
- Análise: concluída
- Geração de conteúdo: concluída
- Publicação: concluída

Artefatos:
- relatório.pdf
- post_linkedin.md
- presentation.pptx
```

### O que o Monitor não pode mostrar

- agents internos;
- prompts;
- arquivos de sistema;
- memória raw;
- settings;
- stack traces completos;
- raciocínio interno;
- chamadas internas do runtime;
- regras do `CLAUDE.md`;
- regras do `SOUL.md`;
- regras do `AGENTS.md`;
- paths internos;
- payload bruto de tools.

---

## Componentes que não devem ser usados diretamente

### Control UI

Não usar como base principal para cliente.

Motivos:

- mais acoplada ao controle do sistema;
- expõe mais superfície interna;
- pressupõe que o usuário é operador/dono do sistema;
- maior risco de exposição de agents, tools e estado interno.

### TUI

Não usar para cliente.

Motivos:

- interface de terminal;
- útil para operador técnico;
- inadequada para produto web B2B.

### Dashboard completo

Não usar direto.

Motivos:

- expõe estrutura operacional demais;
- deve ser usado apenas como fonte de componentes visuais;
- precisa de sanitização e redesign parcial.

---

## Backend/API própria

Criar uma API intermediária que seja a única superfície entre UI e runtime.

### Endpoints mínimos

```http
POST /chat
POST /command
GET /status
GET /events
GET /metrics
GET /history
GET /project/changes
GET /project/artifacts
POST /approval
```

### Responsabilidades da API

- autenticar cliente;
- receber mensagens da UI;
- receber comandos;
- carregar contexto do sistema privado;
- carregar estado do GitHub do cliente;
- chamar runtime/executor;
- chamar LLM API ou CLI/SDK interno;
- executar ações autorizadas;
- sanitizar outputs;
- bloquear vazamentos;
- retornar apenas dados permitidos;
- registrar eventos;
- controlar rate limits básicos;
- proteger tokens;
- montar eventos públicos de execução;
- impedir leitura de `system/` e `platform/`;
- garantir que diffs e artefatos visíveis pertencem ao `project/`.

---

## Exemplos de fluxo

### Chat livre

```text
Cliente:
"Me explica o estado atual do projeto"

UI:
POST /chat

Backend:
- valida usuário
- lê issues do GitHub do cliente
- lê PRs relevantes
- lê estado do Kanban
- monta contexto permitido
- carrega regras internas sem expô-las
- chama runtime/LLM
- sanitiza resposta

UI:
exibe resposta final
```

### Comando `/advance`

```text
Cliente:
"/advance"

UI:
POST /command

Backend:
- valida comando
- consulta Kanban do cliente
- identifica próxima ação
- aciona executor interno
- executa agentes internamente
- cria/comenta/move issues no GitHub do cliente
- retorna resumo sanitizado
```

### Falha em pipeline

```text
Rotina agendada falha
  ↓
Backend captura evento
  ↓
Runtime gera diagnóstico interno
  ↓
Sanitizer remove detalhes internos
  ↓
GitHub issue é criada
  ↓
Monitor mostra falha resumida
```

---

## Isolamento de arquivos de sistema

### Estrutura sugerida

```text
/opt/dual-agent-saas/
  system/
    CLAUDE.md
    SOUL.md
    AGENTS.md
    agents/
    hooks/
    commands/
    memory/
    skills/
    settings.json
    templates/
    policies/
    sanitizer/

  platform/
    frontend/
    backend/
    runner/
    adapters/
    deploy/

  clients/
    acme/
      project/
      public-logs/
      artifacts/

  logs/
    internal/
    public/
```

### Regras obrigatórias

A UI não pode:

- listar `/system`;
- listar `/platform`;
- ler arquivos diretamente;
- baixar arquivos de sistema;
- exibir nomes de agents internos;
- acessar settings;
- acessar memória raw;
- acessar logs internos;
- acessar Gateway/runtime interno diretamente;
- acessar shell direto;
- acessar file explorer amplo.

O runtime não pode oferecer ao usuário:

- file read genérico;
- shell aberto;
- endpoint de filesystem;
- endpoint de prompt dump;
- endpoint de agent listing;
- endpoint de memory dump;
- endpoint de settings/config;
- endpoint de MCP config.

O agente cliente deve operar com allowlist:

```text
allowed:
  /opt/dual-agent-saas/clients/<cliente>/project

denied:
  /opt/dual-agent-saas/system
  /opt/dual-agent-saas/platform
  /opt/dual-agent-saas/logs/internal
  outros clientes
  env vars
  tokens
```

---

## Integração com GitHub do cliente

### GitHub do cliente como source of truth

O sistema deve acessar:

- issues;
- PRs;
- commits;
- Kanban;
- comentários;
- labels;
- milestones, se necessário;
- branches;
- arquivos do projeto/produto, quando autorizado.

### Ações permitidas

- criar issue;
- comentar issue;
- mover card;
- abrir PR;
- revisar PR;
- sugerir mudanças;
- registrar entrega;
- vincular commit a issue;
- registrar falha sanitizada;
- criar artefato de output.

### Ações proibidas

- escrever arquivos de sistema no repo do cliente;
- mencionar regras internas;
- expor nomes ou conteúdo dos arquivos de sistema;
- despejar raciocínio completo;
- comentar detalhes internos dos agentes;
- expor prompts;
- expor paths internos;
- expor payload bruto de tools.

---

## Audit trail operacional no GitHub do cliente

O sistema deve registrar no GitHub do cliente:

- issues criadas;
- critérios de aceite;
- comentários de progresso;
- PRs vinculados;
- commits referenciando issues;
- status de execução;
- falhas sanitizadas;
- links para artefatos gerados;
- decisões finais relevantes;
- gates executados;
- versão pública do sistema usada.

O sistema não deve registrar:

- prompts internos;
- nomes de arquivos de sistema;
- conteúdo de agents;
- raciocínio completo;
- paths internos;
- stack traces brutos;
- payload bruto de tools.

---

## Commits e PRs

### Convenções

- commits devem referenciar issue;
- mensagens devem seguir Conventional Commits;
- PRs devem conter:
  - issue relacionada;
  - resumo da mudança;
  - critério de aceite;
  - testes realizados;
  - riscos;
  - próximos impactos.

### Proibição

Nenhum agente deve fazer merge do próprio trabalho.

Regra esperada:

```text
especialista implementa
  ↓
tech-lead revisa
  ↓
QA valida
  ↓
merge ocorre após validação
  ↓
product-owner fecha issue
```

---

## Sanitização de output

Criar camada de sanitização para tudo que sai para:

- UI;
- GitHub;
- logs visíveis;
- Monitor;
- comentários;
- PRs;
- artefatos públicos.

### Remover ou reescrever

- nomes de agents internos quando desnecessário;
- referências a `CLAUDE.md`;
- referências a `SOUL.md`;
- referências a `AGENTS.md`;
- menções a hooks internos;
- prompts;
- raciocínio operacional detalhado;
- mensagens de erro com paths internos;
- stack traces brutos;
- dumps de memória;
- payload de tools;
- variáveis de ambiente;
- tokens;
- caminhos de `system/` e `platform/`.

### Exemplo ruim

```text
O PR foi rejeitado conforme regra definida no CLAUDE.md.
```

### Exemplo correto

```text
O PR foi rejeitado porque não atende ao critério de aceite definido na issue.
```

---

## Modelo de sessão

O sistema pode reconstruir contexto a cada sessão/chamada.

Isso é aceitável porque:

- LLM é stateless;
- estado do projeto vive no GitHub do cliente;
- arquivos do sistema são recarregáveis;
- custo maior está na chamada LLM, não na leitura dos markdowns.

### Estratégia beta

Usar reconstrução simples:

```text
request
  ↓
load private system context
  ↓
load client project state
  ↓
call runtime/LLM
  ↓
sanitize result
  ↓
write result
```

Não implementar memória de sessão sofisticada nesta fase.

---

## Artefatos do plano de execução

O plano de execução pode gerar:

- PDFs;
- PPTX;
- gráficos;
- relatórios;
- posts;
- boletins;
- arquivos markdown;
- dados processados;
- outputs publicados;
- websites;
- dashboards;
- APIs;
- pipelines;
- análises;
- modelos;
- datasets tratados;
- documentação técnica;
- documentação de produto.

### Evolução posterior

Criar bibliotecas e templates pré-compilados para:

- PPTX;
- PDF;
- gráficos;
- layouts;
- relatórios recorrentes;
- páginas;
- dashboards;
- pipelines recorrentes.

Motivo:

- reduzir variabilidade;
- melhorar consistência visual;
- evitar geração dinâmica de código a cada execução;
- melhorar auditabilidade.

---

## Templates sincronizáveis

A arquitetura deve manter separação entre:

### 1. Sistema base privado

- agents universais;
- commands;
- hooks;
- regras de governança;
- runtime/adapters;
- lógica de orquestração;
- sanitização;
- integração com LLM;
- integração com GitHub.

### 2. Projeto/produto do cliente

- código;
- issues;
- PRs;
- documentação;
- artefatos;
- pipelines específicos;
- dados específicos;
- outputs.

### 3. Domínio/template verticalizado

- vocabulário especializado;
- agentes de domínio;
- workflows específicos;
- outputs próprios do domínio.

A evolução do sistema base deve poder ser propagada para projetos/clientes sem expor arquivos internos.

---

## Infraestrutura beta

### Decisão

Usar uma única VM na nuvem para o beta, controlada pela infraestrutura própria.

O cliente acessa apenas:

- link web da UI;
- login/autenticação da UI;
- GitHub privado do projeto dele.

O cliente não acessa a VM, SSH, filesystem, runtime, logs internos, repo privado do sistema ou arquivos `.md` de sistema.

### Composição da VM

```text
VM única
  ├── frontend web
  ├── backend/API
  ├── job runner privado
  ├── executor agentic interno
  │   ├── Claude Code inicial/preferencial
  │   ├── Codex opcional
  │   ├── Aider opcional
  │   └── runtime alternativo opcional/futuro
  ├── system/
  │   └── clone sincronizado do repo privado do sistema
  ├── platform/
  │   └── código SaaS privado
  ├── clients/<cliente>/project/
  │   └── clone sincronizado do repo privado do cliente
  ├── integração GitHub
  ├── integração LLM
  ├── logs/internal/
  └── logs/public/
```

### Modelo de repositórios

O sistema opera com dois repositórios principais e um código de plataforma privado:

```text
Repo privado do sistema (seu GitHub)
  └── system/
      ├── SOUL.md / CLAUDE.md
      ├── AGENTS.md
      ├── agents/
      ├── commands/
      ├── hooks/
      ├── memory/
      ├── skills/
      ├── settings.json
      ├── templates/
      ├── policies/
      └── sanitizer/

Repo privado da plataforma (seu GitHub)
  └── platform/
      ├── frontend/
      ├── backend/
      ├── runner/
      ├── adapters/
      ├── auth/
      └── deploy/

Repo privado do cliente (GitHub do cliente)
  └── project/
      ├── código do produto
      ├── documentação pública do projeto
      ├── artefatos
      ├── issues
      ├── PRs
      ├── commits
      └── Kanban
```

Na VM:

- `system/` é sincronizado a partir do repo privado do sistema;
- `platform/` é sincronizado a partir do repo privado da plataforma;
- `project/` é sincronizado a partir do repo privado do cliente;
- o runtime lê `system/` como metodologia privada;
- o runtime opera em `project/` como workspace do cliente;
- a UI nunca acessa `system/`, `platform/` ou `project/` diretamente;
- toda interação visível passa pela API e pelo sanitizer;
- outputs permitidos são escritos no GitHub do cliente.

### Regras de sincronização

- `system/` deve ser tratado como read-only durante execuções normais.
- `platform/` deve ser tratado como inacessível para o agente do cliente.
- Atualização de `system/` acontece apenas por deploy/control plane do operador.
- Atualização de `platform/` acontece apenas por deploy/control plane do operador.
- `project/` é o único workspace gravável para código, docs, artefatos, branches e commits do cliente.
- Arquivos de sistema nunca podem ser copiados para `project/`.
- Templates privados só podem gerar artefatos públicos depois de renderização/sanitização.
- Cada execução deve registrar qual versão do sistema foi usada, por exemplo `system@v0.3.1`.
- Tokens devem ser separados:
  - token do operador para clonar/atualizar `system`;
  - token do operador para deploy de `platform`;
  - token/GitHub App do cliente para operar `project`;
  - tokens LLM apenas no backend.

### Acesso

Cliente acessa:

```text
https://produto.seudominio.com
```

Cliente não acessa:

- SSH;
- executor interno direto;
- runtime alternativo direto, se existir;
- Gateway direto, se existir;
- filesystem;
- repo interno do sistema;
- repo interno da plataforma;
- logs internos;
- variáveis de ambiente;
- tokens;
- prompts.

---

## Autenticação

Para beta, implementar autenticação simples:

- login/senha;
- token estático;
- ou autenticação via basic auth/reverse proxy.

Não implementar RBAC avançado nesta fase.

---

## Segurança mínima

### Obrigatório

- runtime/Gateway/executor não exposto publicamente;
- apenas API própria exposta;
- arquivos de sistema fora do root público;
- arquivos de plataforma fora do workspace do agente cliente;
- variáveis de ambiente protegidas;
- tokens GitHub e LLM no backend;
- logs externos sanitizados;
- bloqueio de file explorer amplo;
- bloqueio de agent listing;
- bloqueio de memory raw;
- bloqueio de shell irrestrito;
- bloqueio de file read genérico;
- allowlist de path por cliente;
- sanitizer obrigatório em toda saída.

---

## Uso de LLM API

O sistema deve usar LLM via API ou executor autorizado.

Inicialmente:

- Anthropic Claude via Claude Code/API, se permitido e mantiver qualidade.

Possibilidades futuras:

- OpenAI/Codex;
- Aider com modelos compatíveis;
- runtime alternativo com provedores plugáveis;
- outros modelos compatíveis.

Regras:

- preferir BYOK (`bring your own key`) quando os termos do provedor permitirem uso hospedado/B2B;
- se a chave for da infraestrutura, custo deve ser embutido no preço ou repassado de forma transparente;
- custo de tokens deve ser separado do valor da metodologia/plataforma;
- logs de custo devem ser agregados e sanitizados;
- termos de Claude Code, Codex, Anthropic, OpenAI e demais provedores devem ser avaliados separadamente para uso B2B hospedado.

---

## Modelo comercial beta

### Definição

O produto será oferecido como:

> acesso a uma plataforma gerenciada hospedada na infraestrutura própria, operando sobre o GitHub do cliente e encapsulando uma metodologia privada de delivery com agentes.

A definição comercial consolidada é:

> Service-as-a-Product entregue como Product-as-a-Service.

Isso significa que o serviço consultivo/COE foi productizado em método, agents, commands, hooks, gates, policies, templates e workflows. O produto não é transferido ao cliente: ele consome a capacidade como serviço contínuo, enquanto a inteligência operacional permanece privada e o GitHub do cliente continua sendo a superfície operacional visível.

### Camadas da oferta

```text
Ativo proprietário
  .mds, agentes, comandos, hooks, gates, policies, templates, workflows e método.

Produto
  sistema dual multi-agente que cria, evolui e opera produtos digitais.

Entrega
  plataforma web hospedada, com UI, API, runner, sanitizer, monitor e integração GitHub.

Modelo comercial
  setup/onboarding + mensalidade + eventual repasse/uso separado de tokens.
```

### Natureza da venda

O produto não deve ser vendido como consultoria tradicional. Ele deve ser vendido como uma plataforma gerenciada que automatiza parte da função de uma consultoria/COE de produto e engenharia.

A consultoria é o DNA metodológico. O produto é o ativo. A plataforma gerenciada é a forma de entrega. O cliente deve perceber que está comprando uma capacidade operacional contínua, não horas avulsas: criar projeto, organizar backlog, operar Kanban/GitHub, gerar issues e PRs, revisar entregas, aplicar gates, executar rotinas, registrar decisões, transformar falhas em issues, gerar artefatos e manter rastreabilidade.

### Operação com ponto focal

No beta, o uso deve pressupor um ponto focal treinado do cliente.

Esse papel é equivalente ao ponto focal que uma empresa teria ao contratar uma consultoria ou ao operar um COE interno:

```text
Ponto focal do cliente
  ↓
Interface web
  ↓
Sistema dual multiagente
  ↓
GitHub do cliente
  ↓
issues, PRs, backlog, rotinas, artefatos, decisões
```

- conversa com o sistema;
- aprova caminhos;
- dispara comandos;
- acompanha status;
- revisa diffs e PRs;
- valida outputs;
- responde dúvidas de produto/domínio;
- decide prioridades quando necessário.

O produto não precisa ser self-service irrestrito para todos os funcionários no beta. Ele pode ser high-touch, com onboarding, governança e operador/ponto focal definido.

### Cobrança

Modelo recomendado para beta:

- taxa de setup/onboarding para configuração inicial;
- mensalidade pelo acesso à plataforma gerenciada;
- infraestrutura básica incluída na mensalidade;
- custo fixo de VM previsível incluído no preço;
- tokens LLM pagos pelo cliente via chave própria, quando possível;
- alternativamente, tokens podem ser repassados por consumo em fase posterior;
- customizações profundas cobradas à parte.

O uso de chave própria do cliente para Claude Code/LLM deve ser tratado como modelo BYOK (`bring your own key`). Isso não descaracteriza a oferta como produto/plataforma gerenciada, porque o valor vendido não é a chave do modelo: é a metodologia, a orquestração, a UI controlada, o isolamento, a execução governada, a integração GitHub, a rastreabilidade, o monitoramento, a adaptação por cliente e a evolução contínua.

Não será oferecido como:

- repo;
- template baixável;
- executável;
- instalação local no cliente;
- pacote open-source;
- fork entregável.

O cliente compra:

- acesso à interface;
- operação do sistema;
- adaptação ao projeto/domínio;
- execução governada;
- rastreabilidade;
- outputs;
- uma capacidade operacional de delivery de produto.
- evolução contínua.

O cliente não compra:

- os `.mds` privados;
- os prompts;
- a estrutura interna de agentes;
- os templates privados;
- o código da plataforma;
- o runtime/control plane.

### Formulação comercial curta

> Em vez de vender horas de consultoria ou entregar um template, vendemos acesso a um sistema hospedado que executa um método proprietário de entrega de produtos digitais, operando no GitHub do cliente com backlog, PRs, issues, rotinas, gates e rastreabilidade.

### Posicionamento recomendado

Usar em conversas comerciais:

> Plataforma gerenciada de delivery de produtos digitais com agentes de IA.

Usar em explicações estratégicas:

> Service-as-a-Product entregue como Product-as-a-Service.

Evitar como categoria principal:

- consultoria pura;
- SaaS self-service genérico;
- template;
- framework de agentes;
- UI para Claude Code;
- automação pontual.

---

## Estimativa de prazo

Prazo realista:

```text
2 semanas a 1 mês
```

### Estimativa por bloco

| Bloco | Estimativa |
|---|---:|
| Escolha/fork da UI base | 1-3 dias |
| Setup VM | 1-3 dias |
| Separação system/platform/project | 1-3 dias |
| Backend/API intermediária | 3-7 dias |
| Runner privado com Claude Code | 3-7 dias |
| Adaptação UI chat/comandos | 3-7 dias |
| Integração GitHub cliente | 2-5 dias |
| Diff/PR/status público | 2-5 dias |
| Monitor parcial | 2-5 dias |
| Sanitização e hardening mínimo | 2-5 dias |
| Teste end-to-end | 2-5 dias |
| Ajustes finais | 2-5 dias |

---

## Fora de escopo no beta

Não implementar agora:

- multi-tenant;
- RBAC avançado;
- billing automático;
- isolamento enterprise por cliente;
- marketplace;
- versão on-premise;
- proteção avançada contra engenharia reversa comportamental;
- auditoria enterprise completa;
- UI completa própria do zero, se uma base acelerar;
- controle sofisticado de sessão;
- observabilidade enterprise;
- automação total de priorização;
- templates finais de artefatos para todos os domínios.

---

## Riscos conhecidos

### Aceitáveis no beta

- cliente pode inferir padrões;
- cliente pode observar comportamento;
- cliente pode tentar reproduzir lógica;
- segurança contra engenharia reversa comportamental ainda não é prioridade.

### Não aceitáveis

- cliente acessar arquivos de sistema;
- cliente acessar arquivos de plataforma;
- cliente acessar Gateway/runtime/executor diretamente;
- cliente listar agents;
- cliente ver prompts;
- cliente ver memória raw;
- cliente conseguir executar shell irrestrito;
- cliente conseguir ler filesystem interno;
- cliente copiar o sistema com um clique.

---

## Critérios de aceite

### UI

- cliente acessa por link web;
- cliente faz login;
- cliente consegue conversar com o sistema;
- cliente consegue executar comandos;
- cliente consegue visualizar status de execução;
- cliente consegue ver eventos resumidos;
- cliente consegue ver diffs do projeto;
- cliente consegue ver PRs/issues/artefatos;
- cliente não vê arquivos de sistema;
- cliente não vê arquivos de plataforma;
- cliente não vê agents internos;
- cliente não vê memória raw;
- cliente não acessa Gateway/runtime/executor diretamente.

### Runtime

- executor roda internamente;
- sistema carrega arquivos internos;
- comandos funcionam;
- hooks/session_start funcionam ou têm substituto equivalente;
- chamadas LLM funcionam via API/CLI/SDK autorizado;
- runtime não expõe tools perigosas ao cliente.

### GitHub

- sistema lê Kanban/issues/PRs do cliente;
- sistema cria issues;
- sistema comenta issues;
- sistema abre PRs, se aplicável;
- sistema referencia issues nos commits;
- sistema registra falhas sanitizadas;
- sistema não escreve arquivos de sistema no repo do cliente.

### Monitor

- exibe status de execução;
- exibe eventos resumidos;
- exibe métricas básicas;
- exibe custos aproximados, se disponível;
- exibe links para issues/PRs/artefatos;
- não exibe agents;
- não exibe prompts;
- não exibe paths internos;
- não exibe stack trace bruto.

### Segurança

- runtime privado;
- API própria como única superfície;
- filesystem interno inacessível;
- outputs sanitizados;
- logs visíveis não expõem paths/prompts/agents;
- tokens protegidos;
- endpoints sensíveis inexistentes ou bloqueados.

### Produto B2B beta

- pelo menos um projeto iniciado do zero é desenvolvido/operado pelo beta;
- GitHub do cliente funciona como fonte de verdade;
- `/kickoff` e `/advance` funcionam no fluxo web;
- falha de execução vira issue;
- cliente consegue auditar o que foi feito sem acessar o sistema privado.

---

## Issues menores sugeridas

```markdown
- [ ] Escolher base final de UI para beta
- [ ] Forkar/congelar base escolhida com registro de origem
- [ ] Setup VM única na nuvem
- [ ] Criar estrutura system/platform/clients
- [ ] Sincronizar system com repo privado do sistema
- [ ] Sincronizar project com repo privado do cliente
- [ ] Criar backend wrapper com /chat e /command
- [ ] Implementar runner privado com Claude Code
- [ ] Implementar allowlist de path para project/
- [ ] Bloquear acesso a system/ e platform/
- [ ] Integrar GitHub do cliente
- [ ] Implementar leitura de GitHub Projects/issues/PRs
- [ ] Implementar criação/comentário/movimentação de issues
- [ ] Implementar diff público de project/
- [ ] Implementar sanitização de outputs
- [ ] Implementar eventos públicos de execução
- [ ] Reaproveitar componentes de Monitor para status/eventos
- [ ] Implementar autenticação simples
- [ ] Bloquear tools perigosas
- [ ] Testar fluxo /kickoff
- [ ] Testar fluxo /advance
- [ ] Testar fluxo de chat livre
- [ ] Testar falha de pipeline -> criação de issue
- [ ] Testar geração de artefato
- [ ] Testar ausência de vazamento de arquivos de sistema
- [ ] Testar ausência de vazamento de arquivos de plataforma
- [ ] Testar PR/diff/status público
- [ ] Documentar limites do beta
```

---

## Resultado esperado

Ao final desta epic, o sistema deixa de ser:

```text
ambiente local operado via Claude Code
```

E passa a ser:

```text
produto web beta operado via UI controlada,
com runtime privado,
estado operacional no GitHub do cliente,
arquivos de sistema isolados,
arquivos de plataforma inacessíveis
e execução via executor agentic interno.
```

---

## Formulação final

O cliente não recebe o sistema.

O cliente recebe acesso a:

> uma interface web que aciona um sistema de agentes hospedado e controlado pela infraestrutura própria.

A inteligência permanece privada.

O GitHub do cliente permanece como espaço operacional do projeto/produto.

Comercialmente, o beta deve ser apresentado como:

> uma plataforma gerenciada de delivery de produtos digitais com agentes de IA.

Conceitualmente, o modelo é:

> Service-as-a-Product entregue como Product-as-a-Service.

Ou seja:

> uma função consultiva/COE de produto, engenharia e gestão productizada em software, hospedada como sistema privado, operada por um ponto focal treinado do cliente e registrada no GitHub dele com governança, gates e rastreabilidade.

