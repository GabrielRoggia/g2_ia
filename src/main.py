import argparse
import os
import time

from .city import generate_cities, route_distance
from .genetic_algorithm import GeneticAlgorithm, greedy_nearest_neighbor, chromosome_distance
from .visualization import plot_route, plot_evolution, plot_population


def main() -> None:
    parser = argparse.ArgumentParser(description="TSP com Algoritmo Genético")
    parser.add_argument("--cities", type=int, default=20, help="Número de cidades")
    parser.add_argument("--population", type=int, default=100, help="Tamanho da população")
    parser.add_argument("--generations", type=int, default=500, help="Número de gerações")
    parser.add_argument("--mutation", type=float, default=0.02, help="Taxa de mutação")
    parser.add_argument("--elitism", type=int, default=5, help="Número de elites preservados")
    parser.add_argument("--seed", type=int, default=42, help="Seed para reprodutibilidade")
    parser.add_argument("--save", action="store_true", help="Salvar gráficos em results/")
    parser.add_argument("--show-pop", type=int, default=0, metavar="N",
                        help="Mostrar população completa (pior→melhor) a cada N gerações")
    parser.add_argument("--show-best", type=int, default=0, metavar="N",
                        help="Salvar gráfico da melhor rota a cada N gerações")
    args = parser.parse_args()

    print(f"=== TSP com Algoritmo Genético ===")
    print(f"Cidades: {args.cities} | Geração: {args.generations} | Pop: {args.population}")
    print(f"Mutação: {args.mutation} | Elitismo: {args.elitism} | Seed: {args.seed}\n")

    cities = generate_cities(args.cities, seed=args.seed)

    greedy_route = greedy_nearest_neighbor(cities)
    greedy_dist = chromosome_distance(greedy_route, cities)
    print(f"Baseline greedy (nearest neighbor): {greedy_dist:.2f}")

    ga = GeneticAlgorithm(
        cities=cities,
        population_size=args.population,
        generations=args.generations,
        mutation_rate=args.mutation,
        elitism=args.elitism,
        seed=args.seed,
    )

    def show_population(gen: int, population, fitnesses):
        if args.show_pop and (gen + 1) % args.show_pop == 0:
            n_ind = len(population)
            ranked = sorted(range(n_ind), key=lambda i: fitnesses[i])  # pior → melhor
            elite_set = set(ranked[n_ind - args.elitism:])

            print(f"\n{'─'*62}")
            print(f"  Geração {gen + 1:>4} — população ordenada do PIOR ao MELHOR")
            print(f"{'─'*62}")
            print(f"  {'#':>4}  {'Distância':>10}  {'Fitness':>12}  Rota")
            print(f"{'─'*62}")
            for rank, idx in enumerate(ranked):
                dist = chromosome_distance(population[idx], cities)
                fit = fitnesses[idx]
                tag = " ← PIOR" if rank == 0 else (" ← MELHOR" if rank == n_ind - 1 else "")
                print(f"  {rank+1:>4}  {dist:>10.2f}  {fit:>12.6f}  {population[idx]}{tag}")
            print(f"{'─'*62}")

            # Subpasta por geração
            gen_dir = f"results/gen_{gen + 1:04d}"
            os.makedirs(gen_dir, exist_ok=True)

            # Gráfico de barras da população
            dists = [chromosome_distance(population[i], cities) for i in range(n_ind)]
            pop_path = f"{gen_dir}/populacao_barras.png"
            plot_population(dists, generation=gen + 1, elitism=args.elitism, save_path=pop_path)

            # Gráfico de rota para cada indivíduo (pior → melhor)
            for rank, idx in enumerate(ranked):
                dist = chromosome_distance(population[idx], cities)
                is_elite = idx in elite_set
                label = "MELHOR" if rank == n_ind - 1 else ("PIOR" if rank == 0 else f"{rank+1:02d}")
                elite_tag = "_elite" if is_elite else ""
                route_path = f"{gen_dir}/rota_{rank+1:02d}_{label}{elite_tag}_dist{dist:.0f}.png"
                title = (
                    f"Geração {gen+1} | Indivíduo {rank+1}/{n_ind} "
                    f"({'ELITE ' if is_elite else ''}dist={dist:.1f})"
                )
                plot_route(cities, population[idx], title=title, save_path=route_path)

            print(f"  {n_ind + 1} gráficos salvos em {gen_dir}/")

    def show_best(gen: int, population, fitnesses):
        if args.show_best and (gen + 1) % args.show_best == 0:
            ranked = sorted(range(len(population)), key=lambda i: fitnesses[i], reverse=True)
            best_idx = ranked[0]
            dist = chromosome_distance(population[best_idx], cities)
            os.makedirs("results/best", exist_ok=True)
            path = f"results/best/gen_{gen + 1:04d}_dist{dist:.0f}.png"
            title = f"Melhor rota — Geração {gen + 1} | dist={dist:.1f}"
            plot_route(cities, population[best_idx], title=title, save_path=path)
            print(f"  Gen {gen + 1:>4} | melhor dist: {dist:.2f} → {path}")

    def on_generation(gen, population, fitnesses):
        show_population(gen, population, fitnesses)
        show_best(gen, population, fitnesses)

    start = time.time()
    best_route, best_dist = ga.run(on_generation=on_generation if (args.show_pop or args.show_best) else None)
    elapsed = time.time() - start

    ratio = best_dist / greedy_dist
    print(f"Melhor rota AG:                     {best_dist:.2f}")
    print(f"Razão AG / Greedy:                  {ratio:.3f} ({'OK' if ratio <= 1.20 else 'ACIMA DO LIMITE'})")
    print(f"Tempo de execução:                  {elapsed:.1f}s")
    print(f"\nRota: {best_route}")

    if args.save or args.show_best:
        os.makedirs("results", exist_ok=True)
        route_title = f"Melhor Rota TSP ({args.cities} cidades | dist={best_dist:.1f})"
        plot_route(cities, best_route, title=route_title, save_path="results/route.png")
        plot_evolution(ga.history, save_path="results/evolution.png")
        print("\nGráficos salvos: results/route.png, results/evolution.png")


if __name__ == "__main__":
    main()
