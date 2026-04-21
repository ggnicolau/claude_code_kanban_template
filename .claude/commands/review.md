# Review Orquestrado

Dispare os dois subagentes abaixo em paralelo (numa única chamada com dois Agent tool calls simultâneos):

1. **code-reviewer** — revisão de corretude, tipos, padrões e testes
2. **security-auditor** — varredura de segurança e exposição de dados

Após ambos retornarem, consolide os resultados num único relatório com severidade unificada:
🔴 Crítico | 🟡 Aviso | 🔵 Sugestão

$ARGUMENTS
