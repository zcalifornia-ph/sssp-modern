"""Constant-degree transformation from DMMSY 2025 section 2.

DMMSY assumes a directed graph whose vertices have constant in-degree and
out-degree. Section 2 reduces a general directed graph by replacing each
original vertex with a strongly connected zero-weight cycle of port vertices,
then routing each original arc through one source port and one target port.
Shortest-path distances are preserved after projecting transformed port
distances back to their original vertices.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from sssp.graph import Graph, Vertex


@dataclass(frozen=True, slots=True)
class _PortVertex:
    original: Vertex
    edge_index: int | None
    role: str


@dataclass(frozen=True, slots=True)
class ConstantDegreeTransform:
    """Result of the DMMSY section 2 graph transformation."""

    graph: Graph
    representatives: dict[Vertex, Vertex]
    ports: dict[Vertex, tuple[Vertex, ...]]

    def project_distances(self, distances: Mapping[Vertex, Any]) -> dict[Vertex, Any]:
        """Project transformed port distances back to original vertices."""

        projected: dict[Vertex, Any] = {}
        for original, ports in self.ports.items():
            for port in ports:
                if port not in distances:
                    continue
                distance = distances[port]
                if original not in projected or distance < projected[original]:
                    projected[original] = distance
        return projected


def constant_degree_transform(
    graph: Graph,
    zero_weight: Any = 0.0,
) -> ConstantDegreeTransform:
    """Return the DMMSY section 2 constant-degree transform of `graph`.

    The returned graph is directed and has in-degree and out-degree at most 2
    per transformed vertex: one zero-cycle predecessor/successor and at most
    one original-weight cross arc.
    """

    vertices = graph.vertices()
    edges = graph.edges()
    ports: dict[Vertex, list[Vertex]] = {vertex: [] for vertex in vertices}
    source_ports: dict[int, Vertex] = {}
    target_ports: dict[int, Vertex] = {}

    for index, edge in enumerate(edges):
        source_port = _PortVertex(edge.source, index, "out")
        target_port = _PortVertex(edge.target, index, "in")
        ports[edge.source].append(source_port)
        ports[edge.target].append(target_port)
        source_ports[index] = source_port
        target_ports[index] = target_port

    for vertex, vertex_ports in ports.items():
        if not vertex_ports:
            vertex_ports.append(_PortVertex(vertex, None, "isolated"))

    transformed = Graph(directed=True)
    for vertex_ports in ports.values():
        for port in vertex_ports:
            transformed.add_vertex(port)

    for vertex_ports in ports.values():
        _add_zero_cycle(transformed, tuple(vertex_ports), zero_weight)

    for index, edge in enumerate(edges):
        transformed.add_edge(source_ports[index], target_ports[index], edge.weight)

    frozen_ports = {
        original: tuple(vertex_ports)
        for original, vertex_ports in ports.items()
    }
    representatives = {
        original: vertex_ports[0]
        for original, vertex_ports in frozen_ports.items()
    }
    return ConstantDegreeTransform(transformed, representatives, frozen_ports)


def _add_zero_cycle(graph: Graph, ports: tuple[Vertex, ...], zero_weight: Any) -> None:
    if len(ports) <= 1:
        return
    for index, source in enumerate(ports):
        graph.add_edge(source, ports[(index + 1) % len(ports)], zero_weight)
