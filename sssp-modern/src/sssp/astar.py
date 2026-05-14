"""A* shortest path for non-negative weighted graphs.

Hart, Nilsson, and Raphael 1968 define A* with `g` as the known path cost,
`h` as the estimated remaining cost, and `f = g + h` as the frontier priority.
This module implements that goal-directed search with a binary heap.
"""

from __future__ import annotations

import heapq
from collections.abc import Callable
from itertools import count
from typing import Any

from sssp.graph import Graph, Vertex
from sssp.heuristics import zero

Path = list[Vertex]
Heuristic = Callable[[Vertex, Vertex], Any]


def astar(
    graph: Graph,
    source: Vertex,
    goal: Vertex,
    heuristic: Heuristic = zero,
) -> Path:
    """Return one shortest path from `source` to `goal` using A*.

    Preconditions:
    - `source` and `goal` must be vertices in `graph`.
    - edge weights must be non-negative and support `<` and `+`.
    - optimality depends on the supplied heuristic being admissible.

    Complexity:
    - Time: `O((n + m) log n)` in the worst case with heap-based frontier
      management and lazy deletion of stale entries.
    - Space: `O(n + m)` for score maps, predecessor links, and queued entries.
    """

    vertices = set(graph.vertices())
    if source not in vertices:
        raise ValueError("source must be a vertex in graph")
    if goal not in vertices:
        raise ValueError("goal must be a vertex in graph")

    came_from: dict[Vertex, Vertex] = {}
    g_score: dict[Vertex, Any] = {source: 0.0}
    entry_order = count()
    frontier: list[tuple[Any, int, Any, Vertex]] = [
        (heuristic(source, goal), next(entry_order), 0.0, source)
    ]

    while frontier:
        _, _, queued_g_score, vertex = heapq.heappop(frontier)
        if queued_g_score != g_score.get(vertex):
            continue
        if vertex == goal:
            return _reconstruct_path(came_from, source, goal)

        for edge in graph.neighbors(vertex):
            if edge.weight < 0:
                raise ValueError("A* requires non-negative edge weights")

            tentative_g_score = queued_g_score + edge.weight
            if edge.target not in g_score or tentative_g_score < g_score[edge.target]:
                came_from[edge.target] = vertex
                g_score[edge.target] = tentative_g_score
                f_score = tentative_g_score + heuristic(edge.target, goal)
                heapq.heappush(
                    frontier,
                    (f_score, next(entry_order), tentative_g_score, edge.target),
                )

    return []


def _reconstruct_path(
    came_from: dict[Vertex, Vertex],
    source: Vertex,
    goal: Vertex,
) -> Path:
    path = [goal]
    while path[-1] != source:
        path.append(came_from[path[-1]])
    path.reverse()
    return path
