# Contexto Técnico — TSP-GA

## Stack
- **Linguagem:** Python 3.10+
- **Visualização:** matplotlib 3.7+
- **Testes:** pytest 7.4+
- **Sem dependências de ML** (numpy é opcional, math padrão é suficiente)

## Estrutura de módulos

```
src/
├── __init__.py
├── city.py            # City dataclass, distância euclidiana, geração de instâncias
├── genetic_algorithm.py  # Operadores genéticos + classe GeneticAlgorithm
├── visualization.py   # plot_route(), plot_evolution()
└── main.py            # CLI entry point (argparse)
```

## Decisões de design relevantes

### Representação cromossômica
Cromossomo = `list[int]` — permutação de índices de cidades `[0, N-1]`. Garante que cada cidade aparece exatamente uma vez. Sem necessidade de decodificação.

### Operador de crossover: OX1 (Order Crossover)
Escolhido por preservar a ordem relativa dos genes, propriedade crucial para TSP. Detalhes em `docs/decisoes-tecnicas.md`.

### Operador de mutação: Inversão de segmento
Inverte um segmento aleatório do cromossomo. Mais eficaz que swap simples para TSP pois reorganiza sub-rotas preservando adjacências.

### Seleção: Torneio
k=3 por padrão. Pressão seletiva controlável sem necessidade de ranking global.

### Elitismo
Top-5 indivíduos preservados por geração. Evita regressão — a melhor solução nunca piora.

## Convenções de código
- Funções puras para operadores genéticos (recebem e retornam, sem estado)
- `GeneticAlgorithm` é a única classe stateful — mantém `self.history`
- Type hints em todas as funções públicas
- Seed controlada via `random.seed()` no início de `main()` e nos testes

## Como os testes funcionam
- `tests/test_city.py` — testa City, distância euclidiana, geração de cidades
- `tests/test_ga.py` — testa cada operador isoladamente + reprodutibilidade
- `evals/eval_performance.py` — script de avaliação que imprime métricas e valida CA05, CA06, CA10
