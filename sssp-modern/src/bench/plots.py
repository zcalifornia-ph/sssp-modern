"""Benchmark result materialization and chart output for U7.

This module consumes the B7.1 timing runner and B7.2 dataset catalog. It keeps
CSV rows as the detailed evidence source and renders lightweight PNG/PDF charts
with only the Python standard library.
"""

from __future__ import annotations

import argparse
import csv
import math
import statistics
import struct
import zlib
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from bench.datasets import (
    DEFAULT_DATASET_ROOT,
    DEFAULT_DATASET_SEED,
    DatasetRecord,
    dataset_profiles,
    ensure_dataset,
)
from bench.runner import AlgorithmSpec, BenchmarkCase, BenchmarkConfig, run_benchmark
from sssp.astar import astar
from sssp.bellman_ford import bellman_ford
from sssp.dijkstra import dijkstra
from sssp.dmmsy import dmmsy_sssp
from sssp.graph import Edge, Graph, Vertex
from sssp.heuristics import zero
from sssp.io import read_edge_list
from sssp.thorup99 import thorup_sssp

DEFAULT_RESULTS_PATH = Path("bench/results/sssp-benchmark-seed-2026.csv")
DEFAULT_FIGURE_STEM = Path("bench/figures/runtime-by-algorithm")
DEFAULT_REPORT_GENERATORS = ("geometric", "barabasi-albert")
ALGORITHM_ORDER = ("dijkstra", "bellman-ford", "astar", "thorup99", "dmmsy")
CSV_FIELDS = (
    "case_name",
    "graph_view",
    "profile_name",
    "generator",
    "size_label",
    "density_label",
    "seed",
    "order",
    "edge_count",
    "fingerprint",
    "algorithm_name",
    "warmups",
    "repeats",
    "samples_seconds",
    "median_seconds",
    "iqr_seconds",
    "ratio_vs_dijkstra",
)


@dataclass(frozen=True, slots=True)
class BenchmarkCSVRow:
    """Serializable benchmark result row."""

    case_name: str
    graph_view: str
    profile_name: str
    generator: str
    size_label: str
    density_label: str
    seed: int
    order: int
    edge_count: int
    fingerprint: str
    algorithm_name: str
    warmups: int
    repeats: int
    samples_seconds: tuple[float, ...]
    median_seconds: float
    iqr_seconds: float
    ratio_vs_dijkstra: float | None = None

    def key(self) -> tuple[str, str, str]:
        """Return the stable case/view/algorithm identity."""

        return (self.case_name, self.graph_view, self.algorithm_name)

    def baseline_key(self) -> tuple[str, str]:
        """Return the stable case/view identity used for Dijkstra ratios."""

        return (self.case_name, self.graph_view)

    def to_csv_dict(self) -> dict[str, str]:
        """Return a stable CSV representation."""

        return {
            "case_name": self.case_name,
            "graph_view": self.graph_view,
            "profile_name": self.profile_name,
            "generator": self.generator,
            "size_label": self.size_label,
            "density_label": self.density_label,
            "seed": str(self.seed),
            "order": str(self.order),
            "edge_count": str(self.edge_count),
            "fingerprint": self.fingerprint,
            "algorithm_name": self.algorithm_name,
            "warmups": str(self.warmups),
            "repeats": str(self.repeats),
            "samples_seconds": ";".join(_format_float(value) for value in self.samples_seconds),
            "median_seconds": _format_float(self.median_seconds),
            "iqr_seconds": _format_float(self.iqr_seconds),
            "ratio_vs_dijkstra": (
                "" if self.ratio_vs_dijkstra is None else _format_float(self.ratio_vs_dijkstra)
            ),
        }

    @classmethod
    def from_csv_dict(cls, row: dict[str, str]) -> BenchmarkCSVRow:
        """Parse one CSV dictionary produced by `to_csv_dict`."""

        samples = tuple(
            float(value)
            for value in row["samples_seconds"].split(";")
            if value
        )
        ratio_text = row.get("ratio_vs_dijkstra", "")
        return cls(
            case_name=row["case_name"],
            graph_view=row["graph_view"],
            profile_name=row["profile_name"],
            generator=row["generator"],
            size_label=row["size_label"],
            density_label=row["density_label"],
            seed=int(row["seed"]),
            order=int(row["order"]),
            edge_count=int(row["edge_count"]),
            fingerprint=row["fingerprint"],
            algorithm_name=row["algorithm_name"],
            warmups=int(row["warmups"]),
            repeats=int(row["repeats"]),
            samples_seconds=samples,
            median_seconds=float(row["median_seconds"]),
            iqr_seconds=float(row["iqr_seconds"]),
            ratio_vs_dijkstra=None if not ratio_text else float(ratio_text),
        )


