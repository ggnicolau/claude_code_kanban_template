# Update Memory Full — Reconstrução Completa da Memória

Você é o **`project-manager`**. Este command faz **varredura completa** do projeto desde o primeiro commit e audita o `project_history.md` inteiro — não apenas adiciona o que é recente. É a diferença para `/update-memory` (incremental, só adiciona o que falta no topo).

Use `/update-memory` para atualizações incrementais regulares. Use este command quando o histórico está desatualizado por um período longo, quando suspeita que datas antigas ficaram subdocumentadas, ou periodicamente para garantir cobertura completa.

---

## ⚠️ Armadilha conhecida (não cair nela)

A tentação fácil é **ler o último cabeçalho do `project_history.md`, ver uma data recente, e processar só o período seguinte**. Isso é o que `/update-memory` faz — e este command **existe justamente para evitar esse atalho**.

Datas antigas podem estar:
- **Incompletas** — registradas, mas com poucas entradas para o que aconteceu naquele dia
- **Ausentes** — execuções anteriores pularam aquela data por completo (kickoff, agente que esqueceu, /update-memory que não rodou no dia)
- **Erradas** — entradas que descrevem mal o que aconteceu (corrigir adicionando nova entrada, nunca reescrevendo)

A varredura é **sempre desde o primeiro commit do repositório**, não desde o último cabeçalho do histórico.

---

## O que o `project-manager` faz

### Passo 1 — Mapear o estado atual da memória (não tirar conclusões)

Leia `.claude/memory/project_history.md` **integralmente** (não só o topo).

Liste todas as datas presentes e quantas entradas (bullets) cada uma tem. Exemplo de mapa interno:

```
2026-05-02 → 16 entradas
2026-05-01 → 6 entradas
2026-04-30 → 12 entradas
2026-04-29 → 14 entradas
```

**Não tire conclusões nesta etapa** — só monte o mapa. A avaliação acontece no Passo 3, comparando com o levantamento factual.

### Passo 2 — Levantar todo o histórico do projeto

Execute em paralelo (cobre **desde o primeiro commit** — não use filtros de data):

```bash
git log --oneline --reverse
```

```bash
export GH_TOKEN=$(grep GH_TOKEN .env | cut -d= -f2) && gh issue list --state closed --limit 200 --json number,title,closedAt,labels | python3 -c "
import json, sys
issues = json.load(sys.stdin)
for i in sorted(issues, key=lambda x: x['closedAt']):
    labels = ', '.join(l['name'] for l in i.get('labels', []))
    print(f\"{i['closedAt'][:10]} #{i['number']} [{labels}] {i['title']}\")
"
```

```bash
export GH_TOKEN=$(grep GH_TOKEN .env | cut -d= -f2) && gh pr list --state merged --limit 100 --json number,title,mergedAt,baseRefName | python3 -c "
import json, sys
prs = json.load(sys.stdin)
for p in sorted(prs, key=lambda x: x.get('mergedAt') or ''):
    print(f\"{(p.get('mergedAt') or '')[:10]} PR#{p['number']} -> {p['baseRefName']}: {p['title']}\")
"
```

Agrupe a saída por data para facilitar a auditoria do Passo 3.

### Passo 3 — Auditoria comparativa (passo decisivo deste command)

Para **cada data** com atividade no Passo 2, compare:

**(a) Datas presentes no `project_history.md`:**
- Conte PRs/issues fechados naquela data vs. entradas no histórico
- Se a proporção for desigual (ex: 8 PRs no dia, só 2 entradas no histórico) → **red flag**, investigar o que pode estar faltando
- Para cada PR/issue da data, decidir: já está coberto por alguma entrada? Merece nova entrada?

**(b) Datas ausentes no `project_history.md`:**
- Há PRs/issues fechados naquela data?
- Algum se enquadra nos critérios de inclusão (abaixo)? Se sim, é uma data **ausente** que precisa ser inserida — pode ser data antiga ou recente.

