# Version 0.3.0 Docs

## Quick Diagnostic Read

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
