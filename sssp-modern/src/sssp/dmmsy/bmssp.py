"""BMSSP recursion from DMMSY 2025 Algorithms 2 and 3.

`base_case` implements the bounded mini-Dijkstra routine used at recursion
level 0. `bmssp` implements the Algorithm 3 divide-and-conquer recursion using
FindPivots (Algorithm 1) and the Lemma 3.3 block list. Lemma 3.7 is the
correctness boundary: the returned vertices are complete below the returned
boundary under the paper's BMSSP preconditions.
"""

from __future__ import annotations

import heapq
from collections.abc import Iterable, MutableMapping
from dataclasses import dataclass
from itertools import count
from typing import Any

from sssp.dmmsy.blocklist import BlockList
from sssp.dmmsy.find_pivots import find_pivots
from sssp.graph import Graph, Vertex


@dataclass(frozen=True, slots=True)
class BMSSPResult:
    """Immutable result of `base_case()` or `bmssp()`."""

    bound: Any
    vertices: tuple[Vertex, ...]
    iterations: int
    partial: bool


def base_case(
    graph: Graph,
    bound: Any,
    sources: Iterable[Vertex],
    distances: MutableMapping[Vertex, Any],
    k: int,
    _graph_vertices: set[Vertex] | None = None,
) -> BMSSPResult:
    """Return DMMSY Algorithm 2 for singleton bounded source set `S`.

    The heap is the same lazy-deletion binary-heap pattern used by U2 Dijkstra,
    bounded by `B` and stopped once `k + 1` vertices have been found.
    """

    if k < 1:
        raise ValueError("k must be at least 1")

    source_tuple = _ordered_unique(sources)
    if len(source_tuple) != 1:
        raise ValueError("base_case requires exactly one source")

    source = source_tuple[0]
    graph_vertices = _graph_vertices if _graph_vertices is not None else set(graph.vertices())
    _validate_sources(graph_vertices, source_tuple, distances)

    completed: set[Vertex] = {source}
    completed_order: list[Vertex] = [source]
    settled: set[Vertex] = set()
    entry_order = count()
    heap: list[tuple[Any, int, Vertex]] = [
        (distances[source], next(entry_order), source)
    ]

    while heap and len(completed) < k + 1:
        current_distance, _, vertex = heapq.heappop(heap)
        if vertex in settled:
            continue
        if not distances[vertex] == current_distance:
            continue

        settled.add(vertex)
        _append_unique(vertex, completed, completed_order)

        for edge in graph.neighbors(vertex):
            candidate = distances[vertex] + edge.weight
            current = distances.get(edge.target, _MISSING)
            if not (_can_relax(candidate, current) and _below(candidate, bound)):
                continue

            distances[edge.target] = candidate
            heapq.heappush(heap, (candidate, next(entry_order), edge.target))

    if len(completed) <= k:
        return BMSSPResult(
            bound=bound,
            vertices=tuple(completed_order),
            iterations=len(settled),
            partial=False,
        )

    partial_bound = _max_label(completed_order, distances)
    return BMSSPResult(
        bound=partial_bound,
        vertices=tuple(
            vertex for vertex in completed_order if _below(distances[vertex], partial_bound)
        ),
        iterations=len(settled),
        partial=True,
    )


