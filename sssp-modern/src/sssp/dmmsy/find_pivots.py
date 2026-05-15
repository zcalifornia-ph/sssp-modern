"""FindPivots from DMMSY 2025 Algorithm 1 / Lemma 3.2.

The procedure is the BMSSP shrink step: from a bounded source set `S`, perform
`k` Bellman-Ford-like relaxation layers, collect the visited set `W`, and
return either all sources when the work grows too large or the source roots
whose accepted-relaxation trees contain at least `k` vertices.

The paper's tight-edge forest relies on its graph assumptions. This module
keeps a deterministic predecessor forest from accepted relaxations so tests and
later BMSSP code can inspect the same pivot boundary without adding a separate
forest-construction subsystem.
"""

from __future__ import annotations

from collections.abc import Iterable, MutableMapping
from dataclasses import dataclass
from typing import Any

from sssp.graph import Graph, Vertex


@dataclass(frozen=True, slots=True)
class FindPivotsResult:
    """Immutable result of `find_pivots()`."""

    pivots: tuple[Vertex, ...]
    visited: tuple[Vertex, ...]
    layers: tuple[tuple[Vertex, ...], ...]
    saturated: bool


def find_pivots(
    graph: Graph,
    bound: Any,
    sources: Iterable[Vertex],
    distances: MutableMapping[Vertex, Any],
    k: int,
) -> FindPivotsResult:
    """Return DMMSY Algorithm 1 pivots and visited vertices.

    Parameters:
    - `bound` is the paper's `B`; only candidates strictly below it enter a
      later frontier layer.
    - `sources` is the paper's `S`; every source must already have a distance
      label.
    - `distances` is the mutable `d` label map shared with later BMSSP phases.
    - `k` is the global DMMSY relaxation/pivot parameter and must be positive.

    The relaxation predicate mirrors the paper's `d[u] + w_uv <= d[v]` without
    using Python's `<=`, preserving compatibility with `Weight`.
    """

    if k < 1:
        raise ValueError("k must be at least 1")

    source_tuple = _ordered_unique(sources)
    if not source_tuple:
        raise ValueError("sources must not be empty")

    graph_vertices = set(graph.vertices())
    for source in source_tuple:
        if source not in graph_vertices:
            raise ValueError("every source must be a vertex in graph")
        if source not in distances:
            raise ValueError("every source must have a distance label")

    source_set = set(source_tuple)
    visited_set = set(source_tuple)
    visited_order = list(source_tuple)
    previous_layer = source_tuple
    layers: list[tuple[Vertex, ...]] = [source_tuple]
    parents: dict[Vertex, Vertex] = {}

    for _ in range(k):
        current_layer: list[Vertex] = []
        current_seen: set[Vertex] = set()

        for vertex in previous_layer:
            for edge in graph.neighbors(vertex):
                candidate = distances[vertex] + edge.weight
                current = distances.get(edge.target, _MISSING)
                if not _can_relax(candidate, current):
                    continue

                _record_relaxation(edge.source, edge.target, candidate, current, distances, parents, source_set)
                if not _below_bound(candidate, bound):
                    continue

                _append_unique(current_layer, current_seen, edge.target)
                if edge.target not in visited_set:
                    visited_set.add(edge.target)
                    visited_order.append(edge.target)

        layer_tuple = tuple(current_layer)
        layers.append(layer_tuple)

        if len(visited_set) > k * len(source_tuple):
            return FindPivotsResult(
                pivots=source_tuple,
                visited=tuple(visited_order),
                layers=tuple(layers),
                saturated=True,
            )

        previous_layer = layer_tuple

    subtree_sizes = _subtree_sizes(parents, source_tuple, visited_set)
    pivots = tuple(source for source in source_tuple if subtree_sizes[source] >= k)
    return FindPivotsResult(
        pivots=pivots,
        visited=tuple(visited_order),
        layers=tuple(layers),
        saturated=False,
    )


def FindPivots(
    graph: Graph,
    bound: Any,
    sources: Iterable[Vertex],
    distances: MutableMapping[Vertex, Any],
    k: int,
) -> FindPivotsResult:
    """Paper-named wrapper for `find_pivots()`."""

    return find_pivots(graph, bound, sources, distances, k)


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


def _can_relax(candidate: Any, current: Any) -> bool:
    if current is _MISSING:
        return True
    return bool(candidate < current or candidate == current)


def _below_bound(candidate: Any, bound: Any) -> bool:
    return bool(candidate < bound)


def _record_relaxation(
    source: Vertex,
    target: Vertex,
    candidate: Any,
    current: Any,
    distances: MutableMapping[Vertex, Any],
    parents: dict[Vertex, Vertex],
    source_set: set[Vertex],
) -> None:
    is_new_label = current is _MISSING
    is_strict_improvement = (not is_new_label) and bool(candidate < current)
    distances[target] = candidate

    if target in source_set:
        return

    if is_new_label or is_strict_improvement or target not in parents:
        parents[target] = source


def _append_unique(
    layer: list[Vertex],
    seen: set[Vertex],
    vertex: Vertex,
) -> None:
    if vertex in seen:
        return
    seen.add(vertex)
    layer.append(vertex)


def _subtree_sizes(
    parents: dict[Vertex, Vertex],
    roots: tuple[Vertex, ...],
    visited: set[Vertex],
) -> dict[Vertex, int]:
    children: dict[Vertex, list[Vertex]] = {vertex: [] for vertex in visited}
    for child, parent in parents.items():
        if child not in visited or parent not in visited or child == parent:
            continue
        children.setdefault(parent, []).append(child)

    return {root: _subtree_size(root, children) for root in roots}


def _subtree_size(root: Vertex, children: dict[Vertex, list[Vertex]]) -> int:
    total = 0
    seen: set[Vertex] = set()
    stack = [root]
    while stack:
        vertex = stack.pop()
        if vertex in seen:
            continue
        seen.add(vertex)
        total += 1
        stack.extend(reversed(children.get(vertex, ())))
    return total
