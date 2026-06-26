import random
from .city import City, route_distance

Chromosome = list[int]


# ---------------------------------------------------------------------------
# Fitness
# ---------------------------------------------------------------------------

def fitness(chromosome: Chromosome, cities: list[City]) -> float:
    route = [cities[i] for i in chromosome]
    dist = route_distance(route)
    return 1.0 / dist if dist > 0 else float("inf")


def chromosome_distance(chromosome: Chromosome, cities: list[City]) -> float:
    return route_distance([cities[i] for i in chromosome])


# ---------------------------------------------------------------------------
# Selection
# ---------------------------------------------------------------------------

def tournament_selection(
    population: list[Chromosome],
    fitnesses: list[float],
    k: int = 3,
    rng: random.Random = random,
) -> Chromosome:
    contestants = rng.sample(range(len(population)), k)
    winner = max(contestants, key=lambda i: fitnesses[i])
    return population[winner][:]


# ---------------------------------------------------------------------------
# Crossover — OX1 (Order Crossover)
# ---------------------------------------------------------------------------

def order_crossover(
    parent1: Chromosome,
    parent2: Chromosome,
    rng: random.Random = random,
) -> Chromosome:
    size = len(parent1)
    a, b = sorted(rng.sample(range(size), 2))

    child: Chromosome = [-1] * size
    child[a : b + 1] = parent1[a : b + 1]
    segment_set = set(parent1[a : b + 1])

    fill = [gene for gene in parent2 if gene not in segment_set]
    fill_idx = 0
    for i in range(size):
        if child[i] == -1:
            child[i] = fill[fill_idx]
            fill_idx += 1

    return child


# ---------------------------------------------------------------------------
# Mutation — Inversion (reverses a random sub-segment)
# ---------------------------------------------------------------------------

def inversion_mutation(
    chromosome: Chromosome,
    rate: float = 0.02,
    rng: random.Random = random,
) -> Chromosome:
    result = chromosome[:]
    if rng.random() < rate:
        a, b = sorted(rng.sample(range(len(result)), 2))
        result[a : b + 1] = result[a : b + 1][::-1]
    return result


# ---------------------------------------------------------------------------
# Greedy nearest-neighbor baseline
# ---------------------------------------------------------------------------

def greedy_nearest_neighbor(cities: list[City], start: int = 0) -> Chromosome:
    n = len(cities)
    unvisited = set(range(n))
    route = [start]
    unvisited.remove(start)
    while unvisited:
        last = route[-1]
        nearest = min(unvisited, key=lambda j: cities[last].distance_to(cities[j]))
        route.append(nearest)
        unvisited.remove(nearest)
    return route


# ---------------------------------------------------------------------------
# Genetic Algorithm
# ---------------------------------------------------------------------------

class GeneticAlgorithm:
    def __init__(
        self,
        cities: list[City],
        population_size: int = 100,
        generations: int = 500,
        mutation_rate: float = 0.02,
        elitism: int = 5,
        tournament_k: int = 3,
        seed: int | None = None,
    ) -> None:
        self.cities = cities
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elitism = elitism
        self.tournament_k = tournament_k
        self.rng = random.Random(seed)
        self.history: list[float] = []

    def _random_chromosome(self) -> Chromosome:
        chrom = list(range(len(self.cities)))
        self.rng.shuffle(chrom)
        return chrom

    def _init_population(self) -> list[Chromosome]:
        return [self._random_chromosome() for _ in range(self.population_size)]

    def _evaluate(self, population: list[Chromosome]) -> list[float]:
        return [fitness(chrom, self.cities) for chrom in population]

    def run(
        self,
        on_generation: "callable[[int, list[Chromosome], list[float]], None] | None" = None,
    ) -> tuple[Chromosome, float]:
        population = self._init_population()
        best_chrom: Chromosome = []
        best_dist = float("inf")

        for gen in range(self.generations):
            fitnesses = self._evaluate(population)

            ranked = sorted(range(len(population)), key=lambda i: fitnesses[i], reverse=True)
            current_best_dist = chromosome_distance(population[ranked[0]], self.cities)
            if current_best_dist < best_dist:
                best_dist = current_best_dist
                best_chrom = population[ranked[0]][:]

            self.history.append(best_dist)

            if on_generation:
                on_generation(gen, population, fitnesses)

            new_population: list[Chromosome] = [population[i][:] for i in ranked[: self.elitism]]

            while len(new_population) < self.population_size:
                p1 = tournament_selection(population, fitnesses, self.tournament_k, self.rng)
                p2 = tournament_selection(population, fitnesses, self.tournament_k, self.rng)
                child = order_crossover(p1, p2, self.rng)
                child = inversion_mutation(child, self.mutation_rate, self.rng)
                new_population.append(child)

            population = new_population

        return best_chrom, best_dist
