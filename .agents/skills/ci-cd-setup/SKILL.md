# Skill: CI/CD Setup

Padrão para configuração de pipelines de CI/CD — usado pelo `infra-devops`.

## Quando usar
Ao criar ou atualizar workflows de GitHub Actions, Docker ou deploy.

## Estrutura padrão de workflow Python
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync
      - run: uv run ruff check .
      - run: uv run black --check .
      - run: uv run pytest
```

## Boas práticas
- Nunca hardcodar secrets — usar `${{ secrets.NAME }}`
- Todo deploy precisa de smoke test após subir
- Separar jobs de lint, test e deploy
- Usar cache de dependências para acelerar builds
