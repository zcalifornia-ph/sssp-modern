from __future__ import annotations

from itertools import pairwise

import pytest

from sssp import astar as exported_astar
from sssp import manhattan as exported_manhattan
from sssp import zero as exported_zero
from sssp.astar import astar
from sssp.dijkstra import dijkstra
from sssp.graph import Graph
from sssp.heuristics import manhattan, zero


@pytest.mark.parametrize("goal", ["s", "a", "b", "c", "d"])
def test_astar_zero_heuristic_matches_dijkstra_target_distance(goal) -> None:
    graph = _weighted_directed_graph()
    expected_distances = dijkstra(graph, "s")

    path = astar(graph, "s", goal, zero)

    assert path[0] == "s"
    assert path[-1] == goal
    assert _path_cost(graph, path) == expected_distances[goal]


def test_astar_returns_empty_path_for_unreachable_goal_and_skips_stale_entries() -> None:
    graph = Graph.from_edges(
        [
            ("s", "a", 5.0),
            ("s", "b", 1.0),
            ("b", "a", 1.0),
        ]
    )
    graph.add_vertex("goal")

    assert astar(graph, "s", "goal", zero) == []


def test_astar_returns_source_only_path_when_source_is_goal() -> None:
    graph = Graph()
    graph.add_vertex("s")

    assert astar(graph, "s", "s", zero) == ["s"]


def test_astar_rejects_missing_source_or_goal() -> None:
    graph = Graph.from_edges([("s", "a", 1.0)])

    with pytest.raises(ValueError, match="source"):
        astar(graph, "missing", "a", zero)

    with pytest.raises(ValueError, match="goal"):
        astar(graph, "s", "missing", zero)


def test_astar_rejects_negative_edges() -> None:
    graph = Graph.from_edges([("s", "a", 1.0), ("a", "goal", -2.0)])

    with pytest.raises(ValueError, match="non-negative"):
        astar(graph, "s", "goal", zero)


def test_manhattan_is_admissible_on_grid_demo() -> None:
    graph = _grid_graph(width=3, height=3)
    goal = (2, 2)

    for vertex in graph.vertices():
        assert manhattan(vertex, goal) <= dijkstra(graph, vertex)[goal]

    path = astar(graph, (0, 0), goal, manhattan)

    assert path[0] == (0, 0)
    assert path[-1] == goal
    assert _path_cost(graph, path) == 4.0
    assert len(path) == 5


def test_manhattan_rejects_non_grid_points() -> None:
    with pytest.raises(TypeError, match="2D grid point"):
        manhattan("0,0", (1, 1))

    with pytest.raises(TypeError, match="exactly two"):
        manhattan((0,), (1, 1))

    with pytest.raises(TypeError, match="real numbers"):
        manhattan((True, 0), (1, 1))


def test_astar_and_heuristics_are_exported_from_package() -> None:
    assert exported_astar is astar
    assert exported_zero is zero
    assert exported_manhattan is manhattan


def _weighted_directed_graph() -> Graph:
    graph = Graph.from_edges(
        [
            ("s", "a", 1.0),
            ("s", "b", 4.0),
            ("a", "b", 2.0),
            ("a", "c", 5.0),
            ("b", "c", 1.0),
            ("c", "d", 3.0),
            ("b", "d", 7.0),
            ("a", "d", 10.0),
        ]
    )
    graph.add_vertex("isolated")
    return graph


def _grid_graph(width: int, height: int) -> Graph:
    graph = Graph(directed=False)
    for x in range(width):
        for y in range(height):
            vertex = (x, y)
            graph.add_vertex(vertex)
            if x > 0:
                graph.add_edge((x - 1, y), vertex, 1.0)
            if y > 0:
                graph.add_edge((x, y - 1), vertex, 1.0)
    return graph


def _path_cost(graph: Graph, path: list[object]) -> float:
    total = 0.0
    for source, target in pairwise(path):
        for edge in graph.neighbors(source):
            if edge.target == target:
                total += edge.weight
                break
        else:
            raise AssertionError(f"path uses missing edge {source!r} -> {target!r}")
    return total
