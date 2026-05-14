import pytest

from oracles import OracleUnavailable, networkx_bellman_ford_distances
from sssp.bellman_ford import bellman_ford
from sssp.generators import erdos_renyi_graph
from sssp.graph import Graph


def test_bellman_ford_matches_tiny_directed_golden_fixture(
    tiny_directed_graph,
    tiny_directed_expected_distances,
) -> None:
    distances, report = bellman_ford(
        tiny_directed_graph,
        tiny_directed_expected_distances["source"],
    )

    assert not report.has_cycle
    assert distances == tiny_directed_expected_distances["distances"]
    for vertex in tiny_directed_expected_distances["unreachable"]:
        assert vertex not in distances


@pytest.mark.parametrize("seed", [3, 7, 11])
def test_bellman_ford_agrees_with_networkx_on_seeded_random_graphs_when_available(
    seed,
) -> None:
    graph = erdos_renyi_graph(10, edge_probability=0.35, seed=seed)

    try:
        expected = networkx_bellman_ford_distances(graph, "v0")
    except OracleUnavailable as exc:
        pytest.skip(str(exc))

    distances, report = bellman_ford(graph, "v0")
    assert not report.has_cycle
    assert distances == expected


def test_bellman_ford_returns_only_isolated_source_when_no_edges() -> None:
    graph = Graph()
    graph.add_vertex("s")
    graph.add_vertex("isolated")

    distances, report = bellman_ford(graph, "s")
    assert not report.has_cycle
    assert distances == {"s": 0.0}


def test_bellman_ford_rejects_missing_source() -> None:
    graph = Graph.from_edges([("a", "b", 1.0)])

    with pytest.raises(ValueError, match="source"):
        bellman_ford(graph, "missing")


def test_bellman_ford_detects_reachable_negative_cycle() -> None:
    graph = Graph.from_edges([
        ("s", "a", 1.0),
        ("a", "b", 1.0),
        ("b", "c", -3.0),
        ("c", "a", 1.0),
        ("s", "isolated", 10.0)
    ])
    
    distances, report = bellman_ford(graph, "s")
    assert report.has_cycle


def test_bellman_ford_accepts_negative_edges_without_cycles() -> None:
    graph = Graph.from_edges([
        ("s", "a", 2.0),
        ("a", "b", -1.0),
        ("b", "c", 2.0),
    ])
    
    distances, report = bellman_ford(graph, "s")
    assert not report.has_cycle
    assert distances == {"s": 0.0, "a": 2.0, "b": 1.0, "c": 3.0}


def test_bellman_ford_ignores_unreachable_negative_cycle() -> None:
    graph = Graph.from_edges([
        ("s", "a", 1.0),
        ("x", "y", -1.0),
        ("y", "x", -1.0)
    ])
    
    distances, report = bellman_ford(graph, "s")
    assert not report.has_cycle
    assert distances == {"s": 0.0, "a": 1.0}
