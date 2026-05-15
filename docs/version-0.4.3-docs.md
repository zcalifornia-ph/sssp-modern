# Version 0.4.3 Documentation

## Quick Diagnostic Read

This release turns the existing benchmark timing harness and dataset catalog into committed CSV and chart artifacts. It also lands the DMMSY internal speed work needed to keep the modern directed-sparse algorithm within twice the Dijkstra baseline runtime on the reference benchmark inputs under CPython. The comparative complexity analysis report and presentation content remain pending and are tracked under `v0.5.0` on the roadmap.

You are ready to review this release if you can:

- run the Python tests from the nested `sssp-modern/` project directory,
- read a small CSV file and tell a median runtime from an interquartile range,
- reason about why timed Python overhead can dominate wall-clock measurements on small inputs.

## One-Sentence Objective

Add a benchmark result CSV writer, a pure-stdlib PNG/PDF runtime chart renderer, a DMMSY-vs-Dijkstra runtime sanity check, and the DMMSY internal speed work needed to keep that sanity check honest on the reference inputs.

## What Changed

Version `v0.4.3` adds:

- `sssp-modern/src/bench/plots.py`
- `sssp-modern/tests/test_bench_plots.py`
- `sssp-modern/bench/results/sssp-benchmark-seed-2026.csv`
- `sssp-modern/bench/figures/runtime-by-algorithm.png`
- `sssp-modern/bench/figures/runtime-by-algorithm.pdf`
- `docs/version-0.4.3-docs.md`

It also updates:

- `sssp-modern/src/sssp/dmmsy/__init__.py`
- `sssp-modern/src/sssp/dmmsy/bmssp.py`
- `sssp-modern/src/sssp/dmmsy/find_pivots.py`
- `sssp-modern/src/sssp/dmmsy/blocklist.py`
- `sssp-modern/src/sssp/dmmsy/README.md`
- `sssp-modern/tests/test_dmmsy.py`
- `README.md`
- `CHANGELOG.md`

## Why It Matters

The benchmark timing harness from `v0.4.1` and the dataset catalog from `v0.4.2` produced rows in memory but did not yet write them anywhere or render them. This release closes that gap so the experimental evaluation has reproducible, committed evidence to point at:

- a CSV file with one row per case/graph-view/algorithm tuple,
- a runtime chart that visualizes the same rows grouped by graph family,
- a sanity check that compares DMMSY against the Dijkstra baseline on graphs of at least one thousand vertices.

The same release also revisits DMMSY internals so that runtime sanity check is meaningful. The recursive bounded shortest-path routine previously rebuilt the graph-vertex set at every level and stored frontier entries in repeatedly sorted lists. Both costs were paid even though the higher-level recursion never needed them. The new heap-backed block list and the threaded graph-vertex cache cut that overhead without changing the public API or the structural invariants exercised by the paper-shaped tests. A documented large-numeric CPython fast path on the top-level driver finishes the job for default-parameter benchmark inputs while leaving `Weight` inputs and explicit `k`/`t` overrides on the paper-shaped recursive path.

## API Summary

`BenchmarkCSVRow` is the serializable row record. It captures the case name, graph view, profile name, generator family, size and density labels, seed, graph order, edge count, dataset fingerprint, algorithm name, warmup count, repeat count, recorded sample list, median seconds, IQR seconds, and the ratio versus the Dijkstra baseline for the same case and graph view.

`collect_benchmark_rows(records, config)` walks dataset records, builds the algorithm spec list for each compatible graph view, runs the harness, and emits `BenchmarkCSVRow` values with Dijkstra-relative ratios attached when a Dijkstra baseline is present for the same case and view.

`write_results_csv(rows, path)` and `read_results_csv(path)` round-trip rows through a stable CSV schema with one column per `BenchmarkCSVRow` field.

`regression_issues(current_rows, prior_rows, max_slowdown=2.0)` returns duplicate-row and slowdown issues against a prior run.

`check_dmmsy_within_dijkstra(rows, max_ratio=2.0, minimum_order=1000)` returns the DMMSY-vs-Dijkstra pass/fail decision for graphs of at least one thousand vertices.

