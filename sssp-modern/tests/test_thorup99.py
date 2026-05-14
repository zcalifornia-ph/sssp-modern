import pytest

from oracles import OracleUnavailable, networkx_dijkstra_distances
from sssp.generators import erdos_renyi_graph
from sssp.graph import Graph
from sssp.thorup99 import thorup_sssp


def test_thorup_matches_tiny_undirected_golden_fixture(
    tiny_undirected_graph,
    tiny_undirected_expected_distances,
) -> None:
    # Add a completely isolated vertex to test unreachable vertices
    tiny_undirected_graph.add_vertex("completely_isolated")

    distances = thorup_sssp(
        tiny_undirected_graph,
        tiny_undirected_expected_distances["source"],
    )

    assert distances == tiny_undirected_expected_distances["distances"]
    for vertex in tiny_undirected_expected_distances["unreachable"]:
        assert vertex not in distances


@pytest.mark.parametrize("seed", [3, 7, 11])
def test_thorup_agrees_with_networkx_on_seeded_random_graphs_when_available(
    seed,
) -> None:
    graph = erdos_renyi_graph(10, edge_probability=0.35, seed=seed, directed=False)
    # the generator produces float weights, so we need to add integer weights
    # Let's just create our own random integer graph or overwrite weights
    int_graph = Graph(directed=False)
    for v in graph.vertices():
        int_graph.add_vertex(v)
    for edge in graph.edges():
        if edge.source < edge.target:
            # deterministic weight based on node names
            w = (hash(edge.source) ^ hash(edge.target)) % 100
            int_graph.add_edge(edge.source, edge.target, w)
            
    try:
        expected = networkx_dijkstra_distances(int_graph, "v0")
    except OracleUnavailable as exc:
        pytest.skip(str(exc))

    assert thorup_sssp(int_graph, "v0") == expected


def test_thorup_returns_only_isolated_source_when_no_edges() -> None:
    graph = Graph(directed=False)
    graph.add_vertex("s")
    graph.add_vertex("isolated")

    assert thorup_sssp(graph, "s") == {"s": 0}


def test_thorup_rejects_missing_source() -> None:
    graph = Graph.from_edges([("a", "b", 1)], directed=False)

    with pytest.raises(ValueError, match="source"):
        thorup_sssp(graph, "missing")


def test_thorup_rejects_directed_graph() -> None:
    graph = Graph.from_edges([("a", "b", 1)], directed=True)

    with pytest.raises(ValueError, match="undirected"):
        thorup_sssp(graph, "a")


def test_thorup_rejects_negative_edges() -> None:
    graph = Graph.from_edges([("s", "a", 1), ("a", "b", -2)], directed=False)

    with pytest.raises(ValueError, match="non-negative"):
        thorup_sssp(graph, "s")


def test_thorup_rejects_negative_edges_in_unreachable_components() -> None:
    graph = Graph.from_edges([("s", "a", 1), ("x", "y", -2)], directed=False)

    with pytest.raises(ValueError, match="non-negative"):
        thorup_sssp(graph, "s")


def test_thorup_rejects_non_integer_edges() -> None:
    graph = Graph.from_edges([("s", "a", 1.5)], directed=False)

    with pytest.raises(ValueError, match="integer"):
        thorup_sssp(graph, "s")


def test_thorup_rejects_non_integer_edges_in_unreachable_components() -> None:
    graph = Graph.from_edges([("s", "a", 1), ("x", "y", 1.5)], directed=False)

    with pytest.raises(ValueError, match="integer"):
        thorup_sssp(graph, "s")
