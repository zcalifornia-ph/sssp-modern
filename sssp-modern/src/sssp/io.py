"""JSON graph IO helpers for reproducible SSSP fixtures."""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from sssp.graph import Edge, Graph
from sssp.weights import Weight

EDGE_LIST_FORMAT = "sssp.edge-list.v1"
ADJACENCY_LIST_FORMAT = "sssp.adjacency-list.v1"


def read_edge_list(path: str | Path) -> Graph:
    """Read an `sssp.edge-list.v1` JSON fixture into a Graph."""

    return graph_from_edge_list_data(_read_json_object(path))


def write_edge_list(graph: Graph, path: str | Path) -> None:
    """Write a Graph as an `sssp.edge-list.v1` JSON fixture."""

    _write_json_object(path, graph_to_edge_list_data(graph))


def read_adjacency_list(path: str | Path) -> Graph:
    """Read an `sssp.adjacency-list.v1` JSON fixture into a Graph."""

    return graph_from_adjacency_list_data(_read_json_object(path))


def write_adjacency_list(graph: Graph, path: str | Path) -> None:
    """Write a Graph as an `sssp.adjacency-list.v1` JSON fixture."""

    _write_json_object(path, graph_to_adjacency_list_data(graph))


def graph_to_edge_list_data(graph: Graph) -> dict[str, object]:
    """Convert a Graph to the serializable edge-list fixture mapping."""

    vertices = _serializable_vertices(graph)
    return {
        "format": EDGE_LIST_FORMAT,
        "directed": graph.is_directed,
        "vertices": vertices,
        "edges": [_edge_to_data(edge) for edge in _logical_edges(graph)],
    }


def graph_from_edge_list_data(data: Mapping[str, object]) -> Graph:
    """Build a Graph from an `sssp.edge-list.v1` mapping."""

    _require_format(data, EDGE_LIST_FORMAT)
    directed = _require_bool(data.get("directed"), "directed")
    vertices = _require_string_sequence(data.get("vertices"), "vertices")
    _require_unique(vertices, "vertices")
    vertex_set = set(vertices)
    graph = Graph(directed=directed)

    for vertex in vertices:
        graph.add_vertex(vertex)

    edges = _require_sequence(data.get("edges"), "edges")
    for index, item in enumerate(edges):
        if not isinstance(item, Mapping):
            raise TypeError(f"edges[{index}] must be an object")
        source = _require_string(item.get("source"), f"edges[{index}].source")
        target = _require_string(item.get("target"), f"edges[{index}].target")
        weight = _require_weight(item.get("weight"), f"edges[{index}].weight")
        _require_known_vertex(source, vertex_set, f"edges[{index}].source")
        _require_known_vertex(target, vertex_set, f"edges[{index}].target")
        graph.add_edge(source, target, weight)

    return graph


def graph_to_adjacency_list_data(graph: Graph) -> dict[str, object]:
    """Convert a Graph to the serializable adjacency-list fixture mapping."""

    adjacency: dict[str, list[dict[str, object]]] = {
        vertex: [] for vertex in _serializable_vertices(graph)
    }
    for edge in _logical_edges(graph):
        adjacency[edge.source].append(
            {"target": edge.target, "weight": _serializable_weight(edge.weight)}
        )

    return {
        "format": ADJACENCY_LIST_FORMAT,
        "directed": graph.is_directed,
        "adjacency": adjacency,
    }


def graph_from_adjacency_list_data(data: Mapping[str, object]) -> Graph:
    """Build a Graph from an `sssp.adjacency-list.v1` mapping."""

    _require_format(data, ADJACENCY_LIST_FORMAT)
    directed = _require_bool(data.get("directed"), "directed")
    adjacency = data.get("adjacency")
    if not isinstance(adjacency, Mapping):
        raise TypeError("adjacency must be an object")

    vertices = tuple(_require_string(vertex, "adjacency vertex") for vertex in adjacency)
    _require_unique(vertices, "adjacency vertices")
    vertex_set = set(vertices)
    graph = Graph(directed=directed)

    for vertex in vertices:
        graph.add_vertex(vertex)

    for source, neighbors in adjacency.items():
        source = _require_string(source, "adjacency vertex")
        neighbor_items = _require_sequence(neighbors, f"adjacency[{source!r}]")
        for index, item in enumerate(neighbor_items):
            if not isinstance(item, Mapping):
                raise TypeError(f"adjacency[{source!r}][{index}] must be an object")
            target = _require_string(item.get("target"), f"adjacency[{source!r}][{index}].target")
            weight = _require_weight(item.get("weight"), f"adjacency[{source!r}][{index}].weight")
            _require_known_vertex(target, vertex_set, f"adjacency[{source!r}][{index}].target")
            graph.add_edge(source, target, weight)

    return graph


def _read_json_object(path: str | Path) -> Mapping[str, object]:
    with Path(path).open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, Mapping):
        raise TypeError("graph fixture root must be an object")
    return data


def _write_json_object(path: str | Path, data: Mapping[str, object]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="\n") as file:
        json.dump(data, file, indent=2)
        file.write("\n")


def _logical_edges(graph: Graph) -> tuple[Edge, ...]:
    if graph.is_directed:
        return graph.edges()

    pending = Counter(
        (edge.source, edge.target, _weight_key(edge.weight)) for edge in graph.edges()
    )
    logical: list[Edge] = []

    for edge in graph.edges():
        key = (edge.source, edge.target, _weight_key(edge.weight))
        reverse_key = (edge.target, edge.source, _weight_key(edge.weight))
        if pending[key] <= 0:
            continue

        pending[key] -= 1
        if pending[reverse_key] > 0:
            pending[reverse_key] -= 1
        logical.append(edge)

    return tuple(logical)


def _edge_to_data(edge: Edge) -> dict[str, object]:
    source = _require_string(edge.source, "edge.source")
    target = _require_string(edge.target, "edge.target")
    return {
        "source": source,
        "target": target,
        "weight": _serializable_weight(edge.weight),
    }


def _serializable_vertices(graph: Graph) -> list[str]:
    return [_require_string(vertex, "vertex") for vertex in graph.vertices()]


def _serializable_weight(weight: object) -> int | float:
    if isinstance(weight, Weight):
        return weight.value
    return _require_weight(weight, "weight")


def _weight_key(weight: object) -> tuple[type[object], object]:
    if isinstance(weight, Weight):
        return (Weight, weight.value)
    return (type(weight), weight)


def _require_format(data: Mapping[str, object], expected: str) -> None:
    actual = data.get("format")
    if actual != expected:
        raise ValueError(f"format must be {expected!r}")


def _require_bool(value: object, name: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a boolean")
    return value


def _require_string(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    return value


def _require_sequence(value: object, name: str) -> Sequence[object]:
    if isinstance(value, str) or not isinstance(value, Sequence):
        raise TypeError(f"{name} must be an array")
    return value


def _require_string_sequence(value: object, name: str) -> tuple[str, ...]:
    return tuple(
        _require_string(item, f"{name}[{index}]")
        for index, item in enumerate(_require_sequence(value, name))
    )


def _require_weight(value: object, name: str) -> int | float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise TypeError(f"{name} must be a JSON number")
    return value


def _require_unique(values: Sequence[str], name: str) -> None:
    if len(set(values)) != len(values):
        raise ValueError(f"{name} must not contain duplicates")


def _require_known_vertex(vertex: str, vertices: set[str], name: str) -> None:
    if vertex not in vertices:
        raise ValueError(f"{name} references an unknown vertex")
