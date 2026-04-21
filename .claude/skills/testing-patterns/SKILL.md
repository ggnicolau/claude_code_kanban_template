# Skill: Testing Patterns

Padrões de teste para projetos Python.

## Quando usar
Ao escrever ou revisar testes para funções, pipelines ou integrações.

## Padrões preferidos

### Estrutura
- Separar testes unitários (função isolada) de testes de integração (fluxo completo)
- Dados de teste em `tests/fixtures/` como arquivos, não inline no código
- Usar `pytest.fixture` com `scope="session"` para recursos caros de inicializar

### Cobertura
- Cobrir: input vazio, input inválido, valores limite
- Testes de regressão para bugs corrigidos

## Exemplo
```python
@pytest.fixture(scope="session")
def db_conn():
    return create_connection(":memory:")

def test_insert_returns_id(db_conn):
    result = insert_record(db_conn, {"name": "test"})
    assert result.id is not None
```
