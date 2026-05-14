# Version 0.3.3 Documentation

## Quick Diagnostic Read

This release adds the first implementation support for the 2025 directed-sparse shortest-path algorithm: a constant-degree graph transformation with focused correctness tests. The full shortest-path algorithm is still future work.

You are ready to review this release if you can:

- run the Python tests from the nested `sssp-modern/` project directory,
- understand why reducing high-degree vertices to bounded-degree port vertices helps later graph algorithms,
- compare shortest-path distance maps before and after a graph transformation.

## One-Sentence Objective

Add a tested graph adapter that preserves shortest-path distances while turning arbitrary-degree directed graphs into bounded-degree transformed graphs for the modern directed-sparse SSSP implementation.

## What Changed

Version `v0.3.3` adds:

- `sssp-modern/src/sssp/dmmsy/__init__.py`
- `sssp-modern/src/sssp/dmmsy/transform.py`
- `sssp-modern/tests/test_dmmsy_transform.py`

It also updates:

- `README.md`
- `CHANGELOG.md`
- `docs/version-0.3.3-docs.md`

## Why It Matters

The modern directed-sparse SSSP algorithm assumes a constant-degree graph. Real input graphs can have vertices with many incoming or outgoing edges, so the implementation needs a preprocessing step before later shortest-path machinery can be built safely.

This release adds that preprocessing step as an independently testable module. Each original vertex is represented by deterministic port vertices connected by zero-weight cycle edges. Each original edge becomes one cross edge between a source port and a target port. After running a shortest-path algorithm on the transformed graph, distances can be projected back to the original vertices.

The important property is preservation:

- shortest paths in the original graph can be simulated in the transformed graph,
- zero-weight port cycles do not change path length,
- projected transformed distances match original distances on the tested graphs.

## API Summary

`constant_degree_transform(graph, zero_weight=0.0)` returns a `ConstantDegreeTransform` object with:

- `graph`: the transformed directed graph,
- `representatives`: one transformed source vertex per original vertex,
- `ports`: all transformed vertices grouped by original vertex,
- `project_distances(distances)`: a helper that maps transformed distances back to original vertices.

The transform keeps the shared graph primitive unchanged. That keeps the new logic local to the modern SSSP package area and avoids disturbing the already validated Dijkstra, Bellman-Ford, A*, and Thorup modules.

## Validation Summary

The release was checked with:

```powershell
cd sssp-modern
$env:PYTHONPATH='src'
python -m pytest tests/test_dmmsy_transform.py
```

Result:

```text
4 passed
```

The import-boundary check was also run:

```powershell
python -m pytest tests/test_no_third_party_imports.py
```

Result:

```text
1 passed
```

Nearby regression coverage:

```powershell
python -m pytest tests/test_graph.py tests/test_weights.py tests/test_dijkstra.py tests/test_no_third_party_imports.py tests/test_dmmsy_transform.py
```

Result:

```text
23 passed
```

Full nested test suite:

```powershell
python -m pytest tests
```

Result:

```text
95 passed
```

Focused coverage:

```powershell
python -m coverage run --include='src/sssp/dmmsy/transform.py' -m pytest tests/test_dmmsy_transform.py
python -m coverage report --include='src/sssp/dmmsy/transform.py'
```

Recorded focused coverage:

- `src/sssp/dmmsy/transform.py`: 100%

Syntax/import and diff hygiene:

```powershell
python -m compileall src tests
git diff --check
```

Both checks passed for the release scope.

## Pitfalls

- Do not treat this as the completed 2025 shortest-path implementation; it is the graph-transformation foundation for that implementation.
- Do not compare transformed graph vertex counts directly with original graph vertex counts; the transform intentionally expands vertices into incident-edge ports.
- Do not remove the projection step when comparing distances, because transformed vertices are internal representation details.
- Do not assume the transform improves Python runtime by itself. Its purpose is structural correctness for the later algorithm implementation.

## Next Steps

1. Add the block-list data structure needed by the later directed-sparse SSSP implementation.
2. Add pivot-selection logic and test its invariants against small reachable graph regions.
3. Add the recursive shortest-path routine and compare final distances against Dijkstra on randomized non-negative graphs.
4. Keep the import-boundary and distance-preservation tests in the regression suite as later modules are added.
