from __future__ import annotations

from dataclasses import replace

from bench.datasets import DatasetProfile, DatasetRecord, dataset_fingerprint
from bench.plots import (
    BenchmarkCSVRow,
    check_dmmsy_within_dijkstra,
    collect_benchmark_rows,
    read_results_csv,
    regression_issues,
    render_runtime_chart,
    write_results_csv,
)
from bench.runner import BenchmarkConfig
from sssp.graph import Graph
from sssp.io import write_edge_list


def test_collect_benchmark_rows_adds_dijkstra_ratios_for_all_five_algorithms(tmp_path) -> None:
    record = _record(
        tmp_path,
        _undirected_integer_graph(),
        generator="barabasi-albert",
    )

    rows = collect_benchmark_rows(
        [record],
        BenchmarkConfig(
            seed=7,
            warmups=0,
            repeats=1,
            clock=_clock([1.0, 2.0, 3.0, 4.0, 5.0]),
        ),
    )

    assert [row.algorithm_name for row in rows] == [
        "dijkstra",
        "bellman-ford",
        "astar",
        "thorup99",
        "dmmsy",
    ]
    assert rows[0].graph_view == "integer-undirected"
    assert [row.ratio_vs_dijkstra for row in rows] == [1.0, 2.0, 3.0, 4.0, 5.0]


def test_negative_profile_runs_bellman_ford_context_only(tmp_path) -> None:
    record = _record(
        tmp_path,
        Graph.from_edges([("v0", "v1", -1.0), ("v1", "v2", 2.0)]),
        generator="signed-dag",
        allows_negative_weights=True,
    )

    rows = collect_benchmark_rows(
        [record],
        BenchmarkConfig(seed=7, warmups=0, repeats=1, clock=_clock([1.5])),
    )

    assert [row.algorithm_name for row in rows] == ["bellman-ford"]
    assert rows[0].graph_view == "raw"
    assert rows[0].ratio_vs_dijkstra is None


def test_results_csv_round_trips_and_regression_check_detects_slowdown(tmp_path) -> None:
    current = _row("dijkstra", median_seconds=3.0)
    prior = replace(current, median_seconds=1.0)
    path = tmp_path / "results.csv"

    write_results_csv([current], path)
    loaded = read_results_csv(path)

    assert loaded == (current,)
    assert regression_issues(loaded, [prior], max_slowdown=2.0) == (
        "('case-large', 'raw', 'dijkstra') slowed from 1s to 3s",
    )


def test_render_runtime_chart_writes_png_and_pdf(tmp_path) -> None:
    rows = [
        _row("dijkstra", median_seconds=1.0),
        _row("bellman-ford", median_seconds=2.0),
        _row("dmmsy", median_seconds=3.0),
    ]
    png, pdf = render_runtime_chart(
        rows,
        tmp_path / "runtime.png",
        tmp_path / "runtime.pdf",
    )

    assert png.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    assert pdf.read_bytes().startswith(b"%PDF-1.4")
    assert png.stat().st_size > 100
    assert pdf.stat().st_size > 100


def test_t17_check_reports_pass_and_fail_cases() -> None:
    passing = [
        _row("dijkstra", median_seconds=1.0),
        _row("dmmsy", median_seconds=1.5),
    ]
    failing = [
        _row("dijkstra", median_seconds=1.0),
        _row("dmmsy", median_seconds=2.5),
    ]

    pass_check = check_dmmsy_within_dijkstra(passing)
    fail_check = check_dmmsy_within_dijkstra(failing)

    assert pass_check.passed
    assert pass_check.max_ratio == 1.5
    assert not fail_check.passed
    assert fail_check.max_ratio == 2.5
    assert fail_check.failing_cases == ("case-large [raw]: 2.500x",)


def _record(
    tmp_path,
    graph: Graph,
    *,
    generator: str,
    allows_negative_weights: bool = False,
) -> DatasetRecord:
    profile = DatasetProfile(
        name=f"{generator}-small-sparse",
        generator=generator,
        size_label="small",
        density_label="sparse",
        order=graph.order(),
        parameters=(("edge_probability", 0.1),),
        allows_negative_weights=allows_negative_weights,
    )
    path = tmp_path / f"{profile.name}.edge-list.json"
    write_edge_list(graph, path)
    return DatasetRecord(
        profile=profile,
        seed=7,
        path=path,
        fingerprint=dataset_fingerprint(graph),
        order=graph.order(),
        edge_count=graph.size(),
    )


def _undirected_integer_graph() -> Graph:
    return Graph.from_edges(
        [
            ("v0", "v1", 1),
            ("v1", "v2", 2),
            ("v2", "v3", 3),
            ("v0", "v3", 8),
        ],
        directed=False,
    )


def _row(algorithm: str, *, median_seconds: float) -> BenchmarkCSVRow:
    ratio = None if algorithm == "dijkstra" else median_seconds
    return BenchmarkCSVRow(
        case_name="case-large",
        graph_view="raw",
        profile_name="case-large",
        generator="erdos-renyi",
        size_label="large",
        density_label="sparse",
        seed=2026,
        order=1000,
        edge_count=10,
        fingerprint="abc",
        algorithm_name=algorithm,
        warmups=0,
        repeats=1,
        samples_seconds=(median_seconds,),
        median_seconds=median_seconds,
        iqr_seconds=0.0,
        ratio_vs_dijkstra=ratio,
    )


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
