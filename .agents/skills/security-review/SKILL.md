# Skill: Security Review

Padrão para revisão de segurança — usado pelo `security-auditor`.

## Quando usar
Ao revisar código, infra ou configurações em busca de vulnerabilidades.

## Checklist base
- [ ] Secrets e credenciais hardcodados?
- [ ] Inputs de usuário validados e sanitizados?
- [ ] SQL injection, XSS ou command injection possíveis?
- [ ] Dependências com CVEs conhecidos?
- [ ] Permissões mínimas configuradas (IAM, tokens)?
- [ ] Dados sensíveis logados indevidamente?

## Severidade
- 🔴 Crítico — exploração imediata possível (ex: secret exposto)
- 🟠 Alto — risco real mas requer condição específica
- 🟡 Médio — boa prática não seguida
- 🔵 Info — observação sem risco imediato

## O que NÃO fazer
- Não aprovar deploy com 🔴 em aberto
- Não sugerir segurança que bloqueia desenvolvimento sem justificativa clara
