# Update Memory — Atualizar Memória do Projeto (Incremental)

Você é o **`project-manager`**. Execute uma atualização **incremental** da memória — janela = última entrada do `project_history.md` até hoje.

Para reconstrução completa (varredura desde o primeiro commit + auditoria de datas antigas + detecção de ancoragens emergentes), use `/update-memory-full`.

---

## ⚠️ Escopo deste command

**Sim faz:**
- Atualiza `project_history.md` com o que aconteceu na janela incremental
- Aplica auditoria narrativa **dentro da janela** (viradas compostas que cabem no período)
- Propõe mudanças no `project_genesis.md` quando virada de fundamento aparece — sem aplicar
- Atualiza `user_profile.md` direto se houver mudança de contexto do fundador

**Não faz** (escopo do `/update-memory-full`):
- Auditoria de datas antigas já registradas
- Detecção de ancoragens emergentes no genesis (padrões repetidos no histórico todo)
- Auditoria comparativa massiva PRs/issues vs entradas de todas as datas

Se você suspeita que datas antigas estão subdocumentadas ou que há ancoragens emergentes, pare aqui e use `/update-memory-full`.

---

## O que o `project-manager` faz

### Passo 1 — Levantar o que aconteceu na janela

Leia, nesta ordem:

1. A última entrada em `.claude/memory/project_history.md` — define o início da janela
2. `git log --oneline` desde a data da última entrada
3. Issues fechadas desde a última entrada: `gh issue list --state closed --limit 30 --json number,title,closedAt,labels`
4. PRs mergeados desde a última entrada: `gh pr list --state merged --limit 30 --json number,title,mergedAt,baseRefName`
5. Documentos novos ou revisados em `docs/` desde a última entrada

### Passo 2 — Atualizar `project_history.md` com auditoria narrativa

Adicione uma **nova entrada no topo** com a data de hoje. Antes de escrever bullets isolados, faça uma passada narrativa **na janela incremental**:

**Auditoria narrativa light:**

Para cada cluster de 2-3 PRs/issues que você está prestes a documentar como bullets separados, pergunte:

1. **Isso é só implementação ou muda um fundamento?** (ex: critério passou de arbitrário para citável; estimativa virou fato; opinião virou base legal/regulatória)
2. **Esses 2-3 itens contam uma história junto que nenhum deles conta sozinho?** Se sim, **agrupe num único bullet-narrativa** com sub-bullets, em vez de espalhar.

**Regra de ouro:** se ler os bullets isolados faz alguém perder a história, agrupe.

**Critério de inclusão:**
- Decisões que poderiam ter sido diferentes (arquiteturais, de produto, editoriais)
- Restrições descobertas que afetam o projeto
- Entregáveis significativos aprovados pelo fundador
- Pivots ou mudanças de direção com contexto do porquê
- **Fechamento de lacuna estrutural ou virada de fundamento** — quando combinação de entregas tira o projeto de plano provisório/arbitrário e coloca em plano fundamentado/citável

**Não entra:** bugs corrigidos sem impacto na direção, detalhes de implementação, progresso operacional rotineiro, mudanças de infraestrutura agentic sem impacto editorial.

**Formato:**

```
## YYYY-MM-DD
- [decisão ou entregável — uma linha por item, foco no "o quê" e "por quê"]
```

### Passo 3 — Auditar `project_genesis.md` (propor, não aplicar)

`project_genesis.md` é arquivo curado — agentes confiam nele para se orientar, mudanças têm peso. **Mudanças são propostas no Passo 5, não aplicadas diretamente.** Diferente do `project_history.md` onde o command escreve direto.

**O que verificar (silenciosamente — material para o relatório):**

Para cada PR/issue **da janela incremental**, pergunte:
- **Alguma ancoragem existente foi reforçada?** (aspiracional virou fato implementado — propor reescrita densa citando PR)
- **Alguma ancoragem existente foi contradita?** (decisão na janela contradiz texto atual — propor revisão)
- **Há virada de fundamento na janela?** (identificada na auditoria narrativa do Passo 2 — propor ancoragem nova densa)

**Densidade exigida:** genesis tem poucas ancoragens, cada uma é frase densa (motivação + restrição + cita PR/issue quando faz sentido).

**Não detecta ancoragens emergentes** (padrões repetidos em todo o histórico) — isso exige varredura ampla, é escopo do `/update-memory-full`.

**Exceção de aplicação automática:** se durante a conversa **atual** o usuário aprovou explicitamente uma mudança no genesis, aplique e registre em `## Notas de evolução` com formato:

```
- **YYYY-MM-DD** — [O que mudou onde] após [PR/issue de referência]. Antes desta data, [estado anterior]; agora [estado novo].
```

Se o arquivo ainda não tem `## Notas de evolução`, crie a seção no fim antes de adicionar a entrada.

### Passo 4 — Verificar `user_profile.md`

Atualize **diretamente** apenas se houver:
- Nova parceria, advisor ou contratação
- Mudança de situação profissional (sai de sabbatical, novo trabalho, fundação de empresa)
- Mudança relevante de stack ou expertise técnica explicitada

Se nada disso aconteceu, não toque no arquivo.

### Passo 5 — Commit e push

```bash
git add .claude/memory/
git commit -m "docs(system): atualizar memória do projeto via /update-memory"
git push
```

### Passo 6 — Reportar

**Atualizações aplicadas:**
- Quantas entradas novas no `project_history.md` (com nota se houve agrupamento narrativo)
- Se `user_profile.md` foi alterado e por quê

**Auditoria do `project_genesis.md` — propostas para o usuário decidir:**

Liste em formato decisão sim/não. Nunca aplicar essas mudanças sem confirmação na conversa atual.

- **Ancoragens existentes a revisar** — para cada uma: ancoragem atual, motivo (foi reforçada / foi contradita / aspiracional virou fato), proposta de nova redação densa
- **Ancoragens novas candidatas** (apenas viradas de fundamento da janela; ancoragens emergentes ficam para o `/update-memory-full`) — para cada uma: PRs que evidenciam, proposta de redação densa
- Se nada surgiu na auditoria, declarar: "Genesis auditado na janela, nada a propor"

**Mudanças aplicadas automaticamente** (apenas o que foi aprovado na conversa atual):
- Listar a mudança no arquivo + entrada criada em `## Notas de evolução`

---

## Regras

- Janela = da última entrada do `project_history.md` até hoje (não toque em datas anteriores)
- Nunca apague entradas existentes — só adicione no topo
- Nunca reescreva o histórico — se algo foi registrado errado, adicione correção como nova entrada
- Mudanças no genesis: **propor**, não aplicar (exceto se aprovado na conversa atual)
- Se não houver nada novo para registrar, informe o usuário sem commitar
