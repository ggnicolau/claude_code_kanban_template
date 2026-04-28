# Claude Code Enterprise Template — Equipe

Este repositório é a **fábrica de projetos enterprise**. Os agentes aqui são os do template pai — não os dos projetos filhos.

## Agentes do template pai (`.claude/agents/`)

| Agente | Papel |
|---|---|
| `template-coordinator` | Ponto de entrada — orienta o uso dos commands, coordena melhorias no template |
| `tech-lead` | Revisão técnica de PRs no próprio template |

## Commands do template pai

| Command | Propósito |
|---|---|
| `/wizard` | Criar novo projeto filho enterprise |
| `/sync-to-projects` | Propagar mudanças do template para projetos filhos |
| `/sync-to-template` | Trazer melhorias de um filho de volta ao template |
| `/sync-master` | Sincronizar camada universal com templates irmãos |

## Como criar um projeto filho

Use o `/wizard` em uma conversa nova **neste repositório**.
