from dataclasses import FrozenInstanceError

import pytest

from sssp.graph import Edge, Graph


def test_directed_graph_registers_vertices_and_one_arc() -> None:
    graph = Graph()

    graph.add_edge("a", "b", 2.5)

    assert graph.is_directed
    assert graph.vertices() == ("a", "b")
    assert graph.order() == 2
    assert graph.size() == 1
    assert graph.neighbors("a") == (Edge("a", "b", 2.5),)
    assert graph.neighbors("b") == ()
    assert graph.edges() == (Edge("a", "b", 2.5),)


def test_undirected_graph_stores_reciprocal_arcs() -> None:
    graph = Graph(directed=False)

    graph.add_edge("a", "b", 4)

    assert not graph.is_directed
    assert graph.size() == 2
    assert graph.neighbors("a") == (Edge("a", "b", 4),)
    assert graph.neighbors("b") == (Edge("b", "a", 4),)


def test_from_edges_accepts_edge_objects_and_tuples() -> None:
    graph = Graph.from_edges(
        [
            Edge("a", "b", 1),
            ("b", "c", 2),
            ("c", "d"),
        ]
    )

    assert graph.vertices() == ("a", "b", "c", "d")
    assert graph.edges() == (
        Edge("a", "b", 1),
        Edge("b", "c", 2),
        Edge("c", "d", 1.0),
    )


def test_query_results_are_immutable_snapshots() -> None:
    graph = Graph.from_edges([("a", "b", 1)])
    neighbors = graph.neighbors("a")
    edges = graph.edges()

    with pytest.raises(AttributeError):
        neighbors.append(Edge("a", "c", 2))
    with pytest.raises(AttributeError):
        edges.append(Edge("b", "c", 3))
    with pytest.raises(FrozenInstanceError):
        neighbors[0].weight = 99

    graph.add_edge("a", "c", 2)
    assert neighbors == (Edge("a", "b", 1),)


def test_graph_rejects_unhashable_vertices() -> None:
    graph = Graph()

    with pytest.raises(TypeError):
        graph.add_vertex(["list"])
    with pytest.raises(TypeError):
        graph.add_edge("a", {"set"}, 1)


def test_from_edges_rejects_malformed_tuples() -> None:
    with pytest.raises(ValueError):
        Graph.from_edges([("a",)])
    with pytest.raises(ValueError):
        Graph.from_edges([("a", "b", 1, "extra")])