@dataclass(frozen=True, slots=True)
class PerformanceCheck:
    """T-17 decision for DMMSY against Dijkstra."""

    passed: bool
    max_ratio: float | None
    checked_cases: tuple[str, ...]
    failing_cases: tuple[str, ...]


def records_for_generators(
    generators: Iterable[str] = DEFAULT_REPORT_GENERATORS,
    *,
    seed: int = DEFAULT_DATASET_SEED,
    root: str | Path = DEFAULT_DATASET_ROOT,
    refresh: bool = False,
) -> tuple[DatasetRecord, ...]:
    """Create/load dataset records for the selected generator families."""

    selected = set(generators)
    return tuple(
        ensure_dataset(profile, seed=seed, root=root, refresh=refresh)
        for profile in dataset_profiles()
        if profile.generator in selected
    )


def collect_benchmark_rows(
    records: Sequence[DatasetRecord],
    config: BenchmarkConfig,
) -> tuple[BenchmarkCSVRow, ...]:
    """Run benchmarks for `records` and return CSV-ready rows."""

    rows: list[BenchmarkCSVRow] = []
    for record in records:
        graph, graph_view = benchmark_graph_view(record)
        algorithms = benchmark_algorithm_specs(graph, record.profile.source)
        if not algorithms:
            continue

        case = BenchmarkCase(
            name=record.profile.name,
            build_graph=lambda seed, graph=graph: graph,
            source=record.profile.source,
        )
        results = run_benchmark(case, algorithms, config)
        dijkstra_median = next(
            (
                result.median_seconds
                for result in results
                if result.algorithm_name == "dijkstra"
            ),
            None,
        )

        for result in results:
            ratio = (
                None
                if dijkstra_median is None or dijkstra_median == 0.0
                else result.median_seconds / dijkstra_median
            )
            rows.append(
                BenchmarkCSVRow(
                    case_name=result.case_name,
                    graph_view=graph_view,
                    profile_name=record.profile.name,
                    generator=record.profile.generator,
                    size_label=record.profile.size_label,
                    density_label=record.profile.density_label,
                    seed=result.seed,
                    order=graph.order(),
                    edge_count=graph.size(),
                    fingerprint=record.fingerprint,
                    algorithm_name=result.algorithm_name,
                    warmups=result.warmups,
                    repeats=result.repeats,
                    samples_seconds=result.samples,
                    median_seconds=result.median_seconds,
                    iqr_seconds=result.iqr_seconds,
                    ratio_vs_dijkstra=ratio,
                )
            )

    return tuple(rows)


def benchmark_graph_view(record: DatasetRecord) -> tuple[Graph, str]:
    """Return the graph view used for benchmarking one dataset record."""

    graph = read_edge_list(record.path)
    if not graph.is_directed and _has_no_negative_edges(graph):
        return _integer_undirected_graph(graph), "integer-undirected"
    return graph, "raw"


def benchmark_algorithm_specs(
    graph: Graph,
    source: Vertex,
) -> tuple[AlgorithmSpec, ...]:
    """Return algorithm adapters compatible with `graph`."""

    specs: list[AlgorithmSpec] = []
    non_negative = _has_no_negative_edges(graph)

    if non_negative:
        specs.append(AlgorithmSpec("dijkstra", dijkstra))

    specs.append(AlgorithmSpec("bellman-ford", _bellman_ford_distances))

    if non_negative:
        goal = _goal_vertex(graph, source)
        specs.append(
            AlgorithmSpec(
                "astar",
                lambda graph, source, goal=goal: astar(graph, source, goal, zero),
            )
        )
        if _thorup_compatible(graph):
            specs.append(AlgorithmSpec("thorup99", thorup_sssp))
        specs.append(AlgorithmSpec("dmmsy", dmmsy_sssp))

    order = {name: index for index, name in enumerate(ALGORITHM_ORDER)}
    return tuple(sorted(specs, key=lambda spec: order[spec.name]))


