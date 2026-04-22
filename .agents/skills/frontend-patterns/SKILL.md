# Skill: Frontend Patterns

Padrão para desenvolvimento frontend — usado pelo `frontend-engineer`.

## Quando usar
Ao criar ou revisar componentes, páginas ou integrações frontend.

## Estrutura de projeto
```
src/
  components/   # componentes reutilizáveis
  pages/        # rotas/páginas
  hooks/        # custom hooks
  services/     # chamadas de API
  types/        # tipos TypeScript
```

## Boas práticas
- TypeScript em todos os arquivos
- Variáveis de ambiente para endpoints e keys (nunca hardcodar)
- Testar componentes críticos com Vitest
- Garantir acessibilidade: labels, alt text, contraste
- Validar em mobile e desktop antes de entregar

## Integração com API
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL

async function fetchData<T>(endpoint: string): Promise<T> {
  const res = await fetch(`${API_URL}/${endpoint}`)
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}
```
