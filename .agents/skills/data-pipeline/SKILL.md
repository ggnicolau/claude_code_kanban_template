# Skill: Data Pipeline

Padrão para construção de pipelines de dados — usado pelo `data-engineer`.

## Quando usar
Ao projetar ou implementar ETL/ELT, ingestão ou transformação de dados.

## Estrutura padrão
```
src/
  ingestion/    # leitura de fontes externas
  transform/    # limpeza e transformação
  load/         # escrita no destino
  validation/   # contratos e qualidade
```

## Boas práticas
- Separar ingestão, transformação e carga em etapas independentes
- Validar schema na entrada e na saída de cada etapa
- Usar `pathlib.Path` para todos os paths
- Logar volume de registros processados em cada etapa
- Nunca commitar dados brutos — usar `.gitignore`

## Exemplo de validação
```python
def validate_schema(df: pd.DataFrame, required_cols: list[str]) -> None:
    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Colunas faltando: {missing}")
```
