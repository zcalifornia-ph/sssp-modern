# Version 0.1.3 Docs

## Quick Diagnostic Read

This release adds reusable pytest scaffolding on top of the graph, weight, IO, and generator foundation. It still does not implement the shortest-path algorithms themselves. Its job is to give later algorithm work stable test inputs, expected-output fixtures, an optional oracle boundary, and a source-dependency guard.

You are ready to use this release if you can:

- run the current pytest suite,
- inspect JSON golden fixtures,
- understand the difference between runtime package code and test-only oracle code.

## One-Sentence Objective

Add a reusable test harness so later shortest-path implementations can be checked against stable fixtures and optional reference-library results without adding runtime dependencies.

## What Changed

Version `v0.1.3` adds:

- `sssp-modern/tests/conftest.py`
- `sssp-modern/tests/golden/README.md`
- `sssp-modern/tests/golden/tiny-directed.edge-list.json`
- `sssp-modern/tests/golden/tiny-directed.distances-s.json`
- `sssp-modern/tests/oracles.py`
- `sssp-modern/tests/test_harness.py`
- `sssp-modern/tests/test_no_third_party_imports.py`

The new harness provides:

- common pytest fixtures for project paths and golden graph loading,
- a tiny directed graph fixture that reuses the public edge-list JSON format,
- expected shortest-path distances from source `s`,
- a test-only optional NetworkX Dijkstra adapter,
- a static import check for runtime source modules.

## Why It Matters

Algorithm work becomes fragile when each test file invents its own fixtures and path handling. This release gives the project a shared testing surface before Dijkstra, Bellman-Ford, A*, Thorup, and the 2025 algorithm modules begin landing.

The optional oracle adapter is intentionally isolated in the test tree. NetworkX can help validate future algorithm outputs, but the reference implementations under `src/sssp/` remain standard-library code.

## Harness Summary

| Surface | Purpose |
|---|---|
| `project_root` fixture | Resolves the nested Python project root in tests |
| `golden_dir` fixture | Points tests to stable golden input files |
| `tiny_directed_graph` fixture | Loads a reusable directed weighted graph through `sssp.io` |
| `tiny_directed_expected_distances` fixture | Loads expected source-distance data from JSON |
| `networkx_dijkstra_distances` | Provides optional test-only reference distances |
| `test_no_third_party_imports.py` | Confirms runtime source imports stay standard-library or local |

## Golden Fixture Summary

The tiny directed graph contains vertices:

```text
s, a, b, isolated
```

and directed weighted edges:

```text
s -> a : 1.0
s -> b : 4.5
a -> b : 2.0
```

Expected shortest-path distances from source `s` are:

```text
s = 0.0
a = 1.0
b = 3.0
```

The `isolated` vertex is intentionally unreachable from `s`. That gives later algorithm tests a small but useful case covering direct edges, improved paths through an intermediate vertex, and unreachable vertices.

## How To Run The Checks

From the nested project directory:

```powershell
cd sssp-modern
$env:PYTHONPATH='src'
python -m pytest tests/test_graph.py tests/test_weights.py tests/test_io.py tests/test_generators.py tests/test_harness.py tests/test_no_third_party_imports.py
```

Expected result without NetworkX installed:

```text
51 passed, 1 skipped
```

The skipped test is the optional oracle check. If NetworkX is installed in a development environment, that check should run and compare the tiny graph's distances against the expected JSON fixture.

For a syntax/import sanity check:

```powershell
python -m compileall src tests
```

## System View

```text
tests/golden/*.json
  -> pytest fixtures in tests/conftest.py
  -> tests consume Graph + expected distances

Graph
  -> tests/oracles.py
  -> optional NetworkX reference result

src/sssp/*.py
  -> ast import scan
  -> allow stdlib + local package imports only
```

The key boundary is simple: runtime code stays dependency-light, while optional reference-library checks live in tests.

## Validation Summary

The release was validated with:

- golden graph fixture loading tests,
- expected-distance fixture loading tests,
- optional oracle skip behavior when NetworkX is unavailable,
- static import scanning for runtime source modules,
- existing graph, weight, IO, and generator tests from earlier foundation releases,
- compile check over `src` and `tests`.

## Pitfalls

- Run commands from the nested `sssp-modern/` project directory when executing Python tests.
- Set `PYTHONPATH=src` until package metadata is added.
- Do not import test oracle helpers from runtime source modules.
- Do not treat a missing NetworkX install as a foundation-test failure; the oracle check is optional.
- Keep future golden fixtures small, deterministic, and reviewable.

## Next Steps

1. Implement the Dijkstra baseline using the tiny directed fixture as the first correctness case.
2. Add algorithm-specific expected outputs under `tests/golden/` as new implementations land.
3. Include the static import check in later full verification commands.
