import json

import pytest

from sssp.graph import Edge, Graph
from sssp.io import (
    ADJACENCY_LIST_FORMAT,
    EDGE_LIST_FORMAT,
    graph_from_adjacency_list_data,
    graph_from_edge_list_data,
    graph_to_adjacency_list_data,
    graph_to_edge_list_data,
    read_adjacency_list,
    read_edge_list,
    write_adjacency_list,
    write_edge_list,
)
from sssp.weights import Weight


def test_edge_list_round_trip_preserves_directed_graph(tmp_path) -> None:
    graph = _sample_directed_graph()
    path = tmp_path / "graph.edge-list.json"

    write_edge_list(graph, path)
    loaded = read_edge_list(path)

    _assert_graph_equal(loaded, graph)
    assert json.loads(path.read_text(encoding="utf-8")) == graph_to_edge_list_data(graph)


def test_adjacency_list_round_trip_preserves_directed_graph(tmp_path) -> None:
    graph = _sample_directed_graph()
    path = tmp_path / "graph.adjacency-list.json"

    write_adjacency_list(graph, path)
    loaded = read_adjacency_list(path)

    _assert_graph_equal(loaded, graph)
    assert json.loads(path.read_text(encoding="utf-8")) == graph_to_adjacency_list_data(graph)


def test_round_trip_preserves_undirected_graph_without_duplicate_logical_edges(tmp_path) -> None:
    graph = Graph(directed=False)
    graph.add_edge("a", "b", 3)
    edge_list_path = tmp_path / "undirected.edge-list.json"
    adjacency_path = tmp_path / "undirected.adjacency-list.json"

    write_edge_list(graph, edge_list_path)
    write_adjacency_list(graph, adjacency_path)

    assert graph_to_edge_list_data(graph)["edges"] == [
        {"source": "a", "target": "b", "weight": 3}
    ]
    assert graph_to_adjacency_list_data(graph)["adjacency"] == {
        "a": [{"target": "b", "weight": 3}],
        "b": [],
    }
    _assert_graph_equal(read_edge_list(edge_list_path), graph)
    _assert_graph_equal(read_adjacency_list(adjacency_path), graph)


def test_sample_fixtures_load_to_expected_graph() -> None:
    expected = _sample_directed_graph()

    edge_list = read_edge_list("examples/graphs/tiny-directed.edge-list.json")
    adjacency_list = read_adjacency_list("examples/graphs/tiny-directed.adjacency-list.json")

    _assert_graph_equal(edge_list, expected)
    _assert_graph_equal(adjacency_list, expected)


def test_data_converters_support_weight_values_for_fixture_output() -> None:
    graph = Graph.from_edges([("s", "t", Weight(2.5))])

    assert graph_to_edge_list_data(graph)["edges"] == [
        {"source": "s", "target": "t", "weight": 2.5}
    ]
    assert graph_to_adjacency_list_data(graph)["adjacency"] == {
        "s": [{"target": "t", "weight": 2.5}],
        "t": [],
    }


@pytest.mark.parametrize(
    "data, error",
    [
        ({"format": "wrong", "directed": True, "vertices": [], "edges": []}, ValueError),
        ({"format": EDGE_LIST_FORMAT, "directed": "yes", "vertices": [], "edges": []}, TypeError),
        ({"format": EDGE_LIST_FORMAT, "directed": True, "vertices": ["a", "a"], "edges": []}, ValueError),
        (
            {
                "format": EDGE_LIST_FORMAT,
                "directed": True,
                "vertices": ["a"],
                "edges": [{"source": "a", "target": "b", "weight": 1}],
            },
            ValueError,
        ),
        (
            {
                "format": EDGE_LIST_FORMAT,
                "directed": True,
                "vertices": ["a", "b"],
                "edges": [{"source": "a", "target": "b", "weight": "1"}],
            },
            TypeError,
        ),
    ],
)
def test_edge_list_validation_fails_fast(data, error) -> None:
    with pytest.raises(error):
        graph_from_edge_list_data(data)


@pytest.mark.parametrize(
    "data, error",
    [
        ({"format": "wrong", "directed": True, "adjacency": {}}, ValueError),
        ({"format": ADJACENCY_LIST_FORMAT, "directed": True, "adjacency": []}, TypeError),
        ({"format": ADJACENCY_LIST_FORMAT, "directed": True, "adjacency": {"a": "b"}}, TypeError),
        (
            {
                "format": ADJACENCY_LIST_FORMAT,
                "directed": True,
                "adjacency": {"a": [{"target": "b", "weight": 1}]},
            },
            ValueError,
        ),
        (
            {
                "format": ADJACENCY_LIST_FORMAT,
                "directed": True,
                "adjacency": {"a": [{"target": "a", "weight": False}]},
            },
            TypeError,
        ),
    ],
)
def test_adjacency_list_validation_fails_fast(data, error) -> None:
    with pytest.raises(error):
        graph_from_adjacency_list_data(data)


def test_non_string_vertices_are_rejected_for_portable_fixtures() -> None:
    graph = Graph.from_edges([(1, 2, 3)])

    with pytest.raises(TypeError):
        graph_to_edge_list_data(graph)
    with pytest.raises(TypeError):
        graph_to_adjacency_list_data(graph)


def _sample_directed_graph() -> Graph:
    graph = Graph.from_edges(
        [
            ("s", "a", 1.0),
            ("s", "b", 4.5),
            ("a", "b", 2.0),
        ]
    )
    graph.add_vertex("isolated")
    return graph


def _assert_graph_equal(actual: Graph, expected: Graph) -> None:
    assert actual.is_directed == expected.is_directed
    assert actual.vertices() == expected.vertices()
    assert actual.edges() == expected.edges()
