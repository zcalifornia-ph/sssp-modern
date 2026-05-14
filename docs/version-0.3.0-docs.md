# Version 0.3.0 Docs

## Quick Diagnostic Read

This release turns the previously scoped Thorup work into a tested Python reference implementation. It adds the public `thorup_sssp(graph, source)` API, validates the integer-weight undirected graph contract, and documents why the Python version is a reference implementation rather than a word-RAM performance claim.

You are ready to use this release if you can:

- run pytest from the nested Python project directory,
- distinguish undirected integer-weight graph inputs from the broader graph model,
- read a bucket-based shortest-path queue and compare it against Dijkstra-style distance maps,
- understand that the original Thorup bound depends on a different machine model than CPython.

## One-Sentence Objective

Provide a clear, validated Thorup-style SSSP reference for undirected non-negative integer-weight graphs while keeping the runtime-model caveat explicit.

## What Changed

Version `v0.3.0` adds or updates:

- `sssp-modern/src/sssp/thorup99.py`
- `sssp-modern/tests/test_thorup99.py`
- `sssp-modern/tests/golden/tiny-undirected.edge-list.json`
- `sssp-modern/tests/conftest.py`
- `sssp-modern/docs/decision-thorup-runtime-model.md`
- `sssp-modern/docs/issues/issue-feature-w5-s5-1-add-thorup-1999-hierarchical-bucket-sssp.md`
- `README.md`
- `CHANGELOG.md`
- `docs/version-0.3.0-docs.md`

The new `thorup_sssp(graph, source)` function:

- accepts the existing `Graph` type,
- requires an undirected graph,
- requires the source vertex to exist,
- validates every stored edge weight before traversal,
- rejects negative, non-integer, and boolean weights,
- returns reachable-only integer distance maps,
- keeps production imports limited to Python standard-library and local package roots.

## Why It Matters

Thorup's 1999 result is a key waypoint in the shortest-path literature because it shows how a RAM-model hierarchical bucketing strategy can avoid the comparison-sorting bottleneck for undirected integer-weight SSSP.

This release makes that idea executable in the study package without overstating what Python can do. The implementation demonstrates the bucket-routing structure and validates shortest-path behavior, while the module docstring and decision note state that CPython does not provide the original word-RAM constant-operation model.

## API Summary

```python
from sssp import Graph, thorup_sssp

graph = Graph.from_edges(
    [
        ("s", "a", 10),
        ("s", "c", 3),
        ("c", "b", 2),
        ("b", "a", 2),
        ("a", "d", 1),
    ],
    directed=False,
)

distances = thorup_sssp(graph, "s")
assert distances == {"s": 0, "c": 3, "b": 5, "a": 7, "d": 8}
```

Unreachable vertices are omitted from the returned mapping, matching the package convention used by the Dijkstra baseline.
This release adds the first goal-directed shortest-path implementation in the repository: A* with pluggable heuristics. It also adds focused tests proving that the zero heuristic matches Dijkstra target distances and that Manhattan distance is admissible on a simple grid.

You are ready to use this release if you can:

- run the Python test suite from the nested `sssp-modern/` project directory,
- distinguish Dijkstra's all-reachable-distance output from A*'s one-goal path output,
- explain why an admissible heuristic must not overestimate the remaining path cost.

## One-Sentence Objective

Add a small, pure-stdlib A* implementation with reusable heuristics and tests that prove the implementation stays compatible with the existing graph and Dijkstra baseline.

## What Changed

Version `v0.3.0` adds:

- `sssp-modern/src/sssp/astar.py`
- `sssp-modern/src/sssp/heuristics.py`
- `sssp-modern/tests/test_astar.py`
- `sssp-modern/examples/astar/grid-demo.edge-list.json`
- `docs/version-0.3.0-docs.md`

It also updates:

- `sssp-modern/src/sssp/__init__.py`
- `README.md`
- `CHANGELOG.md`

The new runtime API is:

```python
from sssp import astar, manhattan, zero
```

`astar(graph, source, goal, heuristic)` returns one shortest path as a list of vertices. If the goal is unreachable, it returns an empty list. Missing source or goal vertices and negative edge weights fail fast with `ValueError`.

## Why It Matters

A* adds a useful contrast to Dijkstra. Dijkstra explores by known source distance only; A* also uses an estimate of remaining distance to prioritize the next candidate path. With `zero`, A* behaves like uniform-cost search and can be checked against Dijkstra. With Manhattan distance on a 4-connected unit-cost grid, it demonstrates how a domain-specific heuristic can guide search while preserving optimality.

This gives the project a clean path-oriented implementation without changing the existing graph primitives or the Dijkstra distance-map API.

## System View

```text
Graph(directed=False)
  -> upfront weight validation
  -> hierarchical bucket queue
  -> reachable integer distance map

tests/golden/tiny-undirected.edge-list.json
  -> test_thorup99.py
  -> golden correctness and unreachable-vertex checks

seeded generated graphs
  -> test-only NetworkX oracle when available
  -> randomized agreement check
```