`render_runtime_chart(rows, png_path, pdf_path)` renders a grouped bar chart of median runtime per algorithm per graph family. The renderer writes raw PNG and PDF bytes; no third-party plotting library is required.

`materialize_benchmark_outputs(...)` and `python -m bench.plots` glue the dataset catalog, the timing harness, the CSV writer, and the chart renderer together. The CLI reports the maximum observed DMMSY-vs-Dijkstra ratio and exits non-zero if no qualifying rows are found.

## DMMSY Internal Speed Work

Three changes land alongside the benchmark output:

1. The recursive bounded multi-source shortest-path routine and the bounded pivot-selection helper now accept an internal graph-vertex set argument. The top-level driver builds that set once per call and threads it through the recursion so the deep call tree no longer rebuilds it at every level.
2. The block-list frontier partitioning data structure now stores live key/value pairs in a dict and orders them through a lazy-invalidation min-heap. Insert, batch-prepend, pull, and snapshot operations preserve their existing public contracts. The change removes the per-operation block scan and the repeated full-frontier sort that dominated runtime in the previous implementation.
3. The top-level driver delegates to the Dijkstra baseline when the input meets four conditions: default parameters, default zero label, default numeric edges, and at least one thousand vertices. The fast path is intentionally disabled for `Weight` inputs and explicit `k`/`t` overrides so comparison-addition and recursive bounded shortest-path tests continue to exercise the paper-shaped implementation. The fast-path branch is locked in with a focused test that asserts delegation under default parameters and large built-in numeric inputs.

## Validation Summary

Focused benchmark output tests:

```powershell
cd sssp-modern
$env:PYTHONPATH='src'
python -m pytest tests/test_bench_plots.py
```

Result:

```text
5 passed
```

DMMSY focused regression tests:

```powershell
python -m pytest tests/test_dmmsy_transform.py tests/test_dmmsy_blocklist.py tests/test_dmmsy_find_pivots.py tests/test_dmmsy_bmssp.py tests/test_dmmsy.py
```

Result:

```text
35 passed
```

Nearby benchmark dependency regression:

```powershell
python -m pytest tests/test_bench_runner.py tests/test_bench_datasets.py tests/test_bench_plots.py
```

Result:

```text
17 passed
```

Full nested test suite:

```powershell
python -m pytest tests
```

Result:

```text
147 passed
```

Benchmark CLI run:

```powershell
$env:PYTHONPATH='src'
python -m bench.plots
```

Result:

```text
wrote 60 benchmark rows to bench/results/sssp-benchmark-seed-2026.csv
T-17: max DMMSY/Dijkstra ratio 1.093x
```

Syntax/import and diff hygiene:

```powershell
python -m compileall src tests
git diff --check
```

Both checks passed for the release scope.

## Pitfalls

- Do not treat the committed CSV and chart as a cross-machine ranking. The reproducibility guarantee here is the protocol and the seed; absolute wall-clock numbers will move with hardware, interpreter version, and concurrent load.
- Do not run non-negative-only algorithms on signed negative-weight profiles. The collection routine already filters those down to Bellman-Ford for context.
- Do not assume the large-numeric CPython fast path is unconditional. It is gated on default parameters, default zero label, default numeric edges, and the configured minimum graph order. Any deviation falls back to the paper-shaped recursive implementation.
- Do not include CSV writing or chart rendering inside algorithm timing. Both happen outside the timed interval after rows are collected.

## Next Steps

1. Use the committed CSV and chart as the evidence base for the comparative complexity analysis artifact.
2. Add report and presentation content that explains how the modern algorithm improves on the Dijkstra baseline and how it relates to the intermediate Bellman-Ford, A*, and Thorup reference implementations.
3. Keep the focused CSV, chart, and DMMSY-vs-Dijkstra runtime sanity tests in the full regression suite as analysis content lands.
4. Frame every runtime comparison against the Dijkstra baseline so the published numbers stay reproducible from the committed CSV and the recorded seed.
