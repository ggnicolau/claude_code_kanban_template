# Sync Master

Sincroniza a **camada universal** entre os 3 templates irmãos. Use quando atualizar qualquer arquivo de infraestrutura compartilhada — hooks, settings, wizard, new_repo.py, .gitattributes, meta/, mkdocs.yml estrutural.

**Uso:** `/sync-master` (roda a partir do template atual, propaga para os outros dois)

Os templates irmãos são resolvidos relativamente ao diretório pai (`../`):
- `../claude-code-enterprise-template`
- `../claude-code-social-sciences-template`
- `../claude-code-health-template`

> **Este comando só sincroniza entre templates irmãos.** Para sincronizar template → filhos use `/sync-to-projects`. Para filho → template use `/sync-to-template`.

---

## Arquivos universais (fonte de verdade: template atual)

| Arquivo | Observação |
|---|---|
| `scripts/hooks/session_start.sh` | Idêntico nos 3 |
| `scripts/hooks/post_write.sh` | Idêntico nos 3 |
| `.claude/settings.json` | Idêntico nos 3 |
| `.claude/agents/template-coordinator.md` | Estrutura idêntica, só nome do template difere |
| `.claude/commands/sync-master.md` | Este arquivo |
| `.claude/commands/wizard.md` | Idêntico nos 3 |
| `scripts/new_repo.py` | Idêntico nos 3 |
| `.gitattributes` | Idêntico nos 3 |
| `scripts/templates/.gitattributes` | Idêntico nos 3 |
| `pyproject.toml` | Idêntico nos 3 (exceto campos de projeto filho) |
| `meta/commands_native.md` | Idêntico nos 3 |
| `meta/commands_proposed.md` | Idêntico nos 3 |
| `meta/features_index.md` | Idêntico nos 3 |
| `meta/features_report.md` | Idêntico nos 3 |
| `meta/commands_framework.xlsx` | Idêntico nos 3 |
| `mkdocs.yml` (seções estruturais) | theme, plugins, markdown_extensions + chaves de 1º nível do nav |

**Arquivos que NÃO sincronizam (domain-specific):**
- `CLAUDE.md`, `AGENTS.md`, `README.md` — linguagem de domínio
- `scripts/templates/**` — agentes, commands e templates do filho
- `docs-site/**` — conteúdo do MkDocs
- `mkdocs.yml` → `site_name`, `nav` (subseções), `theme.palette`
- `.github/workflows/setup-kanban.yml` — épicos e labels são domain-specific
- `.agents/skills/**` — skills podem variar por template

---

## Processo obrigatório

### Passo 1 — Identificar templates irmãos

Detecte qual template está ativo (pelo nome do diretório atual). Os outros dois são os alvos.
Verifique se os diretórios existem em `../` — se não existirem, informe e encerre.

### Passo 2 — Mapear diferenças

Para cada template irmão, compare arquivo por arquivo da lista universal acima.

**Para `template-coordinator.md`:** compare ignorando a linha do nome do template (é intencional ser diferente).

**Para `mkdocs.yml`:** compare apenas as seções `theme` (exceto `palette`), `plugins` e `markdown_extensions`, e as chaves de primeiro nível do `nav` (não os valores nem subseções).

**Para cada arquivo, classifique:**
- `DESATUALIZADO` — existe nos dois mas conteúdo difere
- `OK` — idêntico (ignorar)
- `AUSENTE` — existe no atual mas não no irmão

### Passo 3 — Reportar

```
📁 <template-irmão>
  DESATUALIZADO  scripts/hooks/session_start.sh
  DESATUALIZADO  mkdocs.yml (theme.features)
  AUSENTE        meta/commands_native.md
  OK             (8 arquivos idênticos)
```

Se tudo OK, informe e encerre.

### Passo 4 — Confirmar antes de agir

```
Deseja sincronizar os arquivos DESATUALIZADO e AUSENTE acima?
```

Aguarde confirmação explícita antes de prosseguir.

### Passo 5 — Sincronizar

Crie um branch no template irmão e copie os arquivos:

```bash
cd ../<template-irmão>
git checkout -b sync/master-YYYY-MM-DD
```

Para cada arquivo DESATUALIZADO ou AUSENTE:
- Copie diretamente, exceto `template-coordinator.md` e `mkdocs.yml`
- `template-coordinator.md`: copie preservando a linha do nome do template irmão
- `mkdocs.yml`: aplique só as seções universais (theme exceto palette, plugins, markdown_extensions, chaves de 1º nível do nav)

```bash
git add .
git commit -m "chore(system): sync universal layer from <template-origem>"
git push -u origin sync/master-YYYY-MM-DD
gh pr create --base dev --title "chore(system): sync universal layer from <template-origem>" --body "Sincronização automática via /sync-master."
gh pr merge --merge --delete-branch
git checkout dev && git pull
```

### Passo 6 — Reportar resultado

```
✅ <template-irmão> — X arquivos sincronizados
   ~ scripts/hooks/session_start.sh
   + meta/commands_native.md

Mergiado em dev. Aguardando confirmação para promover para main.
```

---

## Regras

- Nunca sincronizar arquivos domain-specific — só os listados na tabela universal
- Sempre criar branch + PR no irmão — nunca commitar direto
- `main` só quando o usuário pedir explicitamente após o merge em `dev`
- Para `template-coordinator.md`: preservar nome do template irmão na linha de identificação
- Para `mkdocs.yml`: merge seletivo — nunca sobrescrever `site_name`, `theme.palette`, `nav`
- Se um template irmão não existir localmente, informar e pular — não é erro fatal

$ARGUMENTS
