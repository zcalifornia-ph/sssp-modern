from __future__ import annotations

import pytest

from bench.runner import (
    AlgorithmSpec,
    BenchmarkCase,
    BenchmarkConfig,
    run_benchmark,
)
from sssp.dijkstra import dijkstra
from sssp.graph import Graph


def test_run_benchmark_replays_same_seed_with_deterministic_clock() -> None:
    first = run_benchmark(
        _case(),
        [AlgorithmSpec("dijkstra", dijkstra)],
        BenchmarkConfig(seed=2026, warmups=1, repeats=3, clock=_clock([1.0, 2.0, 3.0])),
    )
    second = run_benchmark(
        _case(),
        [AlgorithmSpec("dijkstra", dijkstra)],
        BenchmarkConfig(seed=2026, warmups=1, repeats=3, clock=_clock([1.0, 2.0, 3.0])),
    )

    assert first == second
    assert first[0].samples == (1.0, 2.0, 3.0)
    assert first[0].median_seconds == 2.0


def test_run_benchmark_excludes_warmups_from_samples() -> None:
    calls = {"algorithm": 0}

    def run(graph: Graph, source: object) -> dict[object, float]:
        calls["algorithm"] += 1
        return dijkstra(graph, source)

    result = run_benchmark(
        _case(),
        [AlgorithmSpec("dijkstra", run)],
        BenchmarkConfig(seed=7, warmups=2, repeats=3, clock=_clock([3.0, 4.0, 5.0])),
    )[0]

    assert calls["algorithm"] == 5
    assert result.samples == (3.0, 4.0, 5.0)
    assert result.warmups == 2
    assert result.repeats == 3


def test_run_benchmark_builds_graph_outside_timing_window() -> None:
    events: list[str] = []

    def build_graph(seed: int) -> Graph:
        events.append(f"build:{seed}")
        return _graph()

    def run(graph: Graph, source: object) -> dict[object, float]:
        events.append("run")
        return dijkstra(graph, source)

    def clock() -> float:
        events.append("clock")
        return float(len([event for event in events if event == "clock"]))

    run_benchmark(
        BenchmarkCase("ordered", build_graph, "s"),
        [AlgorithmSpec("dijkstra", run)],
        BenchmarkConfig(seed=42, warmups=1, repeats=1, clock=clock),
    )

    assert events == ["build:42", "run", "build:42", "clock", "run", "clock"]


def test_run_benchmark_reports_median_and_iqr() -> None:
    result = run_benchmark(
        _case(),
        [AlgorithmSpec("dijkstra", dijkstra)],
        BenchmarkConfig(
            seed=2026,
            warmups=0,
            repeats=5,
            clock=_clock([1.0, 2.0, 3.0, 4.0, 5.0]),
        ),
    )[0]

    assert result.samples == (1.0, 2.0, 3.0, 4.0, 5.0)
    assert result.median_seconds == 3.0
    assert result.iqr_seconds == 2.0


def test_run_benchmark_validates_protocol_inputs() -> None:
    with pytest.raises(ValueError, match="warmups must be non-negative"):
        BenchmarkConfig(seed=1, warmups=-1)
    with pytest.raises(ValueError, match="repeats must be at least 1"):
        BenchmarkConfig(seed=1, repeats=0)
    with pytest.raises(ValueError, match="case name must be non-empty"):
        BenchmarkCase("", _build_graph, "s")
    with pytest.raises(ValueError, match="algorithm name must be non-empty"):
        AlgorithmSpec("", dijkstra)
    with pytest.raises(ValueError, match="at least one algorithm is required"):
        run_benchmark(_case(), [], BenchmarkConfig(seed=1))
    with pytest.raises(ValueError, match="algorithm names must be unique"):
        run_benchmark(
            _case(),
            [AlgorithmSpec("dijkstra", dijkstra), AlgorithmSpec("dijkstra", dijkstra)],
            BenchmarkConfig(seed=1),
        )


def test_run_benchmark_rejects_invalid_generated_graphs() -> None:
    with pytest.raises(TypeError, match="build_graph must return a Graph"):
        run_benchmark(
            BenchmarkCase("bad-type", lambda seed: object(), "s"),
            [AlgorithmSpec("noop", lambda graph, source: None)],
            BenchmarkConfig(seed=1, warmups=0, repeats=1),
        )

    with pytest.raises(ValueError, match="case source must be a vertex"):
        run_benchmark(
            BenchmarkCase("bad-source", _build_graph, "missing"),
            [AlgorithmSpec("noop", lambda graph, source: None)],
            BenchmarkConfig(seed=1, warmups=0, repeats=1),
        )


def _case() -> BenchmarkCase:
    return BenchmarkCase("tiny-path", _build_graph, "s")


def _build_graph(seed: int) -> Graph:
    graph = _graph()
    graph.add_edge("a", f"seed-{seed}", 2.0)
    return graph


def _graph() -> Graph:
    return Graph.from_edges([("s", "a", 1.0), ("s", "b", 3.0), ("a", "b", 1.0)])


def _clock(durations: list[float]):
    times: list[float] = []
    current = 0.0
    for duration in durations:
        start = current + 10.0
        end = start + duration
        times.extend([start, end])
        current = end

    def clock() -> float:
        return times.pop(0)

    return clock
