"""Deterministic benchmark dataset catalog for SSSP experiments."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sssp.generators import (
    barabasi_albert_graph,
    dag_graph,
    erdos_renyi_graph,
    random_geometric_graph,
    signed_edge_graph,
)
from sssp.graph import Graph, Vertex
from sssp.io import graph_to_edge_list_data, read_edge_list, write_edge_list

DEFAULT_DATASET_ROOT = Path("bench/datasets")
DEFAULT_DATASET_SEED = 2026

_ALL_ALGORITHMS = ("dijkstra", "bellman-ford", "astar", "thorup99", "dmmsy")
_BELLMAN_FORD_ONLY = ("bellman-ford",)
_SIZES = (("small", 64), ("medium", 256), ("large", 1024))
_DENSITIES: dict[str, dict[str, int | float]] = {
    "sparse": {
        "edge_probability": 0.01,
        "radius": 0.08,
        "attachments": 2,
        "signed_edge_probability": 0.01,
    },
    "dense": {
        "edge_probability": 0.03,
        "radius": 0.16,
        "attachments": 4,
        "signed_edge_probability": 0.03,
    },
}
_GENERATORS = (
    "erdos-renyi",
    "geometric",
    "dag",
    "barabasi-albert",
    "signed-dag",
)


@dataclass(frozen=True, slots=True)
class DatasetProfile:
    """One deterministic benchmark dataset profile."""

    name: str
    generator: str
    size_label: str
    density_label: str
    order: int
    parameters: tuple[tuple[str, int | float], ...]
    source: Vertex = "v0"
    compatible_algorithms: tuple[str, ...] = _ALL_ALGORITHMS
    allows_negative_weights: bool = False

    def __post_init__(self) -> None:
        _require_name(self.name, "profile name")
        _require_name(self.generator, "generator")
        _require_name(self.size_label, "size_label")
        _require_name(self.density_label, "density_label")
        _require_int(self.order, "order")
        if self.order < 1:
            raise ValueError("order must be at least 1")
        if not isinstance(self.parameters, tuple):
            raise TypeError("parameters must be a tuple")
        if not isinstance(self.compatible_algorithms, tuple):
            raise TypeError("compatible_algorithms must be a tuple")


@dataclass(frozen=True, slots=True)
class DatasetRecord:
    """Cached dataset metadata used by later benchmark runs."""

    profile: DatasetProfile
    seed: int
    path: Path
    fingerprint: str
    order: int
    edge_count: int


def dataset_profiles() -> tuple[DatasetProfile, ...]:
    """Return the default deterministic benchmark dataset matrix."""

    profiles: list[DatasetProfile] = []
    for generator in _GENERATORS:
        for size_label, order in _SIZES:
            for density_label, density in _DENSITIES.items():
                profiles.append(
                    _profile(
                        generator=generator,
                        size_label=size_label,
                        density_label=density_label,
                        order=order,
                        density=density,
                    )
                )
    return tuple(profiles)


def build_dataset_graph(profile: DatasetProfile, seed: int) -> Graph:
    """Build a graph for `profile` from the configured deterministic generator."""

    if not isinstance(profile, DatasetProfile):
        raise TypeError("profile must be a DatasetProfile")
    _require_int(seed, "seed")

    params = dict(profile.parameters)
    if profile.generator == "erdos-renyi":
        return erdos_renyi_graph(
            profile.order,
            _number(params, "edge_probability"),
            seed=seed,
            directed=True,
        )
    if profile.generator == "geometric":
        return random_geometric_graph(
            profile.order,
            _number(params, "radius"),
            seed=seed,
            directed=False,
        )
    if profile.generator == "dag":
        return dag_graph(
            profile.order,
            _number(params, "edge_probability"),
            seed=seed,
        )
    if profile.generator == "barabasi-albert":
        return barabasi_albert_graph(
            profile.order,
            _integer(params, "attachments"),
            seed=seed,
        )
    if profile.generator == "signed-dag":
        return signed_edge_graph(
            profile.order,
            _number(params, "edge_probability"),
            seed=seed,
            negative_fraction=_number(params, "negative_fraction"),
            acyclic=True,
        )

    raise ValueError(f"unknown generator {profile.generator!r}")


def dataset_fingerprint(graph: Graph) -> str:
    """Return a stable SHA-256 fingerprint for `graph`."""

    if not isinstance(graph, Graph):
        raise TypeError("graph must be a Graph")

    payload = json.dumps(
        graph_to_edge_list_data(graph),
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def dataset_cache_path(
    profile: DatasetProfile,
    seed: int,
    root: str | Path = DEFAULT_DATASET_ROOT,
) -> Path:
    """Return the deterministic cache path for `profile` and `seed`."""

    if not isinstance(profile, DatasetProfile):
        raise TypeError("profile must be a DatasetProfile")
    _require_int(seed, "seed")
    return Path(root) / f"{profile.name}-seed-{seed}.edge-list.json"


def ensure_dataset(
    profile: DatasetProfile,
    seed: int,
    root: str | Path = DEFAULT_DATASET_ROOT,
    refresh: bool = False,
) -> DatasetRecord:
    """Create or load one cached dataset and return its metadata."""

    path = dataset_cache_path(profile, seed, root)
    if path.exists() and not refresh:
        graph = read_edge_list(path)
    else:
        graph = build_dataset_graph(profile, seed)
        write_edge_list(graph, path)

    return DatasetRecord(
        profile=profile,
        seed=seed,
        path=path,
        fingerprint=dataset_fingerprint(graph),
        order=graph.order(),
        edge_count=graph.size(),
    )


def ensure_default_datasets(
    seed: int = DEFAULT_DATASET_SEED,
    root: str | Path = DEFAULT_DATASET_ROOT,
    refresh: bool = False,
) -> tuple[DatasetRecord, ...]:
    """Create or load every default dataset profile."""

    return tuple(
        ensure_dataset(profile, seed=seed, root=root, refresh=refresh)
        for profile in dataset_profiles()
    )


def _profile(
    *,
    generator: str,
    size_label: str,
    density_label: str,
    order: int,
    density: dict[str, int | float],
) -> DatasetProfile:
    params: tuple[tuple[str, int | float], ...]
    compatible_algorithms = _ALL_ALGORITHMS
    allows_negative_weights = False

    if generator in {"erdos-renyi", "dag"}:
        params = (("edge_probability", density["edge_probability"]),)
    elif generator == "geometric":
        params = (("radius", density["radius"]),)
    elif generator == "barabasi-albert":
        params = (("attachments", density["attachments"]),)
    elif generator == "signed-dag":
        params = (
            ("edge_probability", density["signed_edge_probability"]),
            ("negative_fraction", 0.25),
        )
        compatible_algorithms = _BELLMAN_FORD_ONLY
        allows_negative_weights = True
    else:
        raise ValueError(f"unknown generator {generator!r}")

    name = f"{generator}-{size_label}-{density_label}"
    return DatasetProfile(
        name=name,
        generator=generator,
        size_label=size_label,
        density_label=density_label,
        order=order,
        parameters=params,
        compatible_algorithms=compatible_algorithms,
        allows_negative_weights=allows_negative_weights,
    )


def _number(params: dict[str, Any], name: str) -> float:
    value = params[name]
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise TypeError(f"{name} must be numeric")
    return float(value)


def _integer(params: dict[str, Any], name: str) -> int:
    value = params[name]
    _require_int(value, name)
    return value


def _require_int(value: object, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")


def _require_name(value: object, name: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value.strip():
        raise ValueError(f"{name} must be non-empty")
