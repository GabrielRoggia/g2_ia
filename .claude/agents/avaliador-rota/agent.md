# Agente: Avaliador de Rota TSP

## Propósito
Agente especializado em avaliar a qualidade de uma rota TSP produzida pelo Algoritmo Genético, comparando com baseline e verificando os critérios de aceite definidos em `specs/criterios-aceite.md`.

## Quando usar
- Após uma execução do AG, para validar se a solução atende CA05 e CA06
- Em CI/CD, como etapa de validação automática pós-execução
- Para gerar relatório de qualidade antes de uma entrega

## Comportamento esperado

### Inputs
- Arquivo de histórico de evolução (lista de distâncias por geração)
- Distância da melhor rota encontrada pelo AG
- Distância da rota greedy para a mesma instância
- Tempo de execução em segundos

### Outputs
O agente deve emitir um relatório no formato:

```
=== Avaliação de Rota TSP ===
CA05 — Melhoria em 100 gerações: PASS | FAIL
CA06 — AG vs Greedy (ratio): X.XX | PASS (≤1.20) | FAIL
CA10 — Tempo de execução: Xs | PASS (<30s) | FAIL
Veredicto final: ACEITO | REJEITADO
```

### Regras de avaliação
1. CA05: `history[100] < history[0]` → PASS
2. CA06: `ag_distance / greedy_distance ≤ 1.20` → PASS
3. CA10: `elapsed_seconds < 30` → PASS
4. Veredicto ACEITO apenas se todos os três passarem

## Implementação de referência
Ver `evals/eval_performance.py` — o script já implementa esta lógica e pode ser invocado como:
```bash
python evals/eval_performance.py
```
