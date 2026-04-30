# Agentes especialistas

Os 10 agentes que executam o trabalho técnico e estratégico.

---

## Especialistas técnicos

### data-engineer

**Aciona quando:** pipelines de dados, ETL, ingestion, qualidade de dados, transformações.

**Entrega:** scripts Python/SQL, configuração de pipelines, documentação de schemas.

**Colabora com:** ml-engineer (entrega dados processados), qa (valida qualidade), researcher (dados de mercado).

**Skill:** `.agents/skills/data-engineering/SKILL.md`

---

### data-scientist

**Aciona quando:** análise exploratória, modelagem estatística, identificação de anomalias, insights para negócio ou editorial.

**Entrega:** análise com contexto estatístico, modelos validados prontos para produtização pelo ml-engineer.

**Colabora com:** data-engineer (dados limpos), researcher (benchmarks analíticos), marketing-strategist (embasa copy com análise).

**Skills:** `.agents/skills/data-engineering/SKILL.md`, `.agents/skills/ml-engineering/SKILL.md`

---

### ml-engineer

**Aciona quando:** produtização de modelos validados pelo data-scientist — pipeline de treino, serving, monitoramento de drift.

**Entrega:** pipeline de treino automatizado, serviço de serving, relatório de performance em produção.

**Colabora com:** data-scientist (recebe modelos validados), data-engineer (dados para treino), researcher (benchmarks).

**Skill:** `.agents/skills/ml-engineering/SKILL.md`

---

### ai-engineer

**Aciona quando:** integração de LLMs, construção de agentes, RAG, evals, prompts.

**Entrega:** implementação de agentes, pipeline de RAG, suite de evals, relatório de performance.

**Colabora com:** ml-engineer (modelos base), researcher (estado da arte em LLMs).

**Skill:** `.agents/skills/ai-engineering/SKILL.md`

---

### infra-devops

**Aciona quando:** cloud, CI/CD, containers, observabilidade, deploy, IaC.

**Entrega:** workflows GitHub Actions, Dockerfiles, scripts Terraform/CDK, dashboards de observabilidade.

**Colabora com:** security-auditor (revisão de infra), frontend-engineer (deploy de apps web).

**Skill:** `.agents/skills/infra-devops/SKILL.md`

---

### qa

**Aciona quando:** testes unitários, integração, E2E, cobertura, qualidade de código.

**Entrega:** suite de testes, relatório de cobertura, configuração de CI para testes.

**Colabora com:** data-engineer (testes de pipeline), data-scientist (avalia modelos e métricas).

**Skill:** `.agents/skills/qa-testing/SKILL.md`

---

### security-auditor

**Aciona quando:** revisão de segurança, vulnerabilidades, OWASP, compliance, secrets.

**Entrega:** relatório de auditoria, lista de vulnerabilidades priorizadas, recomendações de mitigação.

**Colabora com:** infra-devops (revisão de infra e secrets), tech-lead (priorização de correções).

**Skill:** `.agents/skills/security-audit/SKILL.md`

---

### frontend-engineer

**Aciona quando:** web, UI/UX, acessibilidade, performance web, frameworks frontend.

**Entrega:** componentes, páginas, testes de UI, relatório de acessibilidade.

**Colabora com:** infra-devops (deploy), researcher (UX research e benchmarks).

**Skill:** `.agents/skills/frontend-engineering/SKILL.md`

---

## Especialistas de inteligência

### researcher

**Aciona quando:** pesquisa de mercado, benchmarks técnicos, análise competitiva, estado da arte.

**Entrega:** relatório de pesquisa em `docs/research/` com data e versão.

**Colabora com:** todos os agentes que precisam de inteligência de mercado ou técnica.

**Skills:** `.agents/skills/market-research/SKILL.md`

---

### marketing-strategist

**Aciona quando:** go-to-market, posicionamento, mensagem de produto, canais de aquisição.

**Entrega:** estratégia GTM em `docs/business/`, copy de campanha, plano de lançamento.

**Colabora com:** researcher (dados de mercado para estratégia).

**Skill:** `.agents/skills/go-to-market/SKILL.md`