def bmssp(
    graph: Graph,
    level: int,
    bound: Any,
    sources: Iterable[Vertex],
    distances: MutableMapping[Vertex, Any],
    k: int,
    t: int,
    _graph_vertices: set[Vertex] | None = None,
) -> BMSSPResult:
    """Return DMMSY Algorithm 3 bounded multi-source shortest paths."""

    if level < 0:
        raise ValueError("level must be non-negative")
    if k < 1:
        raise ValueError("k must be at least 1")
    if t < 1:
        raise ValueError("t must be at least 1")

    source_tuple = _ordered_unique(sources)
    if not source_tuple:
        raise ValueError("sources must not be empty")
    graph_vertices = _graph_vertices if _graph_vertices is not None else set(graph.vertices())
    _validate_sources(graph_vertices, source_tuple, distances)

    if level == 0:
        return base_case(graph, bound, source_tuple, distances, k, graph_vertices)

    pivot_result = find_pivots(
        graph,
        bound,
        source_tuple,
        distances,
        k,
        _graph_vertices=graph_vertices,
    )
    pivots = pivot_result.pivots
    block_size = 2 ** ((level - 1) * t)
    workload_limit = k * (2 ** (level * t))
    blocklist = BlockList(
        block_size=block_size,
        upper_bound=bound,
        max_inserts=workload_limit,
    )

    for pivot in pivots:
        blocklist.insert(pivot, distances[pivot])

    boundary_prime = _min_label(pivots, distances, fallback=bound)
    completed: set[Vertex] = set()
    completed_order: list[Vertex] = []
    iterations = 0

    while len(completed) < workload_limit and not blocklist.is_empty():
        iterations += 1
        pulled = blocklist.pull()
        child = bmssp(
            graph,
            level - 1,
            pulled.bound,
            pulled.keys,
            distances,
            k,
            t,
            graph_vertices,
        )
        boundary_prime = child.bound
        for vertex in child.vertices:
            _append_unique(vertex, completed, completed_order)

        prepend_pairs: dict[Vertex, Any] = {}
        for vertex in child.vertices:
            for edge in graph.neighbors(vertex):
                candidate = distances[vertex] + edge.weight
                current = distances.get(edge.target, _MISSING)
                if not _can_relax(candidate, current):
                    continue

                distances[edge.target] = candidate
                if _in_half_open(candidate, pulled.bound, bound):
                    blocklist.insert(edge.target, candidate)
                elif _in_half_open(candidate, child.bound, pulled.bound):
                    _keep_smallest(prepend_pairs, edge.target, candidate)

        for key in pulled.keys:
            label = distances[key]
            if _in_half_open(label, child.bound, pulled.bound):
                _keep_smallest(prepend_pairs, key, label)

        blocklist.batch_prepend(prepend_pairs.items())

        if len(completed) > workload_limit:
            boundary_prime = child.bound
            break

    final_bound = boundary_prime if _below(boundary_prime, bound) else bound
    for vertex in pivot_result.visited:
        if vertex in distances and _below(distances[vertex], final_bound):
            _append_unique(vertex, completed, completed_order)

    return BMSSPResult(
        bound=final_bound,
        vertices=tuple(completed_order),
        iterations=iterations,
        partial=_below(final_bound, bound),
    )


def BaseCase(
    graph: Graph,
    bound: Any,
    sources: Iterable[Vertex],
    distances: MutableMapping[Vertex, Any],
    k: int,
) -> BMSSPResult:
    """Paper-named wrapper for `base_case`."""

    return base_case(graph, bound, sources, distances, k)


def BMSSP(
    graph: Graph,
    level: int,
    bound: Any,
    sources: Iterable[Vertex],
    distances: MutableMapping[Vertex, Any],
    k: int,
    t: int,
) -> BMSSPResult:
    """Paper-named wrapper for `bmssp`."""

    return bmssp(graph, level, bound, sources, distances, k, t)


_MISSING = object()


def _ordered_unique(vertices: Iterable[Vertex]) -> tuple[Vertex, ...]:
    seen: set[Vertex] = set()
    unique: list[Vertex] = []
    for vertex in sorted(vertices, key=repr):
        if vertex in seen:
            continue
        seen.add(vertex)
        unique.append(vertex)
    return tuple(unique)


def _validate_sources(
    graph_vertices: set[Vertex],
    sources: tuple[Vertex, ...],
    distances: MutableMapping[Vertex, Any],
) -> None:
    for source in sources:
        if source not in graph_vertices:
            raise ValueError("every source must be a vertex in graph")
        if source not in distances:
            raise ValueError("every source must have a distance label")


def _append_unique(
    vertex: Vertex,
    seen: set[Vertex],
    order: list[Vertex],
) -> None:
    if vertex in seen:
        return
    seen.add(vertex)
    order.append(vertex)


def _can_relax(candidate: Any, current: Any) -> bool:
    if current is _MISSING:
        return True
    return bool(candidate < current or candidate == current)


def _below(value: Any, bound: Any) -> bool:
    return bool(value < bound)


def _in_half_open(value: Any, lower: Any, upper: Any) -> bool:
    return bool((not value < lower) and value < upper)


def _keep_smallest(items: dict[Vertex, Any], vertex: Vertex, value: Any) -> None:
    current = items.get(vertex, _MISSING)
    if current is _MISSING or value < current:
        items[vertex] = value


def _max_label(vertices: Iterable[Vertex], distances: MutableMapping[Vertex, Any]) -> Any:
    maximum = _MISSING
    for vertex in vertices:
        label = distances[vertex]
        if maximum is _MISSING or maximum < label:
            maximum = label
    if maximum is _MISSING:
        raise ValueError("cannot compute maximum label of an empty vertex set")
    return maximum


def _min_label(
    vertices: Iterable[Vertex],
    distances: MutableMapping[Vertex, Any],
    fallback: Any,
) -> Any:
    minimum = _MISSING
    for vertex in vertices:
        label = distances[vertex]
        if minimum is _MISSING or label < minimum:
            minimum = label
    if minimum is _MISSING:
        return fallback
    return minimum
