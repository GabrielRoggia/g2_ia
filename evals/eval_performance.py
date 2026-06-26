"""
Avaliação de performance do AG para TSP.

Valida os critérios de aceite CA05, CA06 e CA10 definidos em
specs/criterios-aceite.md e imprime um relatório de métricas.
"""

import sys
import time

sys.path.insert(0, ".")

from src.city import generate_cities, route_distance
from src.genetic_algorithm import (
    GeneticAlgorithm,
    greedy_nearest_neighbor,
    chromosome_distance,
)


def run_eval(
    n_cities: int = 20,
    population_size: int = 100,
    generations: int = 500,
    mutation_rate: float = 0.02,
    seed: int = 42,
) -> dict:
    cities = generate_cities(n_cities, seed=seed)

    greedy_route = greedy_nearest_neighbor(cities, start=0)
    greedy_dist = chromosome_distance(greedy_route, cities)

    ga = GeneticAlgorithm(
        cities=cities,
        population_size=population_size,
        generations=generations,
        mutation_rate=mutation_rate,
        seed=seed,
    )

    start = time.time()
    best_route, best_dist = ga.run()
    elapsed = time.time() - start

    improved_in_100 = ga.history[99] < ga.history[0] if len(ga.history) >= 100 else False
    ratio = best_dist / greedy_dist if greedy_dist > 0 else float("inf")

    return {
        "n_cities": n_cities,
        "greedy_distance": greedy_dist,
        "ag_distance": best_dist,
        "ratio_ag_vs_greedy": ratio,
        "elapsed_seconds": elapsed,
        "improved_in_100_gens": improved_in_100,
        "history": ga.history,
    }


def print_report(metrics: dict) -> bool:
    ca05 = metrics["improved_in_100_gens"]
    ca06 = metrics["ratio_ag_vs_greedy"] <= 1.20
    ca10 = metrics["elapsed_seconds"] < 30.0
    all_pass = ca05 and ca06 and ca10

    print("=" * 50)
    print("  AVALIAÇÃO DE PERFORMANCE — TSP-GA")
    print("=" * 50)
    print(f"  Cidades:           {metrics['n_cities']}")
    print(f"  Dist. Greedy:      {metrics['greedy_distance']:.2f}")
    print(f"  Dist. AG:          {metrics['ag_distance']:.2f}")
    print(f"  Razão AG/Greedy:   {metrics['ratio_ag_vs_greedy']:.3f}")
    print(f"  Tempo:             {metrics['elapsed_seconds']:.2f}s")
    print("-" * 50)
    print(f"  CA05 — Melhoria em 100 ger.:  {'PASS' if ca05 else 'FAIL'}")
    print(f"  CA06 — AG/Greedy ≤ 1.20:      {'PASS' if ca06 else 'FAIL'}  ({metrics['ratio_ag_vs_greedy']:.3f})")
    print(f"  CA10 — Tempo < 30s:           {'PASS' if ca10 else 'FAIL'}  ({metrics['elapsed_seconds']:.1f}s)")
    print("-" * 50)
    print(f"  Veredicto: {'ACEITO' if all_pass else 'REJEITADO'}")
    print("=" * 50)

    return all_pass


if __name__ == "__main__":
    metrics = run_eval()
    passed = print_report(metrics)
    sys.exit(0 if passed else 1)
