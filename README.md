# TSP-GA — Caixeiro Viajante com Algoritmo Genético

Solução do **Problema do Caixeiro Viajante (TSP)** usando um **Algoritmo Genético** implementado do zero em Python.

Desenvolvido como projeto da disciplina de Inteligência Artificial — Faculdade Antonio Meneghetti (AMF), 2026/01.

---

## O problema

Dado um conjunto de N cidades com coordenadas 2D, encontrar a rota que visita cada cidade exatamente uma vez e retorna à origem, minimizando a distância total percorrida.

O TSP é NP-difícil: para 20 cidades existem mais de 60 quadrilhões de rotas possíveis. O Algoritmo Genético encontra soluções de boa qualidade em tempo polinomial.

---

## Como rodar

### Instalação
```bash
pip install -r requirements.txt
```

### Executar o AG
```bash
# Execução padrão: 20 cidades, 500 gerações, população 100
python -m src.main

# Com gráficos salvos em results/
python -m src.main --save

# Configuração customizada
python -m src.main --cities 30 --generations 1000 --population 150 --mutation 0.03 --seed 7 --save
```

### Rodar os testes
```bash
pytest tests/ -v
```

### Rodar avaliação de performance
```bash
python evals/eval_performance.py
```

---

## Estrutura do projeto

```
├── CLAUDE.md                    # Mapa do projeto para IA
├── README.md
├── requirements.txt
├── specs/
│   ├── projeto.md               # Descrição do problema e objetivos
│   ├── requisitos.md            # Requisitos funcionais e não-funcionais
│   └── criterios-aceite.md      # Critérios testáveis de aceitação (CA01–CA10)
├── .claude/
│   ├── context.md               # Contexto técnico para IA
│   ├── prompts.md               # Histórico de prompts usados
│   ├── agents/avaliador-rota/   # Agente avaliador de qualidade de rota
│   └── skills/otimizador-genetico/  # Skill de parametrização do AG
├── src/
│   ├── city.py                  # Classe City, distância euclidiana, geração de instâncias
│   ├── genetic_algorithm.py     # Operadores genéticos + classe GeneticAlgorithm
│   ├── visualization.py         # Gráficos de rota e evolução
│   └── main.py                  # CLI entry point
├── tests/
│   ├── test_city.py             # Testes de City e distância
│   └── test_ga.py               # Testes de operadores genéticos (CA01–CA03, CA07–CA08)
├── evals/
│   └── eval_performance.py      # Avaliação CA05, CA06, CA10
└── docs/
    ├── algoritmo-genetico.md    # Teoria dos operadores implementados
    └── decisoes-tecnicas.md     # Justificativas das decisões de design
```

---

## Algoritmo

| Componente | Implementação |
|-----------|---------------|
| Representação | Permutação de índices de cidades |
| Seleção | Torneio (k=3) |
| Crossover | OX1 — Order Crossover |
| Mutação | Inversão de segmento |
| Elitismo | Top-5 preservados por geração |
| Fitness | 1 / distância_total |

Detalhes teóricos: [docs/algoritmo-genetico.md](docs/algoritmo-genetico.md)  
Decisões de design: [docs/decisoes-tecnicas.md](docs/decisoes-tecnicas.md)

---

## Critérios de aceite

Definidos em [specs/criterios-aceite.md](specs/criterios-aceite.md). Os principais:

- **CA01–CA03:** Operadores genéticos produzem permutações válidas
- **CA05:** AG melhora a distância nas primeiras 100 gerações
- **CA06:** Resultado do AG é ≤ 120% da distância do greedy nearest neighbor
- **CA07:** Execuções com a mesma seed produzem resultados idênticos
- **CA10:** Execução completa em menos de 30 segundos (20 cidades, 500 gerações)

---

## Exemplo de saída

```
=== TSP com Algoritmo Genético ===
Cidades: 20 | Geração: 500 | Pop: 100

Baseline greedy (nearest neighbor): 387.42
Melhor rota AG:                     352.18
Razão AG / Greedy:                  0.909 (OK)
Tempo de execução:                  2.3s
```