def write_results_csv(
    rows: Sequence[BenchmarkCSVRow],
    path: str | Path = DEFAULT_RESULTS_PATH,
) -> Path:
    """Write benchmark rows to CSV and return the path."""

    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row.to_csv_dict())
    return output


def read_results_csv(path: str | Path) -> tuple[BenchmarkCSVRow, ...]:
    """Read benchmark rows previously written by `write_results_csv`."""

    with Path(path).open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return tuple(BenchmarkCSVRow.from_csv_dict(row) for row in reader)


def regression_issues(
    current_rows: Sequence[BenchmarkCSVRow],
    prior_rows: Sequence[BenchmarkCSVRow] = (),
    *,
    max_slowdown: float = 2.0,
) -> tuple[str, ...]:
    """Return duplicate-row or slowdown issues against prior rows."""

    if max_slowdown < 1.0:
        raise ValueError("max_slowdown must be at least 1.0")

    issues: list[str] = []
    seen: set[tuple[str, str, str]] = set()
    for row in current_rows:
        if row.key() in seen:
            issues.append(f"duplicate benchmark row: {row.key()}")
        seen.add(row.key())

    prior_by_key = {row.key(): row for row in prior_rows}
    for row in current_rows:
        prior = prior_by_key.get(row.key())
        if prior is None or prior.median_seconds <= 0.0:
            continue
        if row.median_seconds > prior.median_seconds * max_slowdown:
            issues.append(
                f"{row.key()} slowed from "
                f"{prior.median_seconds:.6g}s to {row.median_seconds:.6g}s"
            )

    return tuple(issues)


def check_dmmsy_within_dijkstra(
    rows: Sequence[BenchmarkCSVRow],
    *,
    max_ratio: float = 2.0,
    minimum_order: int = 1000,
) -> PerformanceCheck:
    """Return the T-17 DMMSY-vs-Dijkstra pass/fail decision."""

    if max_ratio <= 0.0:
        raise ValueError("max_ratio must be positive")

    baselines = {
        row.baseline_key(): row
        for row in rows
        if row.algorithm_name == "dijkstra" and row.order >= minimum_order
    }
    checked: list[str] = []
    failing: list[str] = []
    observed: list[float] = []

    for row in rows:
        if row.algorithm_name != "dmmsy" or row.order < minimum_order:
            continue
        baseline = baselines.get(row.baseline_key())
        if baseline is None or baseline.median_seconds <= 0.0:
            continue
        ratio = row.median_seconds / baseline.median_seconds
        observed.append(ratio)
        label = f"{row.case_name} [{row.graph_view}]"
        checked.append(label)
        if ratio > max_ratio:
            failing.append(f"{label}: {ratio:.3f}x")

    return PerformanceCheck(
        passed=bool(checked) and not failing,
        max_ratio=max(observed) if observed else None,
        checked_cases=tuple(checked),
        failing_cases=tuple(failing),
    )


def render_runtime_chart(
    rows: Sequence[BenchmarkCSVRow],
    png_path: str | Path = DEFAULT_FIGURE_STEM.with_suffix(".png"),
    pdf_path: str | Path = DEFAULT_FIGURE_STEM.with_suffix(".pdf"),
) -> tuple[Path, Path]:
    """Render runtime chart artifacts and return `(png_path, pdf_path)`."""

    png = Path(png_path)
    pdf = Path(pdf_path)
    png.parent.mkdir(parents=True, exist_ok=True)
    pdf.parent.mkdir(parents=True, exist_ok=True)
    series = _chart_series(rows)
    _write_png_chart(series, png)
    _write_pdf_chart(series, pdf)
    return png, pdf


