from __future__ import annotations

import pytest

from sssp.dijkstra import dijkstra
from sssp.dmmsy import BMSSP, BaseCase, base_case, bmssp
from sssp.graph import Graph
from sssp.weights import Weight


def test_base_case_returns_success_when_heap_exhausts_before_k_plus_one() -> None:
    graph = Graph()
    graph.add_edge("s", "a", 1)
    graph.add_edge("a", "b", 1)
    distances = {"s": 0}

    result = base_case(graph, bound=10, sources=["s"], distances=distances, k=5)

    assert not result.partial
    assert result.bound == 10
    assert result.vertices == ("s", "a", "b")
    assert distances == {"s": 0, "a": 1, "b": 2}


def test_base_case_returns_partial_boundary_after_k_plus_one_vertices() -> None:
    graph = Graph()
    graph.add_edge("s", "a", 1)
    graph.add_edge("s", "b", 2)
    distances = {"s": 0}

    result = BaseCase(graph, bound=10, sources=["s"], distances=distances, k=1)

    assert result.partial
    assert result.bound == 1
    assert result.vertices == ("s",)
    assert distances["a"] == 1
    assert distances["b"] == 2


def test_bmssp_level_one_matches_dijkstra_below_bound() -> None:
    graph = Graph.from_edges(
        [
            ("s", "a", 1),
            ("a", "b", 1),
            ("b", "c", 1),
            ("s", "d", 5),
        ]
    )
    distances = {"s": 0}

    result = bmssp(graph, level=1, bound=4, sources=["s"], distances=distances, k=2, t=1)

    assert not result.partial
    assert result.bound == 4
    assert set(result.vertices) == {"s", "a", "b", "c"}
    assert _below_bound(distances, result.bound) == _below_bound(dijkstra(graph, "s"), 4)


def test_bmssp_recurses_across_multiple_levels() -> None:
    graph = Graph.from_edges(
        [
            ("s", "a", 1),
            ("s", "b", 3),
            ("a", "c", 1),
            ("c", "d", 1),
            ("b", "d", 1),
            ("d", "e", 1),
        ]
    )
    distances = {"s": 0}

    result = BMSSP(graph, level=2, bound=6, sources=["s"], distances=distances, k=2, t=1)

    assert not result.partial
    assert result.iterations >= 1
    assert _below_bound(distances, result.bound) == _below_bound(dijkstra(graph, "s"), 6)


def test_bmssp_accepts_weight_values_without_forbidden_operations() -> None:
    graph = Graph()
    graph.add_edge("s", "a", Weight(1))
    graph.add_edge("a", "b", Weight(1))
    graph.add_edge("s", "b", Weight(4))
    distances = {"s": Weight(0)}

    result = bmssp(
        graph,
        level=1,
        bound=Weight(5),
        sources=["s"],
        distances=distances,
        k=2,
        t=1,
    )

    assert not result.partial
    assert set(result.vertices) == {"s", "a", "b"}
    assert distances["a"] == Weight(1)
    assert distances["b"] == Weight(2)


def test_bmssp_validates_inputs() -> None:
    graph = Graph()
    graph.add_vertex("s")

    with pytest.raises(ValueError, match="level must be non-negative"):
        bmssp(graph, level=-1, bound=10, sources=["s"], distances={"s": 0}, k=1, t=1)

    with pytest.raises(ValueError, match="k must be at least 1"):
        bmssp(graph, level=0, bound=10, sources=["s"], distances={"s": 0}, k=0, t=1)

    with pytest.raises(ValueError, match="t must be at least 1"):
        bmssp(graph, level=1, bound=10, sources=["s"], distances={"s": 0}, k=1, t=0)

    with pytest.raises(ValueError, match="sources must not be empty"):
        bmssp(graph, level=1, bound=10, sources=[], distances={}, k=1, t=1)

    with pytest.raises(ValueError, match="vertex in graph"):
        bmssp(graph, level=1, bound=10, sources=["missing"], distances={"missing": 0}, k=1, t=1)

    with pytest.raises(ValueError, match="distance label"):
        bmssp(graph, level=1, bound=10, sources=["s"], distances={}, k=1, t=1)

    with pytest.raises(ValueError, match="exactly one source"):
        base_case(graph, bound=10, sources=["s", "s2"], distances={"s": 0, "s2": 0}, k=1)


def _below_bound(distances: dict[object, object], bound: object) -> dict[object, object]:
    return {
        vertex: distance
        for vertex, distance in distances.items()
        if distance < bound
    }
