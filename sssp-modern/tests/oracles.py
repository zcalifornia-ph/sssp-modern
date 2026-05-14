from __future__ import annotations

from collections.abc import Hashable

from sssp.graph import Graph


class OracleUnavailable(RuntimeError):
    """Raised when an optional test oracle dependency is not installed."""


def networkx_dijkstra_distances(graph: Graph, source: Hashable) -> dict[Hashable, float]:
    """Return Dijkstra distances through the optional NetworkX test oracle."""

    try:
        import networkx as nx
    except ImportError as exc:
        raise OracleUnavailable("NetworkX is not installed") from exc

    oracle_graph = nx.DiGraph() if graph.is_directed else nx.Graph()
    oracle_graph.add_nodes_from(graph.vertices())
    for edge in graph.edges():
        oracle_graph.add_edge(edge.source, edge.target, weight=edge.weight)

    return dict(nx.single_source_dijkstra_path_length(oracle_graph, source, weight="weight"))


def networkx_bellman_ford_distances(graph: Graph, source: Hashable) -> dict[Hashable, float]:
    """Return Bellman-Ford distances through the optional NetworkX test oracle."""

    try:
        import networkx as nx
    except ImportError as exc:
        raise OracleUnavailable("NetworkX is not installed") from exc

    oracle_graph = nx.DiGraph() if graph.is_directed else nx.Graph()
    oracle_graph.add_nodes_from(graph.vertices())
    for edge in graph.edges():
        oracle_graph.add_edge(edge.source, edge.target, weight=edge.weight)

    return dict(nx.single_source_bellman_ford_path_length(oracle_graph, source, weight="weight"))
