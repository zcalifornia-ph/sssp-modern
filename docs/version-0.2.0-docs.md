# Version 0.2.0 Docs

## Quick Diagnostic Read

This release adds the first shortest-path algorithm implementation: a binary-heap Dijkstra baseline for non-negative weighted graphs. It builds directly on the existing graph foundation, golden fixtures, seeded generators, and test-only oracle boundary.

You are ready to use this release if you can:

- run pytest from the nested Python project directory,
- read an adjacency-list relaxation loop,
- distinguish runtime package code from test-only validation helpers.

## One-Sentence Objective

Provide a clear, tested Dijkstra reference implementation that later algorithms and benchmarks can compare against.

## What Changed

Version `v0.2.0` adds:

- `sssp-modern/src/sssp/dijkstra.py`
- `sssp-modern/tests/test_dijkstra.py`
- `sssp-modern/examples/dijkstra/tiny-directed.distances-s.json`

It also updates:

- `sssp-modern/src/sssp/__init__.py`
- `README.md`
- `CHANGELOG.md`

The new `dijkstra(graph, source)` function:

- accepts the existing `Graph` type,
- requires a source vertex already present in the graph,
- supports non-negative edge weights,
- returns distances for reachable vertices only,
- rejects negative edges because those belong to Bellman-Ford-style handling.

## Why It Matters

Dijkstra is the comparison baseline for the rest of this study. Without a stable baseline, later implementations and benchmark charts would lack a trustworthy reference point.

This release keeps the implementation intentionally small. The algorithm uses Python's standard-library `heapq`, a deterministic tie-breaker counter, and the existing `Graph.neighbors()` interface. NetworkX remains test-only and is used only to validate results, not to implement runtime behavior.

## API Summary

```python
from sssp import Graph, dijkstra

graph = Graph.from_edges([
    ("s", "a", 1.0),
    ("s", "b", 4.5),
    ("a", "b", 2.0),
])

distances = dijkstra(graph, "s")
assert distances == {"s": 0.0, "a": 1.0, "b": 3.0}
```

Unreachable vertices are omitted from the returned mapping. This matches the current golden fixture and the behavior of the test oracle.

## System View

```text
Graph
  -> dijkstra(graph, source)
  -> reachable distance map

tests/golden/tiny-directed.edge-list.json
  -> test_dijkstra.py
  -> golden correctness check

seeded generated graphs
  -> test-only NetworkX oracle
  -> randomized agreement check
```

## How To Run The Checks

From the nested project directory:

```powershell
cd sssp-modern
$env:PYTHONPATH='src'
python -m pytest tests/test_dijkstra.py
```

Expected result:

```text
7 passed
```

Run the current combined implementation suite:

```powershell
python -m pytest tests/test_graph.py tests/test_weights.py tests/test_io.py tests/test_generators.py tests/test_harness.py tests/test_no_third_party_imports.py tests/test_dijkstra.py
```

Expected result:

```text
59 passed
```

Measure Dijkstra coverage when `coverage` is installed:

```powershell
python -m coverage run --include='src/sssp/dijkstra.py' -m pytest tests/test_dijkstra.py
python -m coverage report --include='src/sssp/dijkstra.py'
```

Expected result for this release:

```text
src\sssp\dijkstra.py      28      0   100%
```

For syntax/import sanity:

```powershell
python -m compileall src tests
```

## Validation Summary

The release was validated with:

- golden-fixture correctness on the tiny directed graph,
- seeded randomized agreement with NetworkX as a test-only oracle,
- missing-source validation,
- negative-edge rejection,
- isolated-source behavior,
- dependency-boundary scanning for runtime source files,
- compile checks over `src` and `tests`,
- 100% line coverage for `src/sssp/dijkstra.py`.

## Pitfalls

- Run commands from the nested `sssp-modern/` project directory.
- Set `PYTHONPATH=src` until package metadata is added.
- Do not use Dijkstra for graphs with negative edges.
- Keep NetworkX imports out of runtime modules.
- Treat missing vertices as input errors, not as unreachable vertices.

## Next Steps

1. Add Bellman-Ford for negative-edge handling.
2. Reuse the Dijkstra tests and oracle pattern for later algorithms.
3. Use Dijkstra as the baseline when the benchmark harness lands.
