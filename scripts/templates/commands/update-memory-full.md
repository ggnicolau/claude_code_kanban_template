# Update Memory Full — Reconstrução Completa da Memória

Você é o **`project-manager`**. Este command é para quando `project_history.md` está vazio ou muito defasado — reconstrói o histórico completo desde o início do projeto.

Use `/update-memory` para atualizações incrementais regulares. Use este command apenas quando o histórico está desatualizado por um período longo (semanas ou mais).

---

## O que o `project-manager` faz

### Passo 1 — Avaliar o estado atual da memória

Leia `.claude/memory/project_history.md` para identificar até onde o histórico está registrado.

### Passo 2 — Levantar todo o histórico do projeto

Execute em paralelo:

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
    print(f\"{(p.get('mergedAt') or '')[:10]} PR#{p['number']} → {p['baseRefName']}: {p['title']}\")
"
```

### Passo 3 — Reconstruir `project_history.md`

Com base no levantamento, reconstrua o histórico completo. **Não apague o que já está no arquivo** — somente adicione entradas que ainda não existem.

**Critério de seleção — o que entra:**
- Decisões que poderiam ter sido diferentes (arquiteturais, de produto, editoriais)
- Restrições descobertas que afetam o projeto (limitações de API, de canal, de métrica)
- Entregáveis significativos aprovados pelo fundador
- Pivots ou mudanças de direção com contexto do porquê
- Marcos importantes (primeira publicação real, primeiro run completo, etc.)

**O que não entra:**
- Bugs corrigidos sem impacto na direção do projeto
- Detalhes de implementação (campo X adicionado, função Y refatorada)
- Progresso operacional rotineiro de issues
- Mudanças de infraestrutura agentic (agentes, hooks, memória) — ficam no git log

**Formato obrigatório** — adicione cada data nova **acima** das existentes:

```
## YYYY-MM-DD
- [decisão ou entregável — uma linha por item, foco no "o quê" e "por quê"]
```

Agrupe por data. Se múltiplos eventos relevantes ocorreram na mesma data, liste todos sob a mesma entrada.

### Passo 4 — Verificar `user_profile.md` e `project_genesis.md`

Verifique se algo no histórico justifica atualizar:
- `user_profile.md` → nova parceria, advisor, mudança de contexto do fundador
- `project_genesis.md` → pivot de visão, nova exclusão estratégica, mudança de ancoragem

Se não houver mudança, não toque nesses arquivos.

### Passo 5 — Commit e push

```bash
git add .claude/memory/
git commit -m "docs(system): reconstruir memória completa via /update-memory-full"
git push
```

### Passo 6 — Reportar

Informe ao usuário:
- Quantas entradas novas foram adicionadas ao `project_history.md`
- Período coberto (de quando até quando)
- Se `user_profile.md` ou `project_genesis.md` foram alterados e por quê
- Se houve informação que não conseguiu classificar (para decisão do usuário)

---

## Regras

- Nunca apague entradas existentes — só adicione acima
- Nunca reescreva o histórico — se algo estava errado, adicione correção como nova entrada
- Foco em decisões e entregáveis, não em progresso técnico
- Em caso de dúvida sobre incluir ou não → inclua, e sinalize ao usuário
