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
