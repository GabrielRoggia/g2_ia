# Prompts Usados no Desenvolvimento — TSP-GA

Registro dos principais prompts utilizados com Claude Code durante o desenvolvimento do projeto.

---

## P01 — Escolha do tema
**Prompt:**
> "de dicas para realizar este trabalho [PDF do trabalho 2 de IA]"

**Resultado:** Orientações sobre estrutura do harness, processo de desenvolvimento, dicas por seção.

---

## P02 — Seleção do tema de IA
**Prompt:**
> "primeiramente me ajude a escolher o tema"

**Resultado:** Apresentação de três opções (Knapsack, TSP, Horário escolar). Escolhido TSP por ser o mais associado a AG, visualmente demonstrável e com boa documentação.

---

## P03 — Construção completa do projeto
**Prompt:**
> "faça o trabalho utilizando sua recomendação, siga todos os requisitos obrigatórios solicitados"

**Resultado:** Geração de toda a estrutura do projeto: harness completo (specs/, .claude/, CLAUDE.md), código-fonte (src/), testes (tests/, evals/) e documentação (docs/, README.md).

**Decisões tomadas durante a geração:**
- Crossover OX1 escolhido sobre PMX por ser mais simples de implementar e igualmente eficaz para TSP de médio porte
- Mutação por inversão de segmento preferida sobre swap por reorganizar sub-rotas de forma mais inteligente
- Elitismo com k=5 como padrão — compromisso entre diversidade e preservação das melhores soluções
- matplotlib como única dependência externa — numpy não necessário para este escopo

---

## P04 — Estrutura de testes TDD
**Contexto:** O enunciado cita TDD (Test-Driven Development).  
**Abordagem adotada:** Critérios de aceite escritos antes do código (CA01–CA10 em `specs/criterios-aceite.md`), testes unitários escritos para validar cada operador isoladamente.

---

## Prompts-modelo para uso futuro

### Para expandir o projeto
```
Implemente o operador 2-opt como pós-processamento local após o AG convergir.
O 2-opt deve estar em src/local_search.py e integrado opcionalmente via flag --local-search.
Siga as convenções em .claude/context.md.
```

### Para adicionar uma instância real do TSP
```
Adicione suporte para carregar instâncias no formato TSPLIB (.tsp) em src/city.py.
A função deve ser load_tsplib(path: str) -> list[City].
Adicione um teste em tests/test_city.py com o arquivo eil51.tsp de exemplo.
```

### Para avaliar com múltiplas seeds
```
Modifique evals/eval_performance.py para rodar o AG com seeds 1 a 10,
calcular média e desvio padrão da distância final, e comparar com greedy em todas as seeds.
```