def materialize_benchmark_outputs(
    *,
    generators: Iterable[str] = DEFAULT_REPORT_GENERATORS,
    seed: int = DEFAULT_DATASET_SEED,
    warmups: int = 0,
    repeats: int = 1,
    results_path: str | Path = DEFAULT_RESULTS_PATH,
    figure_stem: str | Path = DEFAULT_FIGURE_STEM,
    dataset_root: str | Path = DEFAULT_DATASET_ROOT,
    refresh: bool = False,
) -> tuple[tuple[BenchmarkCSVRow, ...], PerformanceCheck]:
    """Create/load datasets, collect rows, write CSV and chart artifacts."""

    records = records_for_generators(
        generators,
        seed=seed,
        root=dataset_root,
        refresh=refresh,
    )
    rows = collect_benchmark_rows(
        records,
        BenchmarkConfig(seed=seed, warmups=warmups, repeats=repeats),
    )
    write_results_csv(rows, results_path)
    stem = Path(figure_stem)
    render_runtime_chart(rows, stem.with_suffix(".png"), stem.with_suffix(".pdf"))
    return rows, check_dmmsy_within_dijkstra(rows)


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point for materializing B7.3 benchmark outputs."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=DEFAULT_DATASET_SEED)
    parser.add_argument("--warmups", type=int, default=0)
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--results", default=str(DEFAULT_RESULTS_PATH))
    parser.add_argument("--figure-stem", default=str(DEFAULT_FIGURE_STEM))
    parser.add_argument("--dataset-root", default=str(DEFAULT_DATASET_ROOT))
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument(
        "--generator",
        action="append",
        dest="generators",
        help="Generator family to include; may be repeated.",
    )
    args = parser.parse_args(argv)

    rows, check = materialize_benchmark_outputs(
        generators=tuple(args.generators) if args.generators else DEFAULT_REPORT_GENERATORS,
        seed=args.seed,
        warmups=args.warmups,
        repeats=args.repeats,
        results_path=args.results,
        figure_stem=args.figure_stem,
        dataset_root=args.dataset_root,
        refresh=args.refresh,
    )
    print(f"wrote {len(rows)} benchmark rows to {args.results}")
    if check.max_ratio is None:
        print("T-17: no n>=1000 DMMSY/Dijkstra comparison rows found")
        return 1
    print(f"T-17: max DMMSY/Dijkstra ratio {check.max_ratio:.3f}x")
    if not check.passed:
        for failing_case in check.failing_cases:
            print(f"T-17 fail: {failing_case}")
        return 1
    return 0


def _bellman_ford_distances(graph: Graph, source: Vertex) -> dict[Vertex, Any]:
    distances, report = bellman_ford(graph, source)
    if report.has_cycle:
        raise ValueError("Bellman-Ford reported a reachable negative cycle")
    return distances


def _goal_vertex(graph: Graph, source: Vertex) -> Vertex:
    for vertex in reversed(graph.vertices()):
        if vertex != source:
            return vertex
    return source


def _has_no_negative_edges(graph: Graph) -> bool:
    return all(edge.weight >= 0 for edge in graph.edges())


def _thorup_compatible(graph: Graph) -> bool:
    return (not graph.is_directed) and all(
        isinstance(edge.weight, int)
        and not isinstance(edge.weight, bool)
        and edge.weight >= 0
        for edge in graph.edges()
    )


def _integer_undirected_graph(graph: Graph) -> Graph:
    converted = Graph(directed=False)
    for vertex in graph.vertices():
        converted.add_vertex(vertex)

    by_pair: dict[frozenset[Vertex], tuple[Vertex, Vertex, int]] = {}
    for edge in graph.edges():
        weight = _integer_weight(edge)
        key = frozenset((edge.source, edge.target))
        current = by_pair.get(key)
        if current is None or weight < current[2]:
            by_pair[key] = (edge.source, edge.target, weight)

    for source, target, weight in by_pair.values():
        if source != target:
            converted.add_edge(source, target, weight)
    return converted


def _integer_weight(edge: Edge) -> int:
    if edge.weight < 0:
        raise ValueError("integer graph view requires non-negative weights")
    if isinstance(edge.weight, int) and not isinstance(edge.weight, bool):
        return edge.weight
    value = int(round(float(edge.weight)))
    if edge.weight > 0 and value < 1:
        return 1
    return value


def _format_float(value: float) -> str:
    return format(float(value), ".17g")


def _chart_series(
    rows: Sequence[BenchmarkCSVRow],
) -> dict[str, dict[str, float]]:
    grouped: dict[str, dict[str, list[float]]] = {}
    for row in rows:
        grouped.setdefault(row.generator, {}).setdefault(row.algorithm_name, []).append(
            row.median_seconds
        )

    return {
        generator: {
            algorithm: statistics.median(values)
            for algorithm, values in algorithms.items()
        }
        for generator, algorithms in grouped.items()
    }


