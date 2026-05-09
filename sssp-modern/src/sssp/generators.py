"""Deterministic graph generators for SSSP benchmark inputs."""

from __future__ import annotations

import math
import random
from collections.abc import Sequence

from sssp.graph import Graph

WeightRange = tuple[float, float]


def erdos_renyi_graph(
    n: int,
    edge_probability: float,
    seed: int,
    directed: bool = True,
    weight_range: WeightRange = (1.0, 10.0),
) -> Graph:
    """Generate a seeded Erdos-Renyi weighted graph."""

    _require_n(n)
    _require_probability(edge_probability, "edge_probability")
    _require_weight_range(weight_range)
    rng = random.Random(seed)
    graph = _empty_graph(n, directed=directed)

    if directed:
        pairs = ((i, j) for i in range(n) for j in range(n) if i != j)
    else:
        pairs = ((i, j) for i in range(n) for j in range(i + 1, n))

    for source, target in pairs:
        if rng.random() <= edge_probability:
            graph.add_edge(_vertex(source), _vertex(target), _random_weight(rng, weight_range))

    return graph


def random_geometric_graph(
    n: int,
    radius: float,
    seed: int,
    directed: bool = False,
    weight_range: WeightRange | None = None,
) -> Graph:
    """Generate a seeded random geometric graph in the unit square."""

    _require_n(n)
    if radius < 0:
        raise ValueError("radius must be non-negative")
    if weight_range is not None:
        _require_weight_range(weight_range)

    rng = random.Random(seed)
    points = [(rng.random(), rng.random()) for _ in range(n)]
    graph = _empty_graph(n, directed=directed)

    for i in range(n):
        for j in range(i + 1, n):
            distance = math.hypot(points[i][0] - points[j][0], points[i][1] - points[j][1])
            if distance <= radius:
                weight = (
                    _random_weight(rng, weight_range)
                    if weight_range is not None
                    else distance
                )
                graph.add_edge(_vertex(i), _vertex(j), weight)
                if directed:
                    graph.add_edge(_vertex(j), _vertex(i), weight)

    return graph


def dag_graph(
    n: int,
    edge_probability: float,
    seed: int,
    weight_range: WeightRange = (1.0, 10.0),
) -> Graph:
    """Generate a seeded directed acyclic weighted graph."""

    _require_n(n)
    _require_probability(edge_probability, "edge_probability")
    _require_weight_range(weight_range)
    rng = random.Random(seed)
    graph = _empty_graph(n, directed=True)

    for source in range(n):
        for target in range(source + 1, n):
            if rng.random() <= edge_probability:
                graph.add_edge(
                    _vertex(source),
                    _vertex(target),
                    _random_weight(rng, weight_range),
                )

    return graph


def barabasi_albert_graph(
    n: int,
    attachments: int,
    seed: int,
    weight_range: WeightRange = (1.0, 10.0),
) -> Graph:
    """Generate a seeded undirected preferential-attachment graph."""

    _require_n(n)
    if attachments < 1:
        raise ValueError("attachments must be at least 1")
    if attachments >= n:
        raise ValueError("attachments must be smaller than n")
    _require_weight_range(weight_range)

    rng = random.Random(seed)
    graph = _empty_graph(n, directed=False)
    degree: dict[str, int] = {_vertex(i): 0 for i in range(n)}
    initial_count = attachments + 1

    for source in range(initial_count):
        for target in range(source + 1, initial_count):
            _add_undirected_weighted_edge(graph, degree, source, target, rng, weight_range)

    for node in range(initial_count, n):
        candidates = [_vertex(index) for index in range(node)]
        for target in _preferential_targets(rng, candidates, degree, attachments):
            _add_undirected_weighted_edge(
                graph,
                degree,
                node,
                int(target[1:]),
                rng,
                weight_range,
            )

    return graph


def signed_edge_graph(
    n: int,
    edge_probability: float,
    seed: int,
    negative_fraction: float = 0.25,
    weight_range: WeightRange = (1.0, 10.0),
    acyclic: bool = True,
) -> Graph:
    """Generate a seeded directed graph that may contain negative weights."""

    _require_n(n)
    _require_probability(edge_probability, "edge_probability")
    _require_probability(negative_fraction, "negative_fraction")
    _require_weight_range(weight_range)
    rng = random.Random(seed)
    graph = _empty_graph(n, directed=True)

    if acyclic:
        pairs = ((i, j) for i in range(n) for j in range(i + 1, n))
    else:
        pairs = ((i, j) for i in range(n) for j in range(n) if i != j)

    for source, target in pairs:
        if rng.random() <= edge_probability:
            magnitude = _random_weight(rng, weight_range)
            sign = -1.0 if rng.random() < negative_fraction else 1.0
            graph.add_edge(_vertex(source), _vertex(target), sign * magnitude)

    return graph


def _empty_graph(n: int, directed: bool) -> Graph:
    graph = Graph(directed=directed)
    for index in range(n):
        graph.add_vertex(_vertex(index))
    return graph


def _vertex(index: int) -> str:
    return f"v{index}"


def _random_weight(rng: random.Random, weight_range: WeightRange) -> float:
    low, high = weight_range
    return rng.uniform(low, high)


def _add_undirected_weighted_edge(
    graph: Graph,
    degree: dict[str, int],
    source: int,
    target: int,
    rng: random.Random,
    weight_range: WeightRange,
) -> None:
    source_vertex = _vertex(source)
    target_vertex = _vertex(target)
    graph.add_edge(source_vertex, target_vertex, _random_weight(rng, weight_range))
    degree[source_vertex] += 1
    degree[target_vertex] += 1


def _preferential_targets(
    rng: random.Random,
    candidates: Sequence[str],
    degree: dict[str, int],
    count: int,
) -> tuple[str, ...]:
    targets: list[str] = []
    while len(targets) < count:
        pool = [
            vertex
            for vertex in candidates
            for _ in range(max(1, degree[vertex]))
            if vertex not in targets
        ]
        choice = rng.choice(pool)
        targets.append(choice)
    return tuple(targets)


def _require_n(n: int) -> None:
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")


def _require_probability(value: float, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise TypeError(f"{name} must be numeric")
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")


def _require_weight_range(weight_range: WeightRange) -> None:
    if len(weight_range) != 2:
        raise ValueError("weight_range must contain exactly two values")
    low, high = weight_range
    if isinstance(low, bool) or isinstance(high, bool):
        raise TypeError("weight_range bounds must be numeric")
    if not isinstance(low, int | float) or not isinstance(high, int | float):
        raise TypeError("weight_range bounds must be numeric")
    if low < 0 or high < 0:
        raise ValueError("weight_range bounds must be non-negative")
    if low > high:
        raise ValueError("weight_range lower bound must be <= upper bound")
