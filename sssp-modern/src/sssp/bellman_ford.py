"""Classic Bellman-Ford shortest paths for directed weighted graphs.

Bellman 1958 and Ford 1956. This algorithm computes shortest paths from a single
source vertex to all reachable vertices, and detects reachable negative cycles.
The relaxation loop runs in O(mn) time for m edges and n vertices.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sssp.graph import Graph, Vertex

Distances = dict[Vertex, Any]


@dataclass(frozen=True, slots=True)
class NegativeCycleReport:
    """Explicit report of whether a reachable negative cycle was detected.

    Attributes:
        has_cycle: True if a reachable negative cycle is detected, False otherwise.
    """
    has_cycle: bool


def bellman_ford(graph: Graph, source: Vertex) -> tuple[Distances, NegativeCycleReport]:
    """Return reachable single-source distances and a negative-cycle report.

    Preconditions:
    - `source` must be a vertex in `graph`.
    - Edge weights must support `<` and `+`.

    Complexity:
    - Time: `O(mn)` for the relaxation loop, where n is order and m is size.
    - Space: `O(n)` for distance labels.
    """

    if source not in set(graph.vertices()):
        raise ValueError("source must be a vertex in graph")

    distances: Distances = {source: 0.0}
    edges = graph.edges()
    n = graph.order()

    # Relax up to |V| - 1 times
    for _ in range(n - 1):
        updated = False
        for edge in edges:
            if edge.source in distances:
                tentative = distances[edge.source] + edge.weight
                if edge.target not in distances or tentative < distances[edge.target]:
                    distances[edge.target] = tentative
                    updated = True
        if not updated:
            break

    # Final pass to detect reachable negative cycles
    has_cycle = False
    for edge in edges:
        if edge.source in distances:
            tentative = distances[edge.source] + edge.weight
            if edge.target not in distances or tentative < distances[edge.target]:
                has_cycle = True
                break

    return distances, NegativeCycleReport(has_cycle=has_cycle)
