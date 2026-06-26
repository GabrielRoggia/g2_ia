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

# Com gráficos da rota final e curva de evolução salvos em results/
python -m src.main --save

# Configuração customizada
python -m src.main --cities 30 --generations 1000 --population 150 --mutation 0.03 --seed 7 --save
```

### Visualizar população geração a geração

A flag `--show-pop N` exibe a população completa ordenada do pior ao melhor indivíduo a cada N gerações e salva os gráficos em subpastas dentro de `results/`:

```bash
# Mostrar e salvar gráficos a cada geração
python -m src.main --cities 10 --population 15 --generations 3 --show-pop 1

# Mostrar a cada 100 gerações (parâmetros padrão)
python -m src.main --show-pop 100
```

Para cada geração exibida são gerados os seguintes arquivos em `results/gen_XXXX/`:

| Arquivo | Conteúdo |
|---|---|
| `populacao_barras.png` | Barras de todos os indivíduos (vermelho = descartado, verde = elite preservada) |
| `rota_01_PIOR_distXXX.png` | Rota do pior indivíduo da geração |
| `rota_02_02_distXXX.png` ... | Indivíduos intermediários em ordem crescente de qualidade |
| `rota_N_MELHOR_elite_distXXX.png` | Rota do melhor indivíduo da geração |

O sufixo `_elite` indica que o indivíduo será copiado intacto para a próxima geração (elitismo).

### Salvar gráfico da melhor rota por geração

A flag `--show-best N` salva o gráfico da melhor rota a cada N gerações em `results/best/`, e automaticamente também gera `results/route.png` e `results/evolution.png` ao final:

```bash
# Salvar melhor rota a cada geração
python -m src.main --show-best 1

# Salvar a cada 50 gerações (parâmetros padrão)
python -m src.main --show-best 50
```

Os arquivos gerados em `results/best/` têm o nome `gen_XXXX_distYYY.png`, onde `XXXX` é o número da geração e `YYY` é a distância da melhor rota naquele momento. Abrindo as imagens em sequência é possível ver a rota evoluindo — nas primeiras gerações há muitos cruzamentos, e nas últimas as linhas ficam mais organizadas.

As flags podem ser combinadas:

```bash
# Melhor rota por geração + população completa a cada 5 + gráficos finais
python -m src.main --show-best 1 --show-pop 5
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

## Parâmetros disponíveis

| Parâmetro | Padrão | Descrição |
|---|---|---|
| `--cities N` | 20 | Número de cidades no mapa |
| `--population N` | 100 | Tamanho da população por geração |
| `--generations N` | 500 | Número de gerações |
| `--mutation F` | 0.02 | Taxa de mutação (0.0 a 1.0) |
| `--elitism N` | 5 | Quantos melhores indivíduos são preservados por geração |
| `--seed N` | 42 | Seed aleatória para reprodutibilidade |
| `--save` | — | Salva `results/route.png` e `results/evolution.png` |
| `--show-pop N` | — | Salva população completa (barras + rota de cada indivíduo) a cada N gerações em `results/gen_XXXX/` |
| `--show-best N` | — | Salva gráfico da melhor rota a cada N gerações em `results/best/` + gráficos finais |

---

## Exemplo com todas as opções

```bash
python -m src.main \
  --cities 20 \
  --population 100 \
  --generations 500 \
  --mutation 0.02 \
  --elitism 5 \
  --seed 42 \
  --save \
  --show-best 50 \
  --show-pop 100
```

O que este comando gera:

```
results/
├── route.png                     # melhor rota final (--save / --show-best)
├── evolution.png                 # curva de distância por geração (--save / --show-best)
├── best/
│   ├── gen_0050_dist399.png      # melhor rota na geração 50  (--show-best 50)
│   ├── gen_0100_dist371.png      # melhor rota na geração 100
│   ├── gen_0150_dist358.png
│   ├── ...
│   └── gen_0500_dist352.png      # melhor rota na geração 500
├── gen_0100/                     # população completa na geração 100 (--show-pop 100)
│   ├── populacao_barras.png
│   ├── rota_01_PIOR_distXXX.png
│   ├── ...
│   └── rota_100_MELHOR_elite_distXXX.png
├── gen_0200/
├── gen_0300/
├── gen_0400/
└── gen_0500/
```

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
