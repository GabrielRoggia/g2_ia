# CLAUDE.md — Mapa do Projeto TSP-GA

## O que é este projeto
Solução de IA que resolve o **Problema do Caixeiro Viajante (TSP)** usando um **Algoritmo Genético** implementado em Python. O objetivo é encontrar a rota mais curta que visita N cidades exatamente uma vez e retorna à origem.

## Problema que resolve
Dado um conjunto de cidades com coordenadas (x, y), encontrar a permutação de visita que minimiza a distância total percorrida. Problema NP-difícil — AG encontra soluções de boa qualidade em tempo polinomial.

## Estrutura do projeto
```
specs/          → especificação SDD: problema, requisitos, critérios de aceite
.claude/        → contexto e instruções para IA durante o desenvolvimento
src/            → código-fonte da solução
tests/          → testes unitários (pytest)
evals/          → avaliação de performance vs baseline
docs/           → documentação técnica e decisões de arquitetura
results/        → saída gerada (gráficos, métricas)
```

## Fontes de informação aprofundadas
- `specs/projeto.md` — descrição completa do problema e objetivos
- `specs/requisitos.md` — requisitos funcionais e não-funcionais
- `specs/criterios-aceite.md` — critérios testáveis de aceitação
- `.claude/context.md` — contexto técnico, stack, decisões de design
- `.claude/prompts.md` — histórico de prompts usados no desenvolvimento
- `docs/algoritmo-genetico.md` — teoria e operadores do AG
- `docs/decisoes-tecnicas.md` — justificativas das escolhas de implementação

## Stack técnica
- Python 3.10+
- `matplotlib` para visualização
- `pytest` para testes
- Sem dependência de frameworks de ML externos

## Restrições técnicas
- Algoritmo genético implementado do zero (sem bibliotecas de AG prontas)
- Solução deve ser reproduzível via seed aleatória
- Testes devem passar antes de qualquer merge

## Como rodar
```bash
pip install -r requirements.txt
python -m src.main --cities 20 --generations 500 --save
pytest tests/
python evals/eval_performance.py
```

## Critérios rápidos de aceite
- AG encontra rota ≤ 20% acima do baseline greedy em instâncias de 20 cidades
- Distância melhora monotonicamente nas primeiras 100 gerações
- Todos os testes unitários passam
- Gráfico de evolução e rota final são gerados corretamente
