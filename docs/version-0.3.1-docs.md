# Version 0.3.1 Docs

## Quick Diagnostic Read

This release completes the Bellman-Ford validation pass. It confirms the public `bellman_ford(graph, source)` API, the reachable negative-cycle report contract, the import boundary, and the Dijkstra regression path, then closes the public Bellman-Ford issue with validation evidence.

You are ready to use this release if you can:

- run pytest from the nested Python project directory,
- distinguish Bellman-Ford's negative-edge support from Dijkstra's non-negative-weight precondition,
- read the returned `(distances, report)` tuple,
- understand that reachable negative cycles invalidate ordinary shortest-path interpretation for the affected source.

## One-Sentence Objective

Provide a validated Bellman-Ford reference implementation with explicit negative-cycle reporting and public evidence that the implementation meets its documented test and coverage targets.

## What Changed

Version `v0.3.1` updates:

- `sssp-modern/src/sssp/bellman_ford.py`
- `README.md`
- `CHANGELOG.md`
- GitHub issue `#4`
- `docs/version-0.3.1-docs.md`

The Bellman-Ford module now states the source-paper references, reachable negative-cycle semantics, and O(mn) relaxation-loop complexity in its module documentation. The public issue record was updated with validation evidence and closed as completed.

## Why It Matters

Bellman-Ford is the repository's baseline for graphs that can contain negative edge weights. Dijkstra remains faster for non-negative edges, but Bellman-Ford gives the study package a clear reference point for negative-edge behavior and reachable negative-cycle detection.

This release also turns the validation evidence into a public handoff: the implementation, tests, import boundary, regression check, and coverage result can be reviewed without rerunning the entire project.

## API Summary

```python
from sssp import Graph, bellman_ford

graph = Graph.from_edges([
    ("s", "a", 2.0),
    ("a", "b", -1.0),
    ("b", "c", 2.0),
])

distances, report = bellman_ford(graph, "s")
assert distances == {"s": 0.0, "a": 2.0, "b": 1.0, "c": 3.0}
assert not report.has_cycle
```

For a reachable negative cycle, the returned report sets `has_cycle` to `True`. Unreachable vertices remain omitted from the distance map, matching the package convention used by the Dijkstra baseline.

## System View

```text
Graph
  -> bellman_ford(graph, source)
      -> source validation
      -> O(mn) relaxation loop
      -> final reachable negative-cycle check
      -> (reachable distance map, NegativeCycleReport)

tests/test_bellman_ford.py
  -> golden directed fixture
  -> negative-edge no-cycle case
  -> reachable negative-cycle case
  -> unreachable negative-cycle boundary
  -> optional test-only oracle comparison
```

## How To Run The Checks

From the nested project directory:

```powershell
cd sssp-modern
$env:PYTHONPATH='src'
python -m pytest tests/test_bellman_ford.py tests/test_no_third_party_imports.py tests/test_dijkstra.py
```

Expected result for this release:

```text
17 passed
```

Measure Bellman-Ford coverage when `coverage` is installed:

```powershell
python -m coverage run --include='src/sssp/bellman_ford.py' -m pytest tests/test_bellman_ford.py
python -m coverage report -m src/sssp/bellman_ford.py
```

Expected result for this release:

```text
src/sssp/bellman_ford.py      32      0   100%
```

## Validation Summary

Completed checks:

- `$env:PYTHONPATH='src'; python -m pytest tests/test_bellman_ford.py tests/test_no_third_party_imports.py tests/test_dijkstra.py`
  - Result: 17 passed.
- `$env:PYTHONPATH='src'; python -m coverage run --include='src/sssp/bellman_ford.py' -m pytest tests/test_bellman_ford.py`
  - Result: 9 passed.
- `python -m coverage report -m src/sssp/bellman_ford.py`
  - Result: 32 statements, 0 missed, 100% line coverage.

The checked behaviors include:

- golden shortest-path distances on the tiny directed fixture,
- omission of unreachable vertices,
- missing-source validation,
- negative edges without negative cycles,
- reachable negative-cycle reporting,
- unreachable negative-cycle isolation,
- optional test-only oracle comparison,
- standard-library/local-only production imports,
- existing Dijkstra regression behavior.

## Pitfalls

- Run commands from the nested `sssp-modern/` project directory.
- Set `PYTHONPATH=src` until package metadata is added.
- Do not treat `report.has_cycle=True` as an ordinary shortest-path result for the affected source.
- Keep optional oracle libraries out of runtime source code; they belong in tests only.

## Next Steps

1. Keep Bellman-Ford as the negative-edge baseline when later algorithms and report sections compare supported graph families.
2. Add examples that show the returned negative-cycle report beside ordinary reachable distances.
3. Continue the remaining modern directed-sparse SSSP implementation and comparative analysis work.