## How To Run The Checks

From the nested project directory:
Graph
  -> Dijkstra: source -> reachable distance map
  -> A*: source + goal + heuristic -> one shortest path
       -> zero heuristic for Dijkstra-equivalence checks
       -> Manhattan heuristic for grid demos
```

The implementation uses the same practical heap pattern as the Dijkstra module: standard-library `heapq`, deterministic tie-breaking, and lazy skipping of stale entries.

## How To Use It

Run the current tests:

```powershell
cd sssp-modern
$env:PYTHONPATH='src'
python -m pytest tests/test_thorup99.py
```

Expected result for this release:

```text
11 passed
```

Run the current full suite:

```powershell
python -m pytest tests
```

Expected result for this release:

```text
70 passed
```

Measure Thorup coverage when `coverage` is installed:

```powershell
python -m coverage run --source=sssp.thorup99 -m pytest tests/test_thorup99.py
python -m coverage report --include='src/sssp/thorup99.py'
```

Expected result for this release:

```text
src\sssp\thorup99.py      76      1    99%
```

For syntax/import sanity:

```powershell
python -m compileall src tests
python -m pytest tests/test_graph.py tests/test_weights.py tests/test_io.py tests/test_generators.py tests/test_harness.py tests/test_no_third_party_imports.py tests/test_dijkstra.py tests/test_astar.py
```

Use A* directly:

```python
from sssp import Graph, astar, zero

graph = Graph.from_edges([
    ("s", "a", 1.0),
    ("a", "goal", 2.0),
    ("s", "goal", 10.0),
])

path = astar(graph, "s", "goal", zero)
assert path == ["s", "a", "goal"]
```

Use Manhattan distance on coordinate vertices:

```python
from sssp import Graph, astar, manhattan

grid = Graph(directed=False)
grid.add_edge((0, 0), (1, 0), 1.0)
grid.add_edge((1, 0), (1, 1), 1.0)
grid.add_edge((0, 0), (0, 1), 1.0)
grid.add_edge((0, 1), (1, 1), 1.0)

path = astar(grid, (0, 0), (1, 1), manhattan)
```

## Validation Summary

The release was validated with:

- golden-fixture correctness on a deterministic undirected integer-weight graph,
- unreachable-vertex behavior,
- a multi-hop path that beats a direct heavier edge,
- missing-source validation,
- directed graph rejection,
- reachable and disconnected negative-weight rejection,
- reachable and disconnected non-integer-weight rejection,
- optional NetworkX oracle agreement on seeded undirected integer-weight graphs,
- dependency-boundary scanning for runtime source files,
- compile checks over `src` and `tests`,
- 99% line coverage for `src/sssp/thorup99.py`.

## Pitfalls

- Run commands from the nested `sssp-modern/` project directory.
- Set `PYTHONPATH=src` until package metadata is added.
- Do not use `thorup_sssp` for directed graphs.
- Do not use `thorup_sssp` with negative, floating-point, boolean, or custom numeric wrapper weights.
- Do not describe the Python implementation as achieving the original word-RAM linear-time bound.
- Keep NetworkX imports out of runtime modules; it remains test-only.

## Next Steps

1. Add Bellman-Ford for negative-edge handling.
2. Add A* with heuristic validation.
3. Reuse Dijkstra and Thorup as baselines when benchmark tooling lands.
4. Carry the runtime-model caveat into the report and presentation discussion.
Completed checks:

- `PYTHONPATH=src python -m pytest tests/test_astar.py`
  - Result: 12 passed.
- `PYTHONPATH=src python -m pytest tests/test_graph.py tests/test_weights.py tests/test_io.py tests/test_generators.py tests/test_harness.py tests/test_no_third_party_imports.py tests/test_dijkstra.py tests/test_astar.py`
  - Result: 71 passed.
- `PYTHONPATH=src python -m coverage run --include='src/sssp/astar.py,src/sssp/heuristics.py' -m pytest tests/test_astar.py`
  - Result: 100% line coverage for the A* and heuristic modules.
- `PYTHONPATH=src python -m compileall src tests`
  - Result: passed.
- `git diff --check`
  - Result: passed.

## Pitfalls

- Do not pass Manhattan distance to arbitrary non-grid vertices; it expects two-coordinate numeric tuples.
- Do not use A* with negative edge weights; Bellman-Ford is the appropriate family for negative-edge handling.
- Do not compare A* and Dijkstra return values directly. Dijkstra returns a distance map, while A* returns a path.
- Do not use third-party shortest-path implementations in runtime source code. Optional external libraries are for test oracles only.

## Next Steps

1. Add Bellman-Ford for negative-edge context and negative-cycle reporting.
2. Add the Thorup reference module with clear word-RAM caveats.
3. Extend examples so each implemented algorithm has documented sample input and output.
4. Feed the Dijkstra and A* implementations into the later benchmark and report sections.
