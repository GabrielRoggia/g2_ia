# Algoritmo Genético para TSP — Fundamentos Técnicos

## O que é um Algoritmo Genético

Um **Algoritmo Genético** (AG) é uma metaheurística de otimização inspirada na evolução biológica. A ideia central é manter uma **população de soluções candidatas** que evolui ao longo de gerações, guiada por um processo de seleção natural: soluções melhores têm mais chance de reproduzir, transmitindo suas características às gerações seguintes.

## Aplicação ao TSP

No contexto do TSP (Traveling Salesman Problem), cada **solução candidata** (cromossomo) representa uma **permutação das cidades**: a ordem em que o caixeiro as visita.

### Representação cromossômica

```
Cromossomo: [3, 7, 1, 5, 0, 9, 4, 2, 8, 6]
             ↑ cidade 3 é visitada primeiro
```

Propriedade fundamental: cada índice aparece **exatamente uma vez**. Qualquer operador genético deve preservar isso.

---

## Operadores Implementados

### 1. Inicialização

A população inicial é gerada com permutações aleatórias. Diversidade total no início.

```python
def _random_chromosome():
    chrom = list(range(N))
    random.shuffle(chrom)
    return chrom
```

---

### 2. Função de Fitness

Mede a qualidade de um cromossomo. Para TSP, queremos **minimizar** distância, mas o AG por padrão **maximiza** fitness — então:

```
fitness = 1 / distância_total
```

Quanto menor a distância, maior o fitness. A distância total considera o retorno à origem:

```
d(rota) = Σ dist(cidade_i, cidade_{i+1}) + dist(cidade_N, cidade_1)
```

---

### 3. Seleção por Torneio

Seleciona `k` indivíduos aleatoriamente e retorna o melhor entre eles. Com k=3:

```
torneio([chrom_5, chrom_12, chrom_38]) → melhor dos três
```

**Vantagem sobre seleção proporcional (roleta):** não sofre com diferenças extremas de fitness. Pressão seletiva ajustável via k.

---

### 4. Crossover OX1 (Order Crossover)

O operador mais eficaz para representações por permutação no TSP.

**Funcionamento:**
1. Seleciona um segmento aleatório do **Pai 1**
2. Copia esse segmento diretamente para o filho
3. Preenche o restante com os genes do **Pai 2**, na ordem em que aparecem, pulando os já presentes

**Exemplo com N=8:**
```
Pai 1:  [3, 1, 6, 2 | 5, 0, 7, 4]   (segmento: posições 4-7)
Pai 2:  [0, 5, 2, 7, 3, 4, 6, 1]

Filho:  [_, _, _, _ | 5, 0, 7, 4]   (copia segmento do Pai 1)
Pai 2 sem {5,0,7,4}: [2, 3, 6, 1]   (ordem do Pai 2)
Filho:  [2, 3, 6, 1, 5, 0, 7, 4]   ✓ permutação válida
```

**Por que OX1 e não PMX ou CX?**
OX1 preserva a **ordem relativa** das cidades de um dos pais, que é uma propriedade importante para TSP — subcaminhos eficientes tendem a manter sua ordem mesmo após crossover.

---

### 5. Mutação por Inversão de Segmento

Reverte um sub-segmento aleatório do cromossomo.

```
Antes:  [3, 1, 6, 2, 5, 0, 7, 4]
         --------
Depois: [3, 1, 0, 5, 2, 6, 7, 4]   (segmento [6,2,5,0] → [0,5,2,6])
```

**Por que inversão e não swap?**
- Swap troca duas cidades e "quebra" duas arestas
- Inversão reverte um segmento e substitui apenas as duas arestas externas
- Matematicamente: inversão é equivalente a tentar um 2-opt local, sendo assim mais eficaz para TSP

**Taxa de mutação:** 2% por padrão. Alta demais → busca aleatória. Baixa demais → convergência prematura.

---

### 6. Elitismo

Os `k` melhores indivíduos de uma geração são copiados diretamente para a próxima, sem crossover ou mutação.

**Efeito:** a melhor distância registrada nunca aumenta entre gerações (monotonicamente decrescente).

---

## Fluxo por geração

```
1. Avaliar fitness de toda a população
2. Registrar melhor distância (histórico)
3. Copiar top-k para nova população (elitismo)
4. Repetir até preencher população:
   a. Selecionar pai1 e pai2 via torneio
   b. Aplicar OX1 → filho
   c. Aplicar mutação por inversão → filho mutado
   d. Adicionar filho à nova população
5. Substituir população antiga pela nova
```

---

## Convergência esperada

Para 20 cidades, 500 gerações, população 100:
- Melhora intensa nas primeiras ~100 gerações
- Platô gradual entre gerações 100-300
- Estabilização após geração ~350

O gráfico de evolução (`results/evolution.png`) visualiza este comportamento.
