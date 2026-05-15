# Version 0.4.1 Documentation

## Quick Diagnostic Read

This release adds a reusable benchmark timing harness for the SSSP comparison work. It does not yet define the full benchmark dataset matrix, write CSV files, or generate charts; it establishes the small, testable timing protocol those later outputs will use.

You are ready to review this release if you can:

- run the Python tests from the nested `sssp-modern/` project directory,
- distinguish graph setup time from algorithm runtime,
- read a small dataclass-based API and reason about deterministic tests with an injected clock.

## One-Sentence Objective

Add a reusable benchmark runner that times algorithm callables fairly by excluding warmups and graph setup from reported samples, then summarizes recorded durations with median and interquartile range.

## What Changed

Version `v0.4.1` adds:

- `sssp-modern/src/bench/__init__.py`
- `sssp-modern/src/bench/runner.py`
- `sssp-modern/tests/test_bench_runner.py`
- `docs/version-0.4.1-docs.md`

It also updates:

- `README.md`
- `CHANGELOG.md`

## Why It Matters

The project now has all five algorithm families needed for the eventual empirical comparison: Dijkstra, Bellman-Ford, A*, Thorup-style integer-weight SSSP, and the modern directed-sparse SSSP driver. The next risk is not algorithm availability; it is measurement discipline.

The new harness makes the measurement rules explicit before larger datasets and report figures are added:

- graph construction happens outside the measured interval,
- warmup executions run first and are discarded from reported samples,
- recorded samples are preserved instead of only keeping an aggregate,
- medians and interquartile ranges are computed by the harness,
- the seed, workload name, algorithm name, warmup count, and repeat count travel with every result.

That separation keeps the future CSV and chart code simpler. Later code can focus on selecting datasets and rendering outputs instead of redefining timing policy.

## API Summary

`BenchmarkConfig(seed, warmups=1, repeats=5, clock=time.perf_counter)` defines the timing protocol. It validates that `seed`, `warmups`, and `repeats` are integers, requires non-negative warmups, requires at least one recorded repeat, and accepts a custom clock for deterministic tests.

`BenchmarkCase(name, build_graph, source)` defines one workload. The graph builder receives the seed and must return a `Graph`. The runner validates that the configured source exists in the generated graph.

`AlgorithmSpec(name, run)` defines one algorithm adapter. The callable receives `(graph, source)`. Algorithm-specific wrappers can adapt signatures such as A* goal selection or Bellman-Ford's extra negative-cycle report without complicating the generic runner.

`run_benchmark(case, algorithms, config)` returns one `BenchmarkResult` per algorithm in caller-provided order. Each result includes:

- case name,
- algorithm name,
- seed,
- warmup count,
- repeat count,
- raw elapsed-time samples,
- median seconds,
- IQR seconds.

## Validation Summary

Focused benchmark harness tests:

```powershell
cd sssp-modern
$env:PYTHONPATH='src'
python -m pytest tests/test_bench_runner.py
```

Result:

```text
6 passed
```

Nearby benchmark dependency regression:

```powershell
python -m pytest tests/test_generators.py tests/test_dijkstra.py tests/test_dmmsy.py tests/test_bench_runner.py
```

Result:

```text
49 passed
```

Full nested test suite:

```powershell
python -m pytest tests
```

Result:

```text
135 passed
```

Syntax/import and diff hygiene:

```powershell
python -m compileall src tests
git diff --check
```

Both checks passed for the release scope.

## Pitfalls

- Do not treat `v0.4.1` as the completed experimental evaluation. It is the timing harness release; datasets, result files, and charts are still pending.
- Do not compare raw wall-clock values from two machines as if they were deterministic. The reproducibility guarantee here is the protocol: same seed, same workload order, same algorithm order, and identical summaries under a controlled clock.
- Do not include graph generation, fixture loading, CSV writing, or plotting inside algorithm timing. The runner deliberately builds the graph before starting the clock.
- Do not assume every algorithm has the exact same natural signature. Use `AlgorithmSpec` wrappers to normalize each implementation to `(graph, source)`.

## Next Steps

1. Add the benchmark dataset suite with multiple graph sizes and densities from the existing deterministic generators.
2. Add CSV output and at least one chart from `BenchmarkResult` rows.
3. Compare every algorithm against the Dijkstra baseline and keep the result framing explicit in the report.
4. Keep the focused harness tests in the full regression suite as datasets and plotting are added.
