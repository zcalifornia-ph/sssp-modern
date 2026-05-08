"""Weighted graph primitives for the SSSP study.

The representation is intentionally small: an adjacency-list graph with
immutable Edge records. This matches the graph model shared by the SSSP papers
in the portfolio, including the directed weighted graph model in DMMSY 2025,
section 2.
"""

from __future__ import annotations

from collections.abc import Hashable, Iterable
from dataclasses import dataclass
from typing import Any

Vertex = Hashable


@dataclass(frozen=True, slots=True)
class Edge:
    """One traversable weighted arc from `source` to `target`."""

    source: Vertex
    target: Vertex
    weight: Any = 1.0

    def __post_init__(self) -> None:
        _require_hashable(self.source, "source")
        _require_hashable(self.target, "target")


class Graph:
    """Adjacency-list graph for shortest-path algorithms.

    Directed graphs store each inserted edge as one traversable arc.
    Undirected graphs store reciprocal arcs so algorithms can iterate neighbors
    without a separate adapter.
    """

    def __init__(self, directed: bool = True) -> None:
        self._directed = bool(directed)
        self._adjacency: dict[Vertex, list[Edge]] = {}
        self._edge_count = 0

    @classmethod
    def from_edges(
        cls,
        edges: Iterable[Edge | tuple[Vertex, Vertex] | tuple[Vertex, Vertex, Any]],
        directed: bool = True,
    ) -> Graph:
        """Build a graph from Edge objects or `(source, target[, weight])` tuples."""

        graph = cls(directed=directed)
        for edge in edges:
            if isinstance(edge, Edge):
                graph.add_edge(edge.source, edge.target, edge.weight)
                continue

            try:
                parts = tuple(edge)
            except TypeError as exc:
                raise TypeError("edge tuples must be iterable") from exc

            if len(parts) == 2:
                source, target = parts
                weight = 1.0
            elif len(parts) == 3:
                source, target, weight = parts
            else:
                raise ValueError("edge tuples must have 2 or 3 values")

            graph.add_edge(source, target, weight)
        return graph

    @property
    def is_directed(self) -> bool:
        """Return whether this graph stores only explicitly directed arcs."""

        return self._directed

    def add_vertex(self, vertex: Vertex) -> None:
        """Register a vertex if it is not already present."""

        _require_hashable(vertex, "vertex")
        self._adjacency.setdefault(vertex, [])

    def add_edge(self, source: Vertex, target: Vertex, weight: Any = 1.0) -> None:
        """Add a weighted edge and register both endpoints."""

        self.add_vertex(source)
        self.add_vertex(target)
        self._append_edge(source, target, weight)
        if not self._directed:
            self._append_edge(target, source, weight)

    def vertices(self) -> tuple[Vertex, ...]:
        """Return vertices in insertion order."""

        return tuple(self._adjacency)

    def neighbors(self, vertex: Vertex) -> tuple[Edge, ...]:
        """Return outgoing arcs for `vertex`, or an empty tuple if absent."""

        _require_hashable(vertex, "vertex")
        return tuple(self._adjacency.get(vertex, ()))

    def edges(self) -> tuple[Edge, ...]:
        """Return all stored traversable arcs in insertion order."""

        return tuple(edge for bucket in self._adjacency.values() for edge in bucket)

    def order(self) -> int:
        """Return the number of vertices."""

        return len(self._adjacency)

    def size(self) -> int:
        """Return the number of stored traversable arcs."""

        return self._edge_count

    def _append_edge(self, source: Vertex, target: Vertex, weight: Any) -> None:
        self._adjacency[source].append(Edge(source, target, weight))
        self._edge_count += 1


def _require_hashable(value: object, name: str) -> None:
    if not isinstance(value, Hashable):
        raise TypeError(f"{name} must be hashable")
