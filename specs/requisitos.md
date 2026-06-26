# Requisitos do Projeto TSP-GA

## Requisitos Funcionais

### RF01 — Geração de instâncias
O sistema deve gerar um conjunto de N cidades com coordenadas (x, y) aleatórias dentro de um espaço 2D configurável, com seed reproduzível.

### RF02 — Representação cromossômica
Cada solução (cromossomo) deve ser representada como uma permutação dos índices das cidades, garantindo que cada cidade apareça exatamente uma vez.

### RF03 — Cálculo de fitness
O sistema deve calcular a distância total de uma rota (soma das distâncias euclidianas consecutivas, incluindo retorno à origem) e derivar o fitness como inverso da distância.

### RF04 — Inicialização da população
O AG deve inicializar a população com cromossomos gerados aleatoriamente (permutações aleatórias).

### RF05 — Seleção por torneio
O sistema deve selecionar pais usando seleção por torneio com parâmetro k configurável.

### RF06 — Crossover OX1 (Order Crossover)
O sistema deve implementar o operador de crossover OX1, que preserva a ordem relativa dos genes de um dos pais enquanto herda um segmento contíguo do outro.

### RF07 — Mutação por inversão
O sistema deve aplicar mutação com taxa configurável, invertendo um segmento aleatório do cromossomo.

### RF08 — Elitismo
O sistema deve preservar os N melhores indivíduos de uma geração para a próxima, sem alteração.

### RF09 — Execução por gerações
O AG deve executar por um número configurável de gerações, registrando a melhor distância de cada geração.

### RF10 — Visualização de rota
O sistema deve gerar um gráfico mostrando as cidades e a melhor rota encontrada.

### RF11 — Visualização de evolução
O sistema deve gerar um gráfico da evolução da melhor distância ao longo das gerações.

### RF12 — Baseline de comparação
O sistema deve implementar um algoritmo greedy (nearest neighbor) para comparação de qualidade.

### RF13 — Interface de linha de comando
O sistema deve aceitar parâmetros via CLI: número de cidades, tamanho da população, gerações, taxa de mutação, seed e flag para salvar gráficos.

## Requisitos Não-Funcionais

### RNF01 — Reprodutibilidade
Dada a mesma seed, o sistema deve produzir exatamente os mesmos resultados em execuções diferentes.

### RNF02 — Independência de frameworks de AG
O algoritmo genético deve ser implementado sem uso de bibliotecas de AG prontas (como DEAP, PyGAD, etc.).

### RNF03 — Testabilidade
Cada operador do AG (crossover, mutação, seleção, fitness) deve ser testável de forma isolada.

### RNF04 — Performance mínima
Para instâncias de 20 cidades com 500 gerações e população de 100, a execução deve completar em menos de 30 segundos em hardware comum.

### RNF05 — Cobertura de testes
Os testes unitários devem cobrir todos os operadores genéticos e o cálculo de distância.
