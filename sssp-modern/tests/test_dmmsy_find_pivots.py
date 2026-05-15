from __future__ import annotations

import pytest

from sssp.dmmsy import FindPivots, find_pivots
from sssp.graph import Graph
from sssp.weights import Weight


def test_find_pivots_relaxes_only_k_layers() -> None:
    graph = Graph()
    graph.add_vertex("x")
    graph.add_edge("s", "a", 1)
    graph.add_edge("a", "b", 1)
    graph.add_edge("b", "c", 1)
    distances = {"s": 0, "x": 0}

    result = find_pivots(graph, bound=10, sources=["s", "x"], distances=distances, k=2)

    assert result.layers == (("s", "x"), ("a",), ("b",))
    assert result.visited == ("s", "x", "a", "b")
    assert result.pivots == ("s",)
    assert not result.saturated
    assert distances["b"] == 2
    assert "c" not in distances


def test_find_pivots_early_returns_sources_when_work_exceeds_limit() -> None:
    graph = Graph()
    for index in range(3):
        graph.add_edge("s", f"v{index}", index + 1)
    distances = {"s": 0}

    result = find_pivots(graph, bound=10, sources=["s"], distances=distances, k=1)

    assert result.saturated
    assert result.pivots == ("s",)
    assert set(result.visited) == {"s", "v0", "v1", "v2"}
    assert result.layers == (("s",), ("v0", "v1", "v2"))


def test_find_pivots_promotes_roots_with_large_tight_trees() -> None:
    graph = Graph()
    graph.add_edge("s", "a", 1)
    graph.add_edge("a", "b", 1)
    graph.add_edge("b", "c", 1)
    graph.add_edge("t", "x", 1)
    distances = {"s": 0, "t": 0}

    result = FindPivots(graph, bound=20, sources=["t", "s"], distances=distances, k=4)

    assert not result.saturated
    assert result.pivots == ("s",)
    assert set(result.visited) == {"s", "t", "a", "b", "c", "x"}
    assert len(result.pivots) <= len(result.visited) // 4


def test_find_pivots_respects_bound_and_existing_shorter_labels() -> None:
    graph = Graph()
    graph.add_edge("s", "near", 4)
    graph.add_edge("s", "at-bound", 5)
    graph.add_edge("s", "too-far", 6)
    graph.add_edge("s", "shorter", 10)
    distances = {"s": 0, "shorter": 1}

    result = find_pivots(graph, bound=5, sources=["s"], distances=distances, k=3)

    assert result.visited == ("s", "near")
    assert result.pivots == ()
    assert distances["near"] == 4
    assert distances["at-bound"] == 5
    assert distances["too-far"] == 6
    assert distances["shorter"] == 1


def test_find_pivots_accepts_weight_values_without_forbidden_operations() -> None:
    graph = Graph()
    graph.add_vertex("z")
    graph.add_edge("s", "a", Weight(1))
    graph.add_edge("a", "b", Weight(1))
    distances = {"s": Weight(0), "z": Weight(0), "a": Weight(1)}

    result = find_pivots(
        graph,
        bound=Weight(3),
        sources=["z", "s"],
        distances=distances,
        k=2,
    )

    assert not result.saturated
    assert result.visited == ("s", "z", "a", "b")
    assert result.pivots == ("s",)
    assert distances["a"] == Weight(1)
    assert distances["b"] == Weight(2)


def test_find_pivots_validates_inputs() -> None:
    graph = Graph()
    graph.add_vertex("s")

    with pytest.raises(ValueError, match="k must be at least 1"):
        find_pivots(graph, bound=10, sources=["s"], distances={"s": 0}, k=0)

    with pytest.raises(ValueError, match="distance label"):
        find_pivots(graph, bound=10, sources=["s"], distances={}, k=1)

    with pytest.raises(ValueError, match="vertex in graph"):
        find_pivots(graph, bound=10, sources=["missing"], distances={"missing": 0}, k=1)

    result = FindPivots(graph, bound=10, sources=["s"], distances={"s": 0}, k=1)
    assert result.pivots == ("s",)
    assert result.layers == (("s",), ())
