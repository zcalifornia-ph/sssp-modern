"""Reusable timing harness for SSSP benchmark runs.

The U7 benchmark protocol excludes graph setup, cached dataset loading, CSV
writing, and plotting from measured algorithm time. This module provides the
small in-process runner used by later U7 Bolts to collect median and IQR timing
summaries from repeat executions.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from statistics import median, quantiles
from typing import Any

from sssp.graph import Graph, Vertex

Clock = Callable[[], float]
GraphBuilder = Callable[[int], Graph]
AlgorithmRunner = Callable[[Graph, Vertex], Any]


@dataclass(frozen=True, slots=True)
class BenchmarkConfig:
    """Timing protocol parameters for one benchmark run."""

    seed: int
    warmups: int = 1
    repeats: int = 5
    clock: Clock = time.perf_counter

    def __post_init__(self) -> None:
        _require_int(self.seed, "seed")
        _require_int(self.warmups, "warmups")
        _require_int(self.repeats, "repeats")
        if self.warmups < 0:
            raise ValueError("warmups must be non-negative")
        if self.repeats < 1:
            raise ValueError("repeats must be at least 1")
        if not callable(self.clock):
            raise TypeError("clock must be callable")


@dataclass(frozen=True, slots=True)
class BenchmarkCase:
    """One seeded graph workload measured by the benchmark runner."""

    name: str
    build_graph: GraphBuilder
    source: Vertex

    def __post_init__(self) -> None:
        _require_name(self.name, "case name")
        if not callable(self.build_graph):
            raise TypeError("build_graph must be callable")


@dataclass(frozen=True, slots=True)
class AlgorithmSpec:
    """One algorithm adapter measured by the benchmark runner."""

    name: str
    run: AlgorithmRunner

    def __post_init__(self) -> None:
        _require_name(self.name, "algorithm name")
        if not callable(self.run):
            raise TypeError("run must be callable")


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    """Timing samples and summary statistics for one case/algorithm pair."""

    case_name: str
    algorithm_name: str
    seed: int
    warmups: int
    repeats: int
    samples: tuple[float, ...]
    median_seconds: float
    iqr_seconds: float


def run_benchmark(
    case: BenchmarkCase,
    algorithms: Sequence[AlgorithmSpec],
    config: BenchmarkConfig,
) -> tuple[BenchmarkResult, ...]:
    """Run `algorithms` against `case` using `config`.

    Warmup executions are performed before recorded executions and are excluded
    from `BenchmarkResult.samples`. `case.build_graph(config.seed)` is invoked
    before the timer starts for every warmup and recorded execution.
    """

    algorithm_specs = tuple(algorithms)
    if not algorithm_specs:
        raise ValueError("at least one algorithm is required")
    _require_unique_algorithm_names(algorithm_specs)

    results: list[BenchmarkResult] = []
    for algorithm in algorithm_specs:
        for _ in range(config.warmups):
            graph = _build_graph(case, config.seed)
            algorithm.run(graph, case.source)

        samples = tuple(
            _measure_once(case, algorithm, config)
            for _ in range(config.repeats)
        )
        results.append(
            BenchmarkResult(
                case_name=case.name,
                algorithm_name=algorithm.name,
                seed=config.seed,
                warmups=config.warmups,
                repeats=config.repeats,
                samples=samples,
                median_seconds=float(median(samples)),
                iqr_seconds=_iqr(samples),
            )
        )

    return tuple(results)


def _measure_once(
    case: BenchmarkCase,
    algorithm: AlgorithmSpec,
    config: BenchmarkConfig,
) -> float:
    graph = _build_graph(case, config.seed)
    start = config.clock()
    algorithm.run(graph, case.source)
    elapsed = float(config.clock() - start)
    if elapsed < 0.0:
        raise ValueError("clock must be monotonic")
    return elapsed


def _build_graph(case: BenchmarkCase, seed: int) -> Graph:
    graph = case.build_graph(seed)
    if not isinstance(graph, Graph):
        raise TypeError("build_graph must return a Graph")
    if case.source not in set(graph.vertices()):
        raise ValueError("case source must be a vertex in the generated graph")
    return graph


def _iqr(samples: Sequence[float]) -> float:
    if len(samples) == 1:
        return 0.0
    q1, _, q3 = quantiles(samples, n=4, method="inclusive")
    return float(q3 - q1)


def _require_unique_algorithm_names(algorithms: Sequence[AlgorithmSpec]) -> None:
    names: set[str] = set()
    for algorithm in algorithms:
        if algorithm.name in names:
            raise ValueError("algorithm names must be unique")
        names.add(algorithm.name)


def _require_int(value: object, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")


def _require_name(value: object, name: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value.strip():
        raise ValueError(f"{name} must be non-empty")
