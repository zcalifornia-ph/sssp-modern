# Version 0.3.0 Docs

## Quick Diagnostic Read

This release adds two reference implementations to the study package: A* for goal-directed shortest paths and a Thorup-style hierarchical bucket reference for undirected non-negative integer-weight graphs. It also records the runtime-model caveat for Thorup so the repository does not overstate what CPython can prove about the original word-RAM result.

You are ready to use this release if you can:

- run pytest from the nested `sssp-modern/` project directory,
- distinguish Dijkstra's all-reachable-distance output from A*'s one-goal path output,
- explain why an admissible heuristic must not overestimate remaining path cost,
- distinguish Thorup's word-RAM theoretical model from this Python reference implementation.

## One-Sentence Objective

Add validated A* and Thorup-style reference implementations while keeping their graph-family assumptions and runtime-model caveats explicit.

## What Changed

Version `v0.3.0` adds or updates:

- `sssp-modern/src/sssp/astar.py`
- `sssp-modern/src/sssp/heuristics.py`
- `sssp-modern/src/sssp/thorup99.py`
- `sssp-modern/src/sssp/__init__.py`
- `sssp-modern/tests/test_astar.py`
- `sssp-modern/tests/test_thorup99.py`
- `sssp-modern/examples/astar/grid-demo.edge-list.json`
- `sssp-modern/tests/golden/tiny-undirected.edge-list.json`
- `sssp-modern/tests/conftest.py`
- `sssp-modern/docs/decision-thorup-runtime-model.md`
- `README.md`
- `CHANGELOG.md`
- `docs/version-0.3.0-docs.md`

The new public APIs are:

```python
from sssp import astar, manhattan, thorup_sssp, zero
```

`astar(graph, source, goal, heuristic)` returns one shortest path as a list of vertices. If the goal is unreachable, it returns an empty list. Missing source or goal vertices and negative edge weights fail fast with `ValueError`.

`thorup_sssp(graph, source)` returns a reachable-only distance map for undirected graphs with non-negative integer weights. Directed graphs, missing sources, negative weights, non-integer weights, and boolean weights fail fast with `ValueError`.

## Why It Matters

A* adds the repository's goal-directed shortest-path implementation. With `zero`, it behaves like uniform-cost search and can be checked against Dijkstra target distances. With Manhattan distance on a 4-connected unit-cost grid, it demonstrates how a domain-specific heuristic can guide search while preserving optimality.

Thorup's 1999 result is a key waypoint in the shortest-path literature because it shows how a RAM-model hierarchical bucketing strategy can avoid the comparison-sorting bottleneck for undirected integer-weight SSSP. This repository implements a documented Python reference to demonstrate the behavior and structure without claiming CPython achieves the original linear-time word-RAM bound.

## System View

```text
Graph
  -> Dijkstra: source -> reachable distance map
  -> A*: source + goal + heuristic -> one shortest path
       -> zero heuristic for Dijkstra-equivalence checks
       -> Manhattan heuristic for grid demos
  -> Thorup-style bucket reference:
       -> undirected graph
       -> non-negative integer weights
       -> reachable distance map
```

## How To Run The Checks

From the nested project directory:

```powershell
cd sssp-modern
$env:PYTHONPATH='src'
python -m pytest tests/test_astar.py tests/test_thorup99.py
```

Run the broader implementation suite:

```powershell
python -m pytest tests
```

Measure focused coverage when `coverage` is installed:

```powershell
python -m coverage run --include='src/sssp/astar.py,src/sssp/heuristics.py,src/sssp/thorup99.py' -m pytest tests/test_astar.py tests/test_thorup99.py
python -m coverage report -m src/sssp/astar.py src/sssp/heuristics.py src/sssp/thorup99.py
```

## Validation Summary

The A* release evidence covered:

- zero-heuristic equivalence with Dijkstra target distances,
- Manhattan admissibility on a 4-connected unit-cost grid,
- path reconstruction,
- unreachable-goal empty path behavior,
- source and goal validation,
- negative-edge rejection,
- package exports for `astar`, `zero`, and `manhattan`.

The Thorup release evidence covered:

- golden correctness on an integer-weight undirected graph,
- unreachable vertices,
- multi-hop paths beating a direct heavier edge,
- missing-source validation,
- directed graph rejection,
- reachable and disconnected invalid-weight rejection,
- optional NetworkX oracle agreement on seeded undirected integer-weight graphs,
- public runtime-model caveat in code and a decision note.

## Pitfalls

- Run commands from the nested `sssp-modern/` project directory.
- Set `PYTHONPATH=src` until package metadata is added.
- Do not pass Manhattan distance to arbitrary non-grid vertices; it expects two-coordinate numeric tuples.
- Do not use A* with negative edge weights; Bellman-Ford is the appropriate family for negative-edge handling.
- Do not use `thorup_sssp` for directed graphs or non-integer weights.
- Do not describe the Python Thorup reference as achieving the original word-RAM linear-time bound.
- Keep optional oracle libraries out of runtime source code. Optional external libraries are for tests only.

## Next Steps

1. Keep Dijkstra, Bellman-Ford, A*, and Thorup available as baselines for the modern directed-sparse SSSP implementation.
2. Add examples that show A* paths and Thorup distance maps beside their expected outputs.
3. Build the benchmark harness and report/deck sections once the remaining modern algorithm implementation lands.