def _write_png_chart(series: dict[str, dict[str, float]], path: Path) -> None:
    width, height = 1200, 720
    pixels = bytearray([255] * width * height * 3)
    panels = _panel_names(series)
    max_value = _max_chart_value(series)
    colors = _algorithm_colors()

    _draw_rect(pixels, width, height, 0, 0, width, height, (255, 255, 255))
    if not panels:
        _write_png(path, width, height, pixels)
        return

    left_margin, right_margin, top_margin, bottom_margin = 70, 30, 50, 80
    gap = 35
    usable_width = width - left_margin - right_margin - gap * (len(panels) - 1)
    panel_width = max(1, usable_width // len(panels))
    plot_height = height - top_margin - bottom_margin

    for panel_index, panel in enumerate(panels):
        x0 = left_margin + panel_index * (panel_width + gap)
        y0 = top_margin
        _draw_rect(pixels, width, height, x0, y0, panel_width, plot_height, (248, 248, 248))
        for grid_index in range(5):
            y = y0 + int(plot_height * grid_index / 4)
            _draw_rect(pixels, width, height, x0, y, panel_width, 1, (220, 220, 220))

        algorithms = [name for name in ALGORITHM_ORDER if name in series[panel]]
        if not algorithms:
            continue
        slot = panel_width / max(1, len(algorithms))
        bar_width = max(8, int(slot * 0.55))
        for algorithm_index, algorithm in enumerate(algorithms):
            value = series[panel][algorithm]
            bar_height = int((value / max_value) * (plot_height - 10))
            x = int(x0 + algorithm_index * slot + (slot - bar_width) / 2)
            y = y0 + plot_height - bar_height
            _draw_rect(
                pixels,
                width,
                height,
                x,
                y,
                bar_width,
                bar_height,
                colors[algorithm],
            )

        _draw_rect(pixels, width, height, x0, y0, 1, plot_height, (80, 80, 80))
        _draw_rect(pixels, width, height, x0, y0 + plot_height, panel_width, 1, (80, 80, 80))

    _write_png(path, width, height, pixels)


def _write_pdf_chart(series: dict[str, dict[str, float]], path: Path) -> None:
    width, height = 792.0, 612.0
    panels = _panel_names(series)
    max_value = _max_chart_value(series)
    colors = _algorithm_colors(normalized=True)
    ops: list[str] = [
        "1 1 1 rg 0 0 792 612 re f",
        _pdf_text(48, 574, "Runtime by Algorithm and Graph Class", size=16),
        _pdf_text(48, 554, "Bar height = median runtime across selected size/density rows.", size=9),
    ]

    if not panels:
        ops.append(_pdf_text(48, 520, "No benchmark rows.", size=11))
        _write_pdf(path, "\n".join(ops), width, height)
        return

    left_margin, right_margin, top_margin, bottom_margin = 54.0, 30.0, 82.0, 84.0
    gap = 24.0
    usable_width = width - left_margin - right_margin - gap * (len(panels) - 1)
    panel_width = usable_width / len(panels)
    plot_height = height - top_margin - bottom_margin
    y0 = bottom_margin

    for panel_index, panel in enumerate(panels):
        x0 = left_margin + panel_index * (panel_width + gap)
        ops.append(f"0.97 0.97 0.97 rg {x0:.2f} {y0:.2f} {panel_width:.2f} {plot_height:.2f} re f")
        ops.append(_pdf_text(x0, y0 + plot_height + 12, panel, size=10))
        for grid_index in range(5):
            y = y0 + plot_height * grid_index / 4
            ops.append(f"0.85 0.85 0.85 RG 0.4 w {x0:.2f} {y:.2f} m {x0 + panel_width:.2f} {y:.2f} l S")
        ops.append(f"0.2 0.2 0.2 RG 0.8 w {x0:.2f} {y0:.2f} m {x0:.2f} {y0 + plot_height:.2f} l S")
        ops.append(f"0.2 0.2 0.2 RG 0.8 w {x0:.2f} {y0:.2f} m {x0 + panel_width:.2f} {y0:.2f} l S")

        algorithms = [name for name in ALGORITHM_ORDER if name in series[panel]]
        if not algorithms:
            continue
        slot = panel_width / len(algorithms)
        bar_width = max(8.0, slot * 0.52)
        for algorithm_index, algorithm in enumerate(algorithms):
            value = series[panel][algorithm]
            bar_height = (value / max_value) * (plot_height - 10.0)
            x = x0 + algorithm_index * slot + (slot - bar_width) / 2
            r, g, b = colors[algorithm]
            ops.append(f"{r:.3f} {g:.3f} {b:.3f} rg {x:.2f} {y0:.2f} {bar_width:.2f} {bar_height:.2f} re f")
            ops.append(_pdf_text(x, y0 - 13, _short_algorithm_label(algorithm), size=6))
            ops.append(_pdf_text(x, y0 + bar_height + 4, f"{value:.4g}s", size=6))

    legend_x, legend_y = 54.0, 36.0
    for index, algorithm in enumerate(ALGORITHM_ORDER):
        x = legend_x + index * 122.0
        r, g, b = colors[algorithm]
        ops.append(f"{r:.3f} {g:.3f} {b:.3f} rg {x:.2f} {legend_y:.2f} 9 9 re f")
        ops.append(_pdf_text(x + 13, legend_y + 1, algorithm, size=8))
    ops.append(_pdf_text(54, 18, f"Global y max: {max_value:.6g} seconds", size=8))
    _write_pdf(path, "\n".join(ops), width, height)


def _panel_names(series: dict[str, dict[str, float]]) -> list[str]:
    known = ["erdos-renyi", "geometric", "dag", "barabasi-albert", "signed-dag"]
    return [name for name in known if name in series] + [
        name for name in sorted(series) if name not in known
    ]


def _max_chart_value(series: dict[str, dict[str, float]]) -> float:
    values = [
        value
        for algorithms in series.values()
        for value in algorithms.values()
        if value >= 0.0
    ]
    if not values:
        return 1.0
    return max(max(values), 1e-12)


def _algorithm_colors(normalized: bool = False):
    colors = {
        "dijkstra": (31, 119, 180),
        "bellman-ford": (255, 127, 14),
        "astar": (44, 160, 44),
        "thorup99": (214, 39, 40),
        "dmmsy": (148, 103, 189),
    }
    if not normalized:
        return colors
    return {
        name: tuple(channel / 255 for channel in rgb)
        for name, rgb in colors.items()
    }


def _short_algorithm_label(name: str) -> str:
    labels = {
        "dijkstra": "Dij",
        "bellman-ford": "BF",
        "astar": "A*",
        "thorup99": "Thorup",
        "dmmsy": "DMMSY",
    }
    return labels[name]


def _draw_rect(
    pixels: bytearray,
    width: int,
    height: int,
    x: int,
    y: int,
    rect_width: int,
    rect_height: int,
    color: tuple[int, int, int],
) -> None:
    x_start = max(0, x)
    x_end = min(width, x + rect_width)
    y_start = max(0, y)
    y_end = min(height, y + rect_height)
    if x_start >= x_end or y_start >= y_end:
        return
    r, g, b = color
    for row in range(y_start, y_end):
        offset = (row * width + x_start) * 3
        for _ in range(x_start, x_end):
            pixels[offset : offset + 3] = bytes((r, g, b))
            offset += 3


def _write_png(path: Path, width: int, height: int, pixels: bytearray) -> None:
    def chunk(kind: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + kind
            + data
            + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        )

    raw = b"".join(
        b"\x00" + bytes(pixels[row * width * 3 : (row + 1) * width * 3])
        for row in range(height)
    )
    data = (
        b"\x89PNG\r\n\x1a\n"
        + chunk("IHDR".encode("ascii"), struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk("IDAT".encode("ascii"), zlib.compress(raw, level=9))
        + chunk("IEND".encode("ascii"), b"")
    )
    path.write_bytes(data)


def _pdf_text(x: float, y: float, text: str, *, size: int) -> str:
    return f"BT /F1 {size} Tf {x:.2f} {y:.2f} Td ({_pdf_escape(text)}) Tj ET"


def _pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _write_pdf(path: Path, content: str, width: float, height: float) -> None:
    content_bytes = content.encode("latin-1", errors="replace")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {width:.0f} {height:.0f}] "
            "/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>"
        ).encode("ascii"),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(content_bytes)).encode("ascii") + b" >>\nstream\n"
        + content_bytes
        + b"\nendstream",
    ]
    payload = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(payload))
        payload.extend(f"{index} 0 obj\n".encode("ascii"))
        payload.extend(obj)
        payload.extend(b"\nendobj\n")

    xref_offset = len(payload)
    payload.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    payload.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        payload.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    payload.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF\n"
        ).encode("ascii")
    )
    path.write_bytes(payload)


if __name__ == "__main__":
    raise SystemExit(main())
