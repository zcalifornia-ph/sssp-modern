# Version 0.1.0 Docs

## Quick Diagnostic Read

This release is the first implementation baseline for `sssp-modern`. It does not yet implement Dijkstra, Bellman-Ford, A*, Thorup, or the 2025 directed SSSP algorithm. Instead, it adds the graph and weight primitives those algorithms will share.

You are ready to use this release if you can:

- run Python modules with a temporary `PYTHONPATH`,
- read simple dataclass-based Python code,
- interpret pytest pass/fail output.

## One-Sentence Objective

Provide a small, tested, pure-stdlib Python foundation for weighted graph algorithms and comparison-addition weight checks.

## What Changed

Version `v0.1.0` adds:

- `sssp-modern/src/sssp/__init__.py`
- `sssp-modern/src/sssp/graph.py`
- `sssp-modern/src/sssp/weights.py`
- `sssp-modern/tests/test_graph.py`
- `sssp-modern/tests/test_weights.py`

The new graph layer exposes:

- immutable `Edge` records,
- a minimal adjacency-list `Graph`,
- directed and undirected graph construction,
- tuple snapshots for vertices, neighbors, and edges,
- basic malformed input checks.

The new weight layer exposes:

- immutable `Weight` values,
- equality comparison,
- strict less-than comparison,
- addition and reflected addition,
- explicit rejection of unrelated numeric operations.

## Why It Matters

Shortest-path implementations need a shared graph surface before the individual algorithms can land. Without this baseline, each algorithm would be tempted to invent its own graph format, which would make testing, fixtures, benchmarking, and comparison harder.

The `Weight` wrapper is also important because the modern directed SSSP result is analyzed in a comparison-addition model. This release makes that constraint testable in Python rather than leaving it as a comment.

## How To Run The Checks

From the repository root:

```powershell
cd sssp-modern
$env:PYTHONPATH='src'
python -m pytest tests/test_graph.py tests/test_weights.py
```

Expected result:

```text
11 passed
```

For a syntax/import sanity check:

```powershell
python -m compileall src tests
```

## System View

```text
Graph
  -> stores vertices in insertion order
  -> stores outgoing Edge records per vertex
  -> returns tuple snapshots

Edge
  -> immutable source, target, weight record

Weight
  -> accepts int or float
  -> allows ==, <, +
  -> rejects other numeric operations
```

The key design choice is restraint. This is not a full graph framework. It is the smallest useful foundation for the reference algorithms planned in this repository.

## Validation Summary

The release was validated with:

- graph API tests for directed edges, undirected reciprocal arcs, construction from tuples and `Edge` objects, immutable snapshots, and invalid inputs,
- weight tests for allowed operations, forbidden operations, immutability, invalid construction, and monkeypatch interception,
- compile check over `src` and `tests`.

## Pitfalls

- Run commands from the nested `sssp-modern/` project directory when executing Python tests.
- Set `PYTHONPATH=src` until packaging metadata is added.
- Do not treat `Weight.value` as an algorithm hot-path escape hatch; it is for fixtures, reports, and debugging.
- The current graph layer does not perform algorithm-specific validation such as non-negative weights, integer-only weights, or negative-cycle semantics. Those checks belong in the algorithm modules that need them.

## Next Steps

1. Add graph IO helpers and sample fixtures.
2. Add deterministic random graph generators.
3. Add broader test harness scaffolding and oracle boundaries.
4. Implement the Dijkstra baseline on top of the foundation.
