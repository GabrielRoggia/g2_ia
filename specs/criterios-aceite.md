# Critérios de Aceite — TSP-GA

Cada critério é verificável de forma objetiva. A solução é considerada aceita quando **todos** os critérios abaixo forem satisfeitos.

## CA01 — Validade da rota
**Dado** qualquer cromossomo produzido pelo AG,  
**quando** verificado,  
**então** ele deve conter cada índice de cidade exatamente uma vez (permutação válida).  
**Verificação:** `tests/test_ga.py::test_chromosome_is_valid_permutation`

## CA02 — Preservação de genes no crossover OX1
**Dado** dois pais com N cidades,  
**quando** aplicado o crossover OX1,  
**então** o filho deve conter todos os N índices de cidades exatamente uma vez.  
**Verificação:** `tests/test_ga.py::test_order_crossover_validity`

## CA03 — Preservação de genes na mutação
**Dado** um cromossomo válido,  
**quando** aplicada a mutação por inversão,  
**então** o resultado deve conter os mesmos genes (mesma quantidade, possivelmente em ordem diferente).  
**Verificação:** `tests/test_ga.py::test_inversion_mutation_preserves_genes`

## CA04 — Simetria do cálculo de distância
**Dado** duas cidades A e B,  
**quando** calculada a distância,  
**então** `distance(A, B) == distance(B, A)` e `distance(A, A) == 0`.  
**Verificação:** `tests/test_city.py::test_distance_symmetry`

## CA05 — Melhoria ao longo das gerações
**Dado** o histórico de melhores distâncias do AG,  
**quando** analisadas as primeiras 100 gerações,  
**então** a distância na geração 100 deve ser estritamente menor que na geração 1.  
**Verificação:** `evals/eval_performance.py` — campo `improved_in_100_gens`

## CA06 — Qualidade vs baseline greedy
**Dado** uma instância de 20 cidades com seed=42,  
**quando** comparado o resultado do AG (500 gerações, pop=100) com o greedy nearest neighbor,  
**então** a distância do AG deve ser ≤ 120% da distância do greedy (no máximo 20% pior).  
**Verificação:** `evals/eval_performance.py` — campo `ratio_ag_vs_greedy ≤ 1.20`

## CA07 — Reprodutibilidade
**Dado** a mesma seed e parâmetros,  
**quando** o AG é executado duas vezes,  
**então** a melhor distância final deve ser idêntica.  
**Verificação:** `tests/test_ga.py::test_reproducibility`

## CA08 — Geração de gráficos
**Dado** a flag `--save` ativa,  
**quando** o programa é executado,  
**então** os arquivos `results/route.png` e `results/evolution.png` devem ser criados e ter tamanho > 0 bytes.  
**Verificação:** verificação manual ou `tests/test_ga.py::test_visualization_saves_files`

## CA09 — Todos os testes unitários passam
**Quando** executado `pytest tests/ -v`,  
**então** todos os testes devem ter status PASSED com 0 falhas.  
**Verificação:** `pytest tests/`

## CA10 — Tempo de execução
**Dado** 20 cidades, 500 gerações, população 100,  
**quando** executado,  
**então** o tempo total deve ser < 30 segundos.  
**Verificação:** `evals/eval_performance.py` — campo `elapsed_seconds < 30`
