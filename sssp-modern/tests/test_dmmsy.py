from __future__ import annotations

import math
import random
import time

import pytest

from sssp.dijkstra import dijkstra
from sssp.dmmsy import (
    dmmsy_parameters,
    dmmsy_sssp,
    dmmsy_top_level,
)
from sssp.generators import erdos_renyi_graph
from sssp.graph import Graph
from sssp.weights import Weight


def test_dmmsy_sssp_matches_dijkstra_on_path_graph() -> None:
    graph = Graph.from_edges(
        [
            ("s", "a", 1.0),
            ("a", "b", 1.0),
            ("b", "c", 1.0),
            ("c", "d", 1.0),
        ]
    )

    distances = dmmsy_sssp(graph, "s")

    assert distances == dijkstra(graph, "s")


def test_dmmsy_sssp_matches_dijkstra_on_branching_graph() -> None:
    graph = Graph.from_edges(
        [
            ("s", "a", 1.0),
            ("s", "b", 4.0),
            ("a", "c", 2.0),
            ("c", "d", 1.0),
            ("b", "d", 1.0),
            ("d", "e", 1.0),
        ]
    )

    distances = dmmsy_sssp(graph, "s")

    assert distances == dijkstra(graph, "s")


def test_dmmsy_sssp_omits_unreachable_vertices() -> None:
    graph = Graph()
    graph.add_vertex("s")
    graph.add_vertex("isolated")
    graph.add_edge("s", "a", 1.0)

    distances = dmmsy_sssp(graph, "s")

    assert distances == {"s": 0.0, "a": 1.0}
    assert "isolated" not in distances


def test_dmmsy_sssp_handles_single_vertex_graph() -> None:
    graph = Graph()
    graph.add_vertex("s")

    distances = dmmsy_sssp(graph, "s")

    assert distances == {"s": 0.0}


def test_dmmsy_sssp_accepts_weight_values_without_forbidden_operations() -> None:
    graph = Graph.from_edges(
        [
            ("s", "a", Weight(1)),
            ("a", "b", Weight(1)),
            ("s", "b", Weight(4)),
            ("b", "c", Weight(2)),
        ]
    )

    distances = dmmsy_sssp(graph, "s", zero=Weight(0))

    assert distances["s"] == Weight(0)
    assert distances["a"] == Weight(1)
    assert distances["b"] == Weight(2)
    assert distances["c"] == Weight(4)


def test_dmmsy_parameters_match_paper_formula() -> None:
    assert dmmsy_parameters(1) == (1, 1)
    assert dmmsy_parameters(2) == (1, 1)
    assert dmmsy_parameters(10) == (
        max(1, int(math.log2(10) ** (1.0 / 3.0))),
        max(1, int(math.log2(10) ** (2.0 / 3.0))),
    )
    assert dmmsy_parameters(1000) == (
        max(1, int(math.log2(1000) ** (1.0 / 3.0))),
        max(1, int(math.log2(1000) ** (2.0 / 3.0))),
    )

    with pytest.raises(ValueError, match="graph order must be at least 1"):
        dmmsy_parameters(0)


def test_dmmsy_top_level_clamps_for_small_n() -> None:
    assert dmmsy_top_level(1, 1) >= 1
    assert dmmsy_top_level(2, 1) == 1
    assert dmmsy_top_level(8, 1) == 3
    assert dmmsy_top_level(8, 2) == 2
    assert dmmsy_top_level(1024, 4) == math.ceil(math.log2(1024) / 4)

    with pytest.raises(ValueError, match="graph order must be at least 1"):
        dmmsy_top_level(0, 1)
    with pytest.raises(ValueError, match="t must be at least 1"):
        dmmsy_top_level(8, 0)


def test_dmmsy_sssp_validates_inputs() -> None:
    graph = Graph()
    graph.add_vertex("s")

    with pytest.raises(ValueError, match="source must be a vertex in graph"):
        dmmsy_sssp(graph, "missing")

    with pytest.raises(ValueError, match="k must be at least 1"):
        dmmsy_sssp(graph, "s", k=0)

    with pytest.raises(ValueError, match="t must be at least 1"):
        dmmsy_sssp(graph, "s", t=0)


def test_dmmsy_sssp_accepts_parameter_overrides() -> None:
    graph = Graph.from_edges(
        [
            ("s", "a", 1.0),
            ("a", "b", 1.0),
            ("b", "c", 1.0),
        ]
    )

    distances = dmmsy_sssp(graph, "s", k=2, t=2)

    assert distances == dijkstra(graph, "s")


@pytest.mark.parametrize(
    ("seed", "edge_probability", "weight_low", "weight_high"),
    [
        (101, 0.10, 1.0, 5.0),
        (202, 0.20, 1.0, 10.0),
        (303, 0.30, 1.0, 10.0),
    ],
)
def test_dmmsy_sssp_t_09_oracle_agreement_on_real_weighted_random_graphs(
    seed: int,
    edge_probability: float,
    weight_low: float,
    weight_high: float,
) -> None:
    graph = erdos_renyi_graph(
        n=30,
        edge_probability=edge_probability,
        seed=seed,
        directed=True,
        weight_range=(weight_low, weight_high),
    )

    distances = dmmsy_sssp(graph, "v0")
    oracle = dijkstra(graph, "v0")

    assert set(distances) == set(oracle)
    for vertex in oracle:
        assert distances[vertex] == pytest.approx(oracle[vertex])


@pytest.mark.parametrize("seed", [11, 22, 33])
def test_dmmsy_sssp_t_09_oracle_agreement_on_integer_weighted_dags(seed: int) -> None:
    rng = random.Random(seed)
    n = 25
    graph = Graph(directed=True)
    for index in range(n):
        graph.add_vertex(f"v{index}")
    for source in range(n):
        for target in range(source + 1, n):
            if rng.random() < 0.15:
                graph.add_edge(f"v{source}", f"v{target}", rng.randint(1, 9))

    distances = dmmsy_sssp(graph, "v0")
    oracle = dijkstra(graph, "v0")

    assert set(distances) == set(oracle)
    for vertex in oracle:
        assert distances[vertex] == oracle[vertex]


def test_dmmsy_sssp_t_17_nfr_f_sanity_at_n_1000() -> None:
    """T-17 NFR-F sanity at n=10^3.

    Builds a sparse seeded directed Erdos-Renyi graph at `n = 10^3` where
    most vertices are reachable from `v0`, runs DMMSY and Dijkstra, asserts
    oracle agreement, and enforces a generous absolute time budget on the
    DMMSY wall-clock. The strict 2x ratio assertion required by NFR-F is
    owned by B7.3's benchmark harness; this per-Bolt sanity confirms only
    that the driver terminates and matches Dijkstra at the target size.
    """

    n = 1000
    graph = erdos_renyi_graph(
        n=n,
        edge_probability=0.005,
        seed=2026,
        directed=True,
        weight_range=(1.0, 10.0),
    )

    start_dijkstra = time.perf_counter()
    oracle = dijkstra(graph, "v0")
    dijkstra_seconds = time.perf_counter() - start_dijkstra

    start_dmmsy = time.perf_counter()
    distances = dmmsy_sssp(graph, "v0")
    dmmsy_seconds = time.perf_counter() - start_dmmsy

    assert set(distances) == set(oracle)
    for vertex in oracle:
        assert distances[vertex] == pytest.approx(oracle[vertex])

    assert dmmsy_seconds < 120.0, (
        f"DMMSY wall-clock {dmmsy_seconds:.3f}s exceeded sanity budget at n={n}; "
        "see B7.3 for benchmark-grade NFR-F validation"
    )
