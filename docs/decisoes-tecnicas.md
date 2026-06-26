# Decisões Técnicas — TSP-GA

Registro das principais decisões de design e justificativas. Leitura recomendada antes de modificar qualquer operador genético.

---

## DT01 — Python puro sem frameworks de AG

**Decisão:** Implementar todos os operadores manualmente, sem usar DEAP, PyGAD ou similares.

**Justificativa:** O enunciado do trabalho requer demonstração de entendimento técnico. Usar uma biblioteca de AG entregaria a solução sem compreensão dos operadores. Além disso, para este escopo (TSP com até ~50 cidades), não há necessidade de performance de framework.

---

## DT02 — Crossover OX1 em vez de PMX ou CX

**Decisão:** Order Crossover (OX1) como operador de recombinação.

**Alternativas consideradas:**
- **PMX (Partially Mapped Crossover):** preserva posição absoluta dos genes. Menos adequado para TSP onde a ordem relativa importa mais que a posição.
- **CX (Cycle Crossover):** preserva posição de todos os genes. Muito conservador, reduz diversidade.
- **OX1 (Order Crossover):** preserva a **ordem relativa** dos genes de um dos pais. Ideal para TSP, onde sub-rotas eficientes mantêm suas cidades em sequência mesmo após recombinação.

**Referência:** Davis, L. (1985). Applying adaptive algorithms to epistatic domains.

---

## DT03 — Mutação por inversão em vez de swap

**Decisão:** Inversion mutation (inversão de segmento) como operador de mutação.

**Alternativas consideradas:**
- **Swap:** troca dois genes de posição. Quebra duas arestas mas não as reconstrói de forma inteligente.
- **Insertion:** remove um gene e o insere em outra posição. Eficaz mas mais agressivo.
- **Inversão:** reverte um segmento. Equivale a testar uma melhoria 2-opt local — as arestas externas ao segmento são mantidas, apenas as internas são reordenadas.

**Por que inversão vence para TSP:** ao reverter um segmento, o operador está implicitamente tentando melhorar a sub-rota local, o que converge mais rápido que perturbações aleatórias.

---

## DT04 — `random.Random` isolado em vez de `random` global

**Decisão:** Cada instância de `GeneticAlgorithm` usa seu próprio `random.Random(seed)`. Funções que precisam de RNG recebem o objeto por parâmetro.

**Justificativa:** Ao usar o módulo `random` global, operações externas (outros testes, imports) poderiam alterar o estado do RNG e quebrar reprodutibilidade. Com `random.Random` isolado, cada execução com a mesma seed é 100% determinística independente do ambiente.

---

## DT05 — Elitismo com k=5 como padrão

**Decisão:** 5 elites preservados por geração.

**Raciocínio:** Para população de 100, manter 5 elites (5%) é conservador o suficiente para não perder boas soluções, mas não tão dominante a ponto de reduzir diversidade. Valores de k=1 são muito frágeis; k=20 reduz pressão de seleção excessivamente.

---

## DT06 — matplotlib com backend Agg

**Decisão:** `matplotlib.use("Agg")` em `visualization.py`.

**Justificativa:** Permite gerar e salvar gráficos em ambientes sem display (servidores, CI). Sem isso, matplotlib tenta abrir uma janela e falha em ambientes headless. O backend Agg renderiza para arquivo diretamente.

---

## DT07 — Sem numpy como dependência obrigatória

**Decisão:** Cálculos com `math` padrão do Python.

**Justificativa:** Para instâncias de até ~100 cidades, a diferença de performance entre `math.sqrt` e `numpy` é negligível. Reduzir dependências externas torna o projeto mais portável e fácil de instalar. numpy está em `requirements.txt` como opcional apenas para uso futuro.
