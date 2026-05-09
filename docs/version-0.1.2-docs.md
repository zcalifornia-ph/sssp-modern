# Version 0.1.2 Docs

## Quick Diagnostic Read

This release adds deterministic graph generators on top of the graph, weight, and JSON fixture foundation. It still does not implement the shortest-path algorithms themselves. Its job is to make repeatable benchmark-style inputs available before algorithm modules and timing harnesses start consuming them.

You are ready to use this release if you can:

- run the current pytest suite,
- understand seeded pseudorandom generation,
- inspect a generated `Graph` for vertices, edges, directedness, and weights.

## One-Sentence Objective

Add seeded, pure-stdlib graph generators so benchmark inputs can be reproduced exactly across local runs.

## What Changed

Version `v0.1.2` adds:

- `sssp-modern/src/sssp/generators.py`
- `sssp-modern/tests/test_generators.py`
- package-root exports for the generator helpers in `sssp-modern/src/sssp/__init__.py`

The new generator module exposes:

- `erdos_renyi_graph`
- `random_geometric_graph`
- `dag_graph`
- `barabasi_albert_graph`
- `signed_edge_graph`

Each generator accepts an explicit `seed` and uses a local `random.Random` instance, so generator calls do not mutate Python's process-global random state.

## Why It Matters

Shortest-path comparisons need input graphs that can be recreated exactly. A seeded generator suite gives the project a stable way to:

- produce sparse or dense directed graphs,
- exercise geometric and preferential-attachment shapes,
- build acyclic inputs for algorithms that benefit from topological structure,
- include signed-edge graphs for later Bellman-Ford coverage,
- keep benchmark setup reproducible without adding dependencies.

The implementation deliberately stays inside Python's standard library. That preserves the repository's current dependency boundary while still preparing useful datasets for later algorithm work.

## Generator Summary

| Generator | Shape | Default directedness | Weight behavior |
|---|---|---:|---|
| `erdos_renyi_graph` | Independent edge sampling by probability | Directed | Uniform non-negative weights |
| `random_geometric_graph` | Points in `[0, 1] x [0, 1]` linked within a radius | Undirected | Distance weights by default, optional uniform weights |
| `dag_graph` | Forward-only directed acyclic graph | Directed | Uniform non-negative weights |
| `barabasi_albert_graph` | Preferential-attachment graph | Undirected | Uniform non-negative weights |
| `signed_edge_graph` | Directed graph with configurable negative-edge fraction | Directed | Signed uniform magnitudes |

All generated vertices use stable string identifiers: `v0`, `v1`, ..., `v{n-1}`.

## How To Run The Checks

From the nested project directory:

```powershell
cd sssp-modern
$env:PYTHONPATH='src'
python -m pytest tests/test_graph.py tests/test_weights.py tests/test_io.py tests/test_generators.py
```

Expected result:

```text
47 passed
```

For a syntax/import sanity check:

```powershell
python -m compileall src tests
```

## System View

```text
seed + parameters
  -> local random.Random(seed)
  -> generator-specific edge selection
  -> Graph(vertices, weighted edges)
  -> tests compare graph signatures across repeated runs
```

The key invariant is reproducibility: the same generator, parameters, and seed must produce the same directedness, vertex order, edge order, and weights on repeated runs.

## Validation Summary

The release was validated with:

- fixed-seed determinism tests across all five generators,
- a check that generator calls do not alter process-global random state,
- edge-probability extreme tests for Erdos-Renyi graphs,
- distance-weight and symmetric-arc tests for random geometric graphs,
- forward-edge invariants for directed acyclic graphs,
- undirected shape checks for preferential-attachment graphs,
- positive and negative weight coverage for signed-edge graphs,
- parameter validation tests,
- existing graph, weight, and IO tests from earlier foundation releases,
- compile check over `src` and `tests`.

## Pitfalls

- Run commands from the nested `sssp-modern/` project directory when executing Python tests.
- Set `PYTHONPATH=src` until package metadata is added.
- `signed_edge_graph` can emit negative weights; do not feed those graphs into non-negative-only algorithms without validation.
- Non-signed generators reject negative weight ranges because they are intended for non-negative shortest-path inputs.
- `barabasi_albert_graph` requires `attachments >= 1` and `attachments < n`.
- `random_geometric_graph` uses geometric distance as the weight unless a `weight_range` is provided.

## Next Steps

1. Add broader test harness scaffolding and oracle boundaries.
2. Start the Dijkstra reference implementation on top of the graph and generator foundation.
3. Use these generators later for reproducible benchmark datasets and comparison charts.
