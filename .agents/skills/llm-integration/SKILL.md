# Skill: LLM Integration

Padrão para integrar LLMs e construir sistemas de IA — usado pelo `ai-engineer`.

## Quando usar
Ao integrar APIs de LLM, construir agentes, RAG ou sistemas de prompting.

## Boas práticas
- Sempre usar prompt caching para reduzir custos (Anthropic SDK)
- Definir schema de input/output com Pydantic
- Implementar evals mínimos antes de ir para produção
- Logar tokens usados e latência por chamada

## Estrutura mínima de um agente
```python
from anthropic import Anthropic
from pydantic import BaseModel

client = Anthropic()

def run_agent(prompt: str, system: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
```

## Quando NÃO usar LLM
- Quando uma regex ou regra determinística resolve
- Quando latência < 100ms é requisito
