# Wizard — Criar Novo Repositório

Colete as informações abaixo perguntando uma de cada vez, com opções numeradas quando aplicável:

1. **Nome do repositório** — texto livre
2. **Visibilidade**
   - 1. Privado
   - 2. Público
3. **Instalar skills Caveman?** (~75% menos tokens)
   - 1. Sim
   - 2. Não

Com as respostas, execute:

```bash
python scripts/new_repo.py --name <nome> --visibility <private|public> --yes [--caveman | --skip-caveman]
```

$ARGUMENTS
