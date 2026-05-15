# Version 0.4.2 Documentation

## Quick Diagnostic Read

This release adds the deterministic benchmark dataset catalog and cached graph inputs needed for the upcoming empirical comparison work. It does not yet run the full benchmark matrix, write result CSV files, or generate charts.

You are ready to review this release if you can:

- run the Python tests from the nested `sssp-modern/` project directory,
- understand the existing graph generators as deterministic graph factories,
- read JSON edge-list graph fixtures and compare graph fingerprints.

## One-Sentence Objective

Add a reproducible benchmark dataset catalog with cached JSON graph inputs and stable fingerprints so later benchmark execution can time algorithms against known, auditable graph cases.

## What Changed

Version `v0.4.2` adds:

- `sssp-modern/src/bench/datasets.py`
- `sssp-modern/tests/test_bench_datasets.py`
- 30 JSON graph fixtures under `sssp-modern/bench/datasets/`
- `docs/version-0.4.2-docs.md`

It also updates:

- `sssp-modern/src/bench/__init__.py`
- `README.md`
- `CHANGELOG.md`

## Why It Matters

The benchmark runner introduced in `v0.4.1` made timing policy explicit, but it still needed a stable set of graph inputs. This release separates dataset selection from benchmark execution.

The dataset catalog now provides:

- five graph families from the existing deterministic generators,
- three size points: 64, 256, and 1024 vertices,
- two density profiles: sparse and dense,
- fixed-seed JSON edge-list cache files,
- stable SHA-256 fingerprints for generated and cached graphs,
- compatibility metadata for signed negative-edge cases.

That gives later result CSV rows a concrete provenance trail: generator, size, density, seed, graph order, edge count, and fingerprint.

## API Summary

`dataset_profiles()` returns the default 30-profile matrix in deterministic order.

Each `DatasetProfile` records:

- stable profile name,
- generator family,
- size label,
- density label,
- graph order,
- generator parameters,
- source vertex,
- compatible algorithm names,
- whether negative weights may appear.

`build_dataset_graph(profile, seed)` builds a graph using the existing generator functions.

`dataset_fingerprint(graph)` returns a SHA-256 digest over canonical JSON edge-list data.

`dataset_cache_path(profile, seed, root)` returns a deterministic cache path ending in `.edge-list.json`.

`ensure_dataset(profile, seed, root, refresh=False)` creates or reloads one cached graph and returns a `DatasetRecord` containing path, fingerprint, order, and edge count.

`ensure_default_datasets(seed=2026, root=Path("bench/datasets"), refresh=False)` creates or reloads the full default catalog.

## Dataset Matrix

Size points:

| Label | Vertices |
|---|---:|
| small | 64 |
| medium | 256 |
| large | 1024 |

Density profiles:

| Label | Use |
|---|---|
| sparse | Lower edge probability, lower geometric radius, lower attachment count |
| dense | Higher edge probability, higher geometric radius, higher attachment count |

Generator families:

| Family | Notes |
|---|---|
| Erdos-Renyi | Directed, non-negative real weights |
| Geometric | Undirected, distance weights |
| DAG | Directed acyclic, non-negative real weights |
| Barabasi-Albert | Undirected preferential attachment |
| Signed DAG | Directed acyclic, may contain negative weights, marked for Bellman-Ford-only comparisons |

## Validation Summary

Focused dataset tests:

```powershell
cd sssp-modern
$env:PYTHONPATH='src'
python -m pytest tests/test_bench_datasets.py
```

Result:

```text
6 passed
```

Nearby dataset dependency regression:

```powershell
python -m pytest tests/test_generators.py tests/test_io.py tests/test_bench_runner.py tests/test_bench_datasets.py
```

Result:

```text
48 passed
```

Full nested test suite:

```powershell
python -m pytest tests
```

Result:

```text
141 passed
```

Syntax/import and diff hygiene:

```powershell
python -m compileall src tests
git diff --check
```

Both checks passed for the release scope.

Dataset cache generation:

```powershell
$env:PYTHONPATH='src'
python -c "from bench.datasets import ensure_default_datasets; print(len(ensure_default_datasets(refresh=True)))"
```

Result:

```text
30
```

## Pitfalls

- Do not treat this release as benchmark results. These are inputs and cache helpers, not measured runtimes.
- Do not run non-negative-only algorithms on signed negative-edge profiles. Those profiles are retained for Bellman-Ford context and carry compatibility metadata.
- Do not include graph generation time in algorithm timing. Cache loading and graph construction remain setup work for the timing harness.
- Do not assume the default size points are the largest possible report measurements. They are chosen to keep committed validation practical while preserving a 1024-vertex bridge to the later performance sanity run.

## Next Steps

1. Add benchmark execution that consumes `dataset_profiles()` and `ensure_dataset()`.
2. Write benchmark result CSV files with profile names, seeds, fingerprints, edge counts, algorithm names, median runtime, and IQR.
3. Generate at least one chart from the CSV output.
4. Frame every runtime comparison against the Dijkstra baseline in the report and presentation material.
