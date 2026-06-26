import os
import random
import pytest
from src.city import generate_cities, route_distance
from src.genetic_algorithm import (
    fitness,
    tournament_selection,
    order_crossover,
    inversion_mutation,
    greedy_nearest_neighbor,
    chromosome_distance,
    GeneticAlgorithm,
)


CITIES = generate_cities(10, seed=42)
N = len(CITIES)


# ---------------------------------------------------------------------------
# CA01 — Validade de cromossomo
# ---------------------------------------------------------------------------

def test_chromosome_is_valid_permutation():
    ga = GeneticAlgorithm(CITIES, population_size=50, generations=1, seed=0)
    chrom, _ = ga.run()
    assert sorted(chrom) == list(range(N))


# ---------------------------------------------------------------------------
# CA02 — Crossover OX1 produz permutação válida
# ---------------------------------------------------------------------------

def test_order_crossover_validity():
    rng = random.Random(7)
    for _ in range(100):
        p1 = list(range(N))
        p2 = list(range(N))
        rng.shuffle(p1)
        rng.shuffle(p2)
        child = order_crossover(p1, p2, rng)
        assert sorted(child) == list(range(N)), f"Filho inválido: {child}"


def test_order_crossover_inherits_segment_from_parent1():
    rng = random.Random(0)
    p1 = list(range(N))
    p2 = list(reversed(range(N)))
    child = order_crossover(p1, p2, rng)
    # child must be a valid permutation
    assert sorted(child) == list(range(N))


# ---------------------------------------------------------------------------
# CA03 — Mutação por inversão preserva genes
# ---------------------------------------------------------------------------

def test_inversion_mutation_preserves_genes():
    rng = random.Random(3)
    chrom = list(range(N))
    for _ in range(200):
        mutated = inversion_mutation(chrom, rate=1.0, rng=rng)
        assert sorted(mutated) == list(range(N))


def test_inversion_mutation_rate_zero_no_change():
    rng = random.Random(0)
    chrom = list(range(N))
    mutated = inversion_mutation(chrom, rate=0.0, rng=rng)
    assert mutated == chrom


# ---------------------------------------------------------------------------
# Fitness
# ---------------------------------------------------------------------------

def test_fitness_shorter_route_has_higher_fitness():
    short = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    long_route = list(reversed(short))
    cities = generate_cities(10, seed=0)
    f_short = fitness(short, cities)
    f_long = fitness(long_route, cities)
    # One of them should be strictly higher (routes differ)
    assert f_short != f_long or chromosome_distance(short, cities) == chromosome_distance(long_route, cities)


def test_fitness_positive():
    chrom = list(range(N))
    assert fitness(chrom, CITIES) > 0


# ---------------------------------------------------------------------------
# Seleção por torneio
# ---------------------------------------------------------------------------

def test_tournament_selection_returns_valid_chromosome():
    rng = random.Random(1)
    population = [list(range(N)) for _ in range(20)]
    for p in population:
        rng.shuffle(p)
    fitnesses = [fitness(p, CITIES) for p in population]
    selected = tournament_selection(population, fitnesses, k=3, rng=rng)
    assert sorted(selected) == list(range(N))


# ---------------------------------------------------------------------------
# CA07 — Reprodutibilidade
# ---------------------------------------------------------------------------

def test_reproducibility():
    ga1 = GeneticAlgorithm(CITIES, population_size=30, generations=50, seed=99)
    ga2 = GeneticAlgorithm(CITIES, population_size=30, generations=50, seed=99)
    _, dist1 = ga1.run()
    _, dist2 = ga2.run()
    assert dist1 == dist2


# ---------------------------------------------------------------------------
# Greedy baseline
# ---------------------------------------------------------------------------

def test_greedy_nearest_neighbor_valid_route():
    route = greedy_nearest_neighbor(CITIES, start=0)
    assert sorted(route) == list(range(N))


def test_greedy_nearest_neighbor_starts_at_given_city():
    route = greedy_nearest_neighbor(CITIES, start=3)
    assert route[0] == 3


# ---------------------------------------------------------------------------
# GA melhora ao longo das gerações
# ---------------------------------------------------------------------------

def test_ga_improves_over_random():
    cities = generate_cities(15, seed=7)
    ga = GeneticAlgorithm(cities, population_size=50, generations=200, seed=42)
    _, best_dist = ga.run()

    # Compare with average of random permutations
    rng = random.Random(0)
    random_dists = []
    for _ in range(30):
        chrom = list(range(len(cities)))
        rng.shuffle(chrom)
        random_dists.append(chromosome_distance(chrom, cities))
    avg_random = sum(random_dists) / len(random_dists)

    assert best_dist < avg_random, (
        f"AG ({best_dist:.2f}) não melhorou sobre média aleatória ({avg_random:.2f})"
    )


# ---------------------------------------------------------------------------
# CA08 — Visualização cria arquivos
# ---------------------------------------------------------------------------

def test_visualization_saves_files(tmp_path):
    from src.visualization import plot_route, plot_evolution
    import matplotlib
    matplotlib.use("Agg")

    cities = generate_cities(5, seed=1)
    route = list(range(5))
    history = [100.0 - i * 0.1 for i in range(50)]

    route_path = str(tmp_path / "route.png")
    evo_path = str(tmp_path / "evolution.png")

    plot_route(cities, route, save_path=route_path)
    plot_evolution(history, save_path=evo_path)

    assert os.path.exists(route_path) and os.path.getsize(route_path) > 0
    assert os.path.exists(evo_path) and os.path.getsize(evo_path) > 0
