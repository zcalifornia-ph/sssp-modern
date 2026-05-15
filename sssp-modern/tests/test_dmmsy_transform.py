from sssp.dijkstra import dijkstra
from sssp.dmmsy import constant_degree_transform
from sssp.graph import Graph


def test_constant_degree_transform_preserves_tiny_directed_distances(
    tiny_directed_graph,
) -> None:
    transform = constant_degree_transform(tiny_directed_graph)

    original = dijkstra(tiny_directed_graph, "s")
    transformed = dijkstra(transform.graph, transform.representatives["s"])

    assert transform.project_distances(transformed) == original


def test_constant_degree_transform_bounds_indegree_and_outdegree() -> None:
    graph = Graph()
    for index in range(5):
        graph.add_edge("s", f"out-{index}", index + 1)
        graph.add_edge(f"in-{index}", "s", index + 2)
    graph.add_edge("s", "out-0", 9)

    transform = constant_degree_transform(graph)
    indegree, outdegree = _degree_maps(transform.graph)

    assert max(indegree.values()) <= 2
    assert max(outdegree.values()) <= 2


def test_constant_degree_transform_preserves_high_degree_distances() -> None:
    graph = Graph.from_edges(
        [
            ("s", "a", 4.0),
            ("s", "b", 2.0),
            ("s", "c", 7.0),
            ("a", "t", 4.0),
            ("b", "t", 3.0),
            ("c", "t", 1.0),
            ("t", "z", 2.0),
        ]
    )

    transform = constant_degree_transform(graph)
    original = dijkstra(graph, "s")
    transformed = dijkstra(transform.graph, transform.representatives["s"])

    assert transform.project_distances(transformed) == original


def test_constant_degree_transform_preserves_isolated_source_reachability() -> None:
    graph = Graph()
    graph.add_vertex("s")
    graph.add_vertex("isolated")

    transform = constant_degree_transform(graph)
    transformed = dijkstra(transform.graph, transform.representatives["s"])

    assert set(transform.representatives) == {"s", "isolated"}
    assert transform.project_distances(transformed) == {"s": 0.0}


def _degree_maps(graph: Graph) -> tuple[dict[object, int], dict[object, int]]:
    indegree = {vertex: 0 for vertex in graph.vertices()}
    outdegree = {vertex: 0 for vertex in graph.vertices()}
    for edge in graph.edges():
        outdegree[edge.source] += 1
        indegree[edge.target] += 1
    return indegree, outdegree
