# Skill: Otimizador Genético para TSP

## Propósito
Skill reutilizável que encapsula o conhecimento necessário para configurar e executar o Algoritmo Genético deste projeto, tunar parâmetros e interpretar resultados.

## Como usar esta skill

### Execução básica
```bash
python -m src.main --cities 20 --generations 500 --population 100 --save
```

### Parâmetros e seus efeitos

| Parâmetro | Padrão | Efeito ao aumentar |
|-----------|--------|---------------------|
| `--cities` | 20 | Problema mais difícil, mais gerações necessárias |
| `--population` | 100 | Melhor exploração, mais lento por geração |
| `--generations` | 500 | Maior chance de convergência, mais tempo total |
| `--mutation` | 0.02 | Mais diversidade, risco de perder boas soluções |
| `--elitism` | 5 | Mais conservador, menos diversidade |

### Sinais de problema e ajustes

**AG converge muito rápido (platô nas primeiras 50 gerações):**
→ Aumentar `--mutation` (0.05) ou reduzir `--elitism` (2)

**AG não converge (distância oscila sem melhorar):**
→ Reduzir `--mutation` (0.01), aumentar `--population` (200)

**Resultado muito inferior ao greedy:**
→ Aumentar `--generations` (1000) e `--population` (200)

## Regras desta skill

1. Sempre usar `--seed` fixo para comparações reproduzíveis
2. Validar CA05 e CA06 após qualquer alteração de parâmetros
3. Nunca modificar os operadores genéticos sem atualizar os testes em `tests/test_ga.py`
4. Registrar novos experimentos de parametrização em `.claude/prompts.md`

## Referência de operadores
- Crossover: OX1 — detalhes em `docs/algoritmo-genetico.md`
- Mutação: Inversão de segmento — detalhes em `docs/algoritmo-genetico.md`
- Seleção: Torneio k=3 — detalhes em `docs/decisoes-tecnicas.md`
