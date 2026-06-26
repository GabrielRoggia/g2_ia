import math
import pytest
from src.city import City, generate_cities, route_distance


def test_distance_between_same_city_is_zero():
    c = City(x=3.0, y=4.0)
    assert c.distance_to(c) == 0.0


def test_distance_known_value():
    a = City(x=0.0, y=0.0)
    b = City(x=3.0, y=4.0)
    assert math.isclose(a.distance_to(b), 5.0)


def test_distance_symmetry():
    a = City(x=1.5, y=2.7)
    b = City(x=8.3, y=5.1)
    assert math.isclose(a.distance_to(b), b.distance_to(a))


def test_generate_cities_count():
    cities = generate_cities(n=10, seed=1)
    assert len(cities) == 10


def test_generate_cities_within_bounds():
    cities = generate_cities(n=50, seed=99, width=50.0, height=80.0)
    for c in cities:
        assert 0.0 <= c.x <= 50.0
        assert 0.0 <= c.y <= 80.0


def test_generate_cities_reproducible():
    cities_a = generate_cities(n=20, seed=42)
    cities_b = generate_cities(n=20, seed=42)
    for a, b in zip(cities_a, cities_b):
        assert a.x == b.x and a.y == b.y


def test_generate_cities_different_seeds_differ():
    cities_a = generate_cities(n=20, seed=1)
    cities_b = generate_cities(n=20, seed=2)
    coords_a = [(c.x, c.y) for c in cities_a]
    coords_b = [(c.x, c.y) for c in cities_b]
    assert coords_a != coords_b


def test_route_distance_triangle():
    a = City(x=0, y=0)
    b = City(x=3, y=0)
    c = City(x=3, y=4)
    dist = route_distance([a, b, c])
    # a->b: 3, b->c: 4, c->a: 5 (3-4-5 right triangle)
    assert math.isclose(dist, 12.0)


def test_route_distance_single_city_is_zero():
    c = City(x=5, y=5)
    assert route_distance([c]) == 0.0
