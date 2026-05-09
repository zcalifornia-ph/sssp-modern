import random

import pytest

from sssp.generators import (
    barabasi_albert_graph,
    dag_graph,
    erdos_renyi_graph,
    random_geometric_graph,
    signed_edge_graph,
)
from sssp.graph import Graph


@pytest.mark.parametrize(
    "factory,args",
    [
        (erdos_renyi_graph, (8, 0.35, 11)),
        (random_geometric_graph, (8, 0.45, 11)),
        (dag_graph, (8, 0.35, 11)),
        (barabasi_albert_graph, (8, 2, 11)),
        (signed_edge_graph, (8, 0.35, 11)),
    ],
)
def test_generators_are_deterministic_with_fixed_seed(factory, args) -> None:
    first = factory(*args)
    second = factory(*args)

    assert _signature(first) == _signature(second)


def test_generators_do_not_mutate_global_random_state() -> None:
    random.seed(123)
    before = random.random()

    erdos_renyi_graph(6, 0.5, seed=99)
    random_geometric_graph(6, 0.5, seed=99)
    dag_graph(6, 0.5, seed=99)
    barabasi_albert_graph(6, 2, seed=99)
    signed_edge_graph(6, 0.5, seed=99)

    after = random.random()
    random.seed(123)
    assert before == random.random()
    assert after == random.random()


def test_erdos_renyi_respects_probability_extremes_and_directedness() -> None:
    empty = erdos_renyi_graph(4, 0.0, seed=1)
    complete_directed = erdos_renyi_graph(4, 1.0, seed=1)
    complete_undirected = erdos_renyi_graph(4, 1.0, seed=1, directed=False)

    assert empty.vertices() == ("v0", "v1", "v2", "v3")
    assert empty.edges() == ()
    assert complete_directed.is_directed
    assert complete_directed.size() == 12
    assert not complete_undirected.is_directed
    assert complete_undirected.size() == 12
    _assert_no_self_loops(complete_directed)
    _assert_no_self_loops(complete_undirected)


def test_random_geometric_graph_uses_distance_weights_by_default() -> None:
    graph = random_geometric_graph(5, radius=2.0, seed=7)

    assert not graph.is_directed
    assert graph.vertices() == ("v0", "v1", "v2", "v3", "v4")
    assert graph.size() == 20
    assert all(edge.weight >= 0 for edge in graph.edges())
    _assert_no_self_loops(graph)


def test_random_geometric_graph_can_emit_directed_symmetric_arcs() -> None:
    graph = random_geometric_graph(4, radius=2.0, seed=7, directed=True)

    assert graph.is_directed
    assert graph.size() == 12
    for edge in graph.edges():
        assert any(
            reverse.source == edge.target
            and reverse.target == edge.source
            and reverse.weight == edge.weight
            for reverse in graph.edges()
        )


def test_dag_graph_only_emits_forward_edges() -> None:
    graph = dag_graph(8, 1.0, seed=4)

    assert graph.is_directed
    assert graph.size() == 28
    for edge in graph.edges():
        assert int(edge.source[1:]) < int(edge.target[1:])


def test_barabasi_albert_graph_has_expected_undirected_shape() -> None:
    graph = barabasi_albert_graph(8, attachments=2, seed=5)

    assert not graph.is_directed
    assert graph.vertices() == tuple(f"v{i}" for i in range(8))
    assert graph.size() == 26
    _assert_no_self_loops(graph)
    assert all(edge.weight >= 1.0 for edge in graph.edges())


def test_signed_edge_graph_can_emit_positive_and_negative_weights() -> None:
    graph = signed_edge_graph(
        8,
        edge_probability=1.0,
        seed=4,
        negative_fraction=0.5,
        acyclic=True,
    )
    weights = [edge.weight for edge in graph.edges()]

    assert graph.is_directed
    assert graph.size() == 28
    assert any(weight < 0 for weight in weights)
    assert any(weight > 0 for weight in weights)
    for edge in graph.edges():
        assert int(edge.source[1:]) < int(edge.target[1:])


@pytest.mark.parametrize(
    "call",
    [
        lambda: erdos_renyi_graph(-1, 0.5, seed=1),
        lambda: erdos_renyi_graph(4, 1.5, seed=1),
        lambda: random_geometric_graph(4, -1.0, seed=1),
        lambda: dag_graph(4, -0.1, seed=1),
        lambda: barabasi_albert_graph(4, 0, seed=1),
        lambda: barabasi_albert_graph(4, 4, seed=1),
        lambda: signed_edge_graph(4, 0.5, seed=1, negative_fraction=2.0),
        lambda: signed_edge_graph(4, 0.5, seed=1, weight_range=(10.0, 1.0)),
    ],
)
def test_generators_validate_parameters(call) -> None:
    with pytest.raises(ValueError):
        call()


def _signature(graph: Graph) -> tuple[bool, tuple[object, ...], tuple[object, ...]]:
    return (graph.is_directed, graph.vertices(), graph.edges())


def _assert_no_self_loops(graph: Graph) -> None:
    assert all(edge.source != edge.target for edge in graph.edges())
