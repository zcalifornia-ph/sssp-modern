from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from sssp.graph import Graph
from sssp.io import read_edge_list


@pytest.fixture
def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


@pytest.fixture
def golden_dir(project_root: Path) -> Path:
    return project_root / "tests" / "golden"


@pytest.fixture
def tiny_directed_graph(golden_dir: Path) -> Graph:
    return read_edge_list(golden_dir / "tiny-directed.edge-list.json")


@pytest.fixture
def tiny_directed_expected_distances(golden_dir: Path) -> dict[str, Any]:
    path = golden_dir / "tiny-directed.distances-s.json"
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise TypeError("golden distance fixture root must be an object")
    return data


@pytest.fixture
def tiny_undirected_graph(golden_dir: Path) -> Graph:
    return read_edge_list(golden_dir / "tiny-undirected.edge-list.json", directed=False)


@pytest.fixture
def tiny_undirected_expected_distances(golden_dir: Path) -> dict[str, Any]:
    path = golden_dir / "tiny-undirected.distances-s.json"
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise TypeError("golden distance fixture root must be an object")
    return data
