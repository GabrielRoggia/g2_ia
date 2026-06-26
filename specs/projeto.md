# Projeto: Caixeiro Viajante com Algoritmo Genético (TSP-GA)

## Problema

O **Problema do Caixeiro Viajante** (Travelling Salesman Problem — TSP) é um dos problemas de otimização combinatória mais estudados na ciência da computação. Dado um conjunto de N cidades e as distâncias entre elas, o objetivo é encontrar a rota mais curta que:

1. Visita cada cidade **exatamente uma vez**
2. Retorna à cidade de origem ao final

O TSP é classificado como **NP-difícil**: não existe algoritmo conhecido que resolva instâncias grandes em tempo polinomial. Para N = 20 cidades, existem (20-1)!/2 ≈ 6 × 10¹⁶ rotas possíveis — inviável por força bruta.

## Solução proposta

Implementação de um **Algoritmo Genético (AG)** que explora o espaço de soluções de forma inteligente, inspirada no processo evolutivo da natureza. O AG mantém uma população de soluções candidatas (cromossomos), que evoluem ao longo de gerações através de seleção, crossover e mutação.

## Objetivos

- Demonstrar a aplicação de IA evolutiva em um problema clássico de otimização
- Implementar todos os operadores do AG do zero, sem uso de bibliotecas prontas
- Comparar a qualidade da solução do AG contra um baseline guloso (nearest neighbor)
- Visualizar o processo de evolução e a rota final encontrada

## Escopo

**Dentro do escopo:**
- AG com representação por permutação (índices de cidades)
- Seleção por torneio, crossover OX1 (Order Crossover), mutação por inversão
- Elitismo para preservar melhores soluções
- Geração de cidades aleatórias com seed controlada
- Visualização da rota e curva de evolução
- Comparação com greedy nearest neighbor

**Fora do escopo:**
- Instâncias reais do TSP (TSPLIB)
- Interface gráfica interativa
- Otimizações como 2-opt local search
- Execução paralela / multi-thread
