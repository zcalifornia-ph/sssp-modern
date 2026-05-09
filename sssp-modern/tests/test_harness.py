import pytest

from oracles import OracleUnavailable, networkx_dijkstra_distances
from sssp.graph import Edge


def test_project_root_and_golden_dir_fixtures(project_root, golden_dir) -> None:
    assert (project_root / "src" / "sssp").is_dir()
    assert golden_dir == project_root / "tests" / "golden"
    assert (golden_dir / "tiny-directed.edge-list.json").is_file()


def test_tiny_directed_graph_fixture_loads_expected_graph(tiny_directed_graph) -> None:
    assert tiny_directed_graph.is_directed
    assert tiny_directed_graph.vertices() == ("s", "a", "b", "isolated")
    assert tiny_directed_graph.edges() == (
        Edge("s", "a", 1.0),
        Edge("s", "b", 4.5),
        Edge("a", "b", 2.0),
    )


def test_tiny_directed_distance_fixture_loads_expected_mapping(
    tiny_directed_expected_distances,
) -> None:
    assert tiny_directed_expected_distances == {
        "source": "s",
        "distances": {"s": 0.0, "a": 1.0, "b": 3.0},
        "unreachable": ["isolated"],
    }


def test_networkx_oracle_matches_tiny_directed_distances_when_available(
    tiny_directed_graph,
    tiny_directed_expected_distances,
) -> None:
    try:
        distances = networkx_dijkstra_distances(
            tiny_directed_graph,
            tiny_directed_expected_distances["source"],
        )
    except OracleUnavailable as exc:
        pytest.skip(str(exc))

    assert distances == tiny_directed_expected_distances["distances"]
    assert "isolated" not in distances
