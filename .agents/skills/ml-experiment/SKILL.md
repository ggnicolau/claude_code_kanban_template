# Skill: ML Experiment

Padrão para condução de experimentos de ML — usado pelo `ml-engineer`.

## Quando usar
Ao treinar, avaliar ou comparar modelos de machine learning.

## Fluxo padrão
1. Definir baseline simples antes de modelos complexos
2. Fixar seed para reprodutibilidade
3. Registrar experimento (MLflow ou W&B) com params e métricas
4. Avaliar com métricas adequadas ao problema (não só acurácia)
5. Documentar conclusão no notebook

## Estrutura de config de experimento
```python
from dataclasses import dataclass

@dataclass
class ExperimentConfig:
    model_name: str
    learning_rate: float
    n_estimators: int
    random_state: int = 42
```

## O que sempre logar
- Versão dos dados usados
- Hiperparâmetros
- Métricas de treino e validação
- Tempo de treinamento
