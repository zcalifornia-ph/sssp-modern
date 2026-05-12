"""Dijkstra shortest paths for non-negative weighted graphs.

Dijkstra 1959, Problem 2 grows a settled set A of vertices whose minimum
distance from the source is known, and a frontier set B from which the next
minimum-distance vertex is selected. This module realizes that frontier with a
binary heap.
"""

from __future__ import annotations

import heapq
from itertools import count
from typing import Any

from sssp.graph import Graph, Vertex

Distances = dict[Vertex, Any]


def dijkstra(graph: Graph, source: Vertex) -> Distances:
    """Return reachable single-source distances using binary-heap Dijkstra.

    Preconditions:
    - `source` must be a vertex in `graph`.
    - edge weights must be non-negative and support `<` and `+`.

    Complexity:
    - Time: `O((n + m) log n)` with lazy deletion of stale heap entries.
    - Space: `O(n + m)` for distance labels, settled vertices, and queued
      tentative labels in the worst case.
    """

    if source not in set(graph.vertices()):
        raise ValueError("source must be a vertex in graph")

    distances: Distances = {source: 0.0}
    settled: set[Vertex] = set()
    entry_order = count()
    heap: list[tuple[Any, int, Vertex]] = [(0.0, next(entry_order), source)]

    while heap:
        current_distance, _, vertex = heapq.heappop(heap)
        if vertex in settled:
            continue

        settled.add(vertex)

        for edge in graph.neighbors(vertex):
            if edge.weight < 0:
                raise ValueError("Dijkstra requires non-negative edge weights")
            if edge.target in settled:
                continue

            tentative = current_distance + edge.weight
            if edge.target not in distances or tentative < distances[edge.target]:
                distances[edge.target] = tentative
                heapq.heappush(heap, (tentative, next(entry_order), edge.target))

    return distances
