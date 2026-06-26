# Guia de Uso — TSP-GA

## Pré-requisitos

```bash
# Criar e ativar o ambiente virtual (apenas na primeira vez)
python3 -m venv .venv

# Instalar dependências
.venv/bin/pip install -r requirements.txt
```

---

## Comandos disponíveis

### 1. Execução básica

Roda o algoritmo com os parâmetros padrão (20 cidades, 500 gerações, população 100):

```bash
.venv/bin/python -m src.main
```

Saída esperada:

```
=== TSP com Algoritmo Genético ===
Cidades: 20 | Geração: 500 | Pop: 100

Baseline greedy (nearest neighbor): 460.51
Melhor rota AG:                     352.32
Razão AG / Greedy:                  0.765 (OK)
Tempo de execução:                  1.1s
```

---

### 2. Salvar gráficos da rota e evolução

A flag `--save` gera dois arquivos em `results/`:

```bash
.venv/bin/python -m src.main --save
```

| Arquivo gerado | O que mostra |
|---|---|
| `results/route.png` | Mapa com as cidades e a melhor rota encontrada |
| `results/evolution.png` | Curva da melhor distância ao longo das gerações |

---

### 3. Visualizar população geração a geração

A flag `--show-pop N` exibe a população completa (do pior ao melhor indivíduo) **a cada N gerações** e salva gráficos organizados por subpasta.

```bash
.venv/bin/python -m src.main --show-pop 1
```

Para cada geração exibida são gerados os seguintes arquivos dentro de `results/gen_XXXX/`:

| Arquivo | O que mostra |
|---|---|
| `populacao_barras.png` | Gráfico de barras de todos os indivíduos ordenados do pior ao melhor. Barras vermelhas serão descartados; barras verdes são a elite preservada. |
| `rota_01_PIOR_distXXX.png` | Rota do pior indivíduo da geração |
| `rota_02_02_distXXX.png` ... | Indivíduos intermediários em ordem crescente de qualidade |
| `rota_15_MELHOR_elite_distXXX.png` | Rota do melhor indivíduo (marcado com `_elite` se for preservado) |

O sufixo `_elite` no nome do arquivo indica que aquele indivíduo será copiado intacto para a próxima geração (elitismo).

---

### 4. Exemplos práticos por objetivo

#### Ver a evolução a cada 100 gerações (parâmetros padrão)
```bash
.venv/bin/python -m src.main --show-pop 100
```
Gera subpastas `results/gen_0100/`, `results/gen_0200/`, ..., `results/gen_0500/`.

#### Experimento com poucos indivíduos para estudar o algoritmo
```bash
.venv/bin/python -m src.main --cities 10 --population 15 --generations 3 --show-pop 1 --seed 42
```
Gera gráficos para **todas** as 3 gerações com apenas 15 indivíduos — bom para visualizar o efeito do crossover e mutação.

#### Problema maior com gráfico final
```bash
.venv/bin/python -m src.main --cities 30 --generations 1000 --population 200 --save
```

#### Reproduzir exatamente a mesma execução
```bash
.venv/bin/python -m src.main --seed 42
```
A flag `--seed` garante que os resultados sejam idênticos entre execuções.

---

### 5. Todos os parâmetros disponíveis

| Parâmetro | Padrão | Descrição |
|---|---|---|
| `--cities N` | 20 | Número de cidades no mapa |
| `--population N` | 100 | Tamanho da população por geração |
| `--generations N` | 500 | Número de gerações que o AG vai executar |
| `--mutation F` | 0.02 | Taxa de mutação (0.0 a 1.0) |
| `--elitism N` | 5 | Quantos melhores indivíduos são preservados por geração |
| `--seed N` | 42 | Seed aleatória para reprodutibilidade |
| `--save` | — | Salva `results/route.png` e `results/evolution.png` |
| `--show-pop N` | — | Exibe e salva a população completa a cada N gerações |

---

### 6. Testes e avaliação

#### Rodar todos os testes unitários
```bash
.venv/bin/pytest tests/ -v
```

Testa cada operador genético isoladamente (crossover, mutação, seleção, fitness) e verifica os critérios de aceite CA01 a CA08.

#### Rodar a avaliação de performance
```bash
.venv/bin/python evals/eval_performance.py
```

Valida os critérios CA05 (melhora em 100 gerações), CA06 (AG ≤ 120% do greedy) e CA10 (tempo < 30s), imprimindo um relatório com veredicto final.

---

### 7. Estrutura de saída gerada

Após rodar com `--save` e `--show-pop`, a pasta `results/` terá a seguinte estrutura:

```
results/
├── route.png                  # melhor rota final (com --save)
├── evolution.png              # curva de evolução (com --save)
├── gen_0001/                  # geração 1 (com --show-pop 1)
│   ├── populacao_barras.png
│   ├── rota_01_PIOR_dist586.png
│   ├── rota_02_02_dist581.png
│   ├── ...
│   └── rota_15_MELHOR_elite_dist415.png
├── gen_0002/
│   └── ...
└── gen_0003/
    └── ...
```
