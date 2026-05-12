import pytest

from oracles import OracleUnavailable, networkx_dijkstra_distances
from sssp.dijkstra import dijkstra
from sssp.generators import erdos_renyi_graph
from sssp.graph import Graph


def test_dijkstra_matches_tiny_directed_golden_fixture(
    tiny_directed_graph,
    tiny_directed_expected_distances,
) -> None:
    distances = dijkstra(
        tiny_directed_graph,
        tiny_directed_expected_distances["source"],
    )

    assert distances == tiny_directed_expected_distances["distances"]
    for vertex in tiny_directed_expected_distances["unreachable"]:
        assert vertex not in distances


@pytest.mark.parametrize("seed", [3, 7, 11])
def test_dijkstra_agrees_with_networkx_on_seeded_random_graphs_when_available(
    seed,
) -> None:
    graph = erdos_renyi_graph(10, edge_probability=0.35, seed=seed)

    try:
        expected = networkx_dijkstra_distances(graph, "v0")
    except OracleUnavailable as exc:
        pytest.skip(str(exc))

    assert dijkstra(graph, "v0") == expected


def test_dijkstra_returns_only_isolated_source_when_no_edges() -> None:
    graph = Graph()
    graph.add_vertex("s")
    graph.add_vertex("isolated")

    assert dijkstra(graph, "s") == {"s": 0.0}


def test_dijkstra_rejects_missing_source() -> None:
    graph = Graph.from_edges([("a", "b", 1.0)])

    with pytest.raises(ValueError, match="source"):
        dijkstra(graph, "missing")


def test_dijkstra_rejects_negative_edges() -> None:
    graph = Graph.from_edges([("s", "a", 1.0), ("a", "b", -2.0)])

    with pytest.raises(ValueError, match="non-negative"):
        dijkstra(graph, "s")