**Critério de seleção — o que entra no histórico:**
- Decisões que poderiam ter sido diferentes (arquiteturais, de produto, editoriais)
- Restrições descobertas que afetam o projeto (limitações de API, de canal, de métrica)
- Entregáveis significativos aprovados pelo fundador
- Pivots ou mudanças de direção com contexto do porquê
- Marcos importantes (primeira publicação real, primeiro run completo, etc.)

**O que não entra:**
- Bugs corrigidos sem impacto na direção do projeto
- Detalhes de implementação (campo X adicionado, função Y refatorada)
- Progresso operacional rotineiro de issues
- Mudanças de infraestrutura agentic (agentes, hooks, memória) sem impacto editorial — ficam no git log

### Passo 4 — Reconstruir incrementalmente, em qualquer posição

`project_history.md` é cronologicamente **reverso** — mais novo no topo, mais antigo na base. **Sempre.**

Cinco casos possíveis ao inserir:

| Caso | Situação | Onde insere |
|---|---|---|
| **A** | Data nova mais recente que o topo | Acima do topo (vira novo topo) |
| **B** | Data nova entre duas existentes | Na posição cronológica correta entre elas |
| **C** | Data nova mais antiga que a base | Abaixo da base (vira nova base) |
| **D** | Data já existe mas faltam entradas | Adicionar bullets dentro do bloco existente daquela data (no fim da lista) |
| **E** | Data antiga "esquecida" por execução anterior do `/update-memory` ou kickoff | Trata-se como B ou C — insere na posição cronológica correta, mesmo que seja "no meio do passado" |

A regra única é: **respeitar a ordem cronológica reversa, em qualquer posição** (topo, meio, base, ou dentro de um bloco existente).

**Restrições absolutas:**
- **Nunca** apagar entradas existentes — só adicionar
- **Nunca** reordenar entradas existentes
- **Nunca** reescrever uma entrada — se algo estava errado, adicione correção como nova entrada (no caso D, dentro do bloco daquela data)

**Formato obrigatório:**

```
## YYYY-MM-DD
- [decisão ou entregável — uma linha por item, foco no "o quê" e "por quê"]
```

Agrupe por data. Se múltiplos eventos relevantes ocorreram na mesma data, liste todos sob a mesma entrada.

### Passo 5 — Verificar `user_profile.md` e `project_genesis.md`

Verifique se algo no histórico (recente ou antigo, recém-descoberto) justifica atualizar:
- `user_profile.md` → nova parceria, advisor, mudança de contexto do fundador
- `project_genesis.md` → pivot de visão, nova exclusão estratégica, mudança de ancoragem

Se não houver mudança, não toque nesses arquivos.

### Passo 6 — Commit e push

```bash
git add .claude/memory/
git commit -m "docs(system): reconstruir memória completa via /update-memory-full"
git push
```

### Passo 7 — Reportar com granularidade

Informe ao usuário, separando claramente:

**Datas com inserções:**
- **Datas novas adicionadas (Casos A/B/C/E):** liste cada uma e em qual posição entrou (topo, meio, base, posição cronológica)
- **Datas existentes completadas (Caso D):** liste cada uma e quantas entradas foram adicionadas

**Datas auditadas e consideradas completas:**
- Liste as datas onde a comparação Passo 3 não revelou nada faltando — transparência sobre o trabalho de auditoria realmente feito

**Outras seções:**
- Período coberto pela varredura (data do primeiro commit até hoje)
- Se `user_profile.md` ou `project_genesis.md` foram alterados e por quê
- Se houve informação que não conseguiu classificar (para decisão do usuário)

Sem este reporte granular, fica impossível para o usuário saber se a varredura foi mesmo completa ou se foi feita só no topo.

---

## Regras

- Varredura sempre **desde o primeiro commit**, nunca desde o último cabeçalho do histórico
- Nunca apague entradas existentes — só adicione (em qualquer posição que respeite a ordem cronológica reversa)
- Nunca reordene entradas existentes
- Nunca reescreva o histórico — se algo estava errado, adicione correção como nova entrada
- Foco em decisões e entregáveis, não em progresso técnico
- Em caso de dúvida sobre incluir ou não → inclua, e sinalize ao usuário no relatório
