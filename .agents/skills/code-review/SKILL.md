# Skill: Code Review

Padrão de revisão de código — usado pelo `tech-lead`.

## Quando usar
Ao revisar PRs, outputs de agentes ou código submetido pelo usuário.

## Processo
1. Verificar corretude: o código faz o que promete?
2. Verificar robustez: trata erros e casos de borda?
3. Verificar manutenibilidade: legível, sem abstrações prematuras?
4. Verificar conformidade com CLAUDE.md (type hints, logging, pathlib)

## Severidade
- 🔴 Crítico — bloqueia merge (bug, segurança, dados perdidos)
- 🟡 Aviso — deve ser corrigido antes do merge
- 🔵 Sugestão — melhoria opcional

## O que NÃO fazer
- Não reescrever código que funciona só por estilo
- Não sugerir abstrações para código usado em um único lugar
