import math
import random
from dataclasses import dataclass, field


@dataclass
class City:
    x: float
    y: float
    name: str = field(default="")

    def distance_to(self, other: "City") -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __repr__(self) -> str:
        label = self.name or f"({self.x:.1f},{self.y:.1f})"
        return f"City({label})"


def generate_cities(
    n: int,
    seed: int = 42,
    width: float = 100.0,
    height: float = 100.0,
) -> list[City]:
    rng = random.Random(seed)
    return [
        City(x=rng.uniform(0, width), y=rng.uniform(0, height), name=f"C{i}")
        for i in range(n)
    ]


def route_distance(route: list[City]) -> float:
    n = len(route)
    return sum(route[i].distance_to(route[(i + 1) % n]) for i in range(n))
