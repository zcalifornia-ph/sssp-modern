# Version 0.3.5 Documentation

## Quick Diagnostic Read

This release adds bounded pivot selection for the modern directed-sparse shortest-path implementation. The recursive shortest-path routine and top-level driver are still future work.

You are ready to review this release if you can:

- run the Python tests from the nested `sssp-modern/` project directory,
- understand shortest-path relaxation from a labeled frontier,
- read a result object as both algorithm output and test/debug evidence.

## One-Sentence Objective

Add a tested FindPivots helper that performs bounded relaxation, returns the useful source pivots, and preserves the comparison-addition behavior needed by the modern shortest-path implementation.

## What Changed

Version `v0.3.5` adds:

- `sssp-modern/src/sssp/dmmsy/find_pivots.py`
- `sssp-modern/tests/test_dmmsy_find_pivots.py`
- `docs/version-0.3.5-docs.md`

It also updates:

- `sssp-modern/src/sssp/dmmsy/__init__.py`
- `README.md`
- `CHANGELOG.md`

## Why It Matters

The modern directed-sparse SSSP algorithm does not recursively process every current source. It first runs a bounded relaxation pass and keeps only the source roots that are useful enough to seed later recursive calls.

This release implements that shrink step directly:

- distance labels are updated in place,
- only candidates below the active bound enter later frontier layers,
- large frontier growth returns all sources immediately,
- otherwise sources with sufficiently large accepted-relaxation trees become pivots.

That gives the next implementation stage a small, tested API for choosing recursive starting points.

## API Summary

`find_pivots(graph, bound, sources, distances, k)` returns a `FindPivotsResult`.

Inputs:

- `graph`: the directed graph to inspect.
- `bound`: the upper distance bound for this bounded pass.
- `sources`: the current source vertices.
- `distances`: a mutable distance-label map.
- `k`: the bounded relaxation and pivot-size parameter.

Result fields:

- `pivots`: source vertices selected for later recursive work.
- `visited`: vertices reached during bounded relaxation.
- `layers`: the source layer followed by each bounded relaxation layer.
- `saturated`: whether the early large-workload return path was used.

Compatibility helper:

- `FindPivots(...)` mirrors the paper-style name while calling the same implementation.

## Validation Summary

Focused pivot-selection tests:

```powershell
cd sssp-modern
$env:PYTHONPATH='src'
python -m pytest tests/test_dmmsy_find_pivots.py
```

Result:

```text
6 passed
```

Import-boundary regression:

```powershell
python -m pytest tests/test_no_third_party_imports.py
```

Result:

```text
1 passed
```

Nearby modern-SSSP regression coverage:

```powershell
python -m pytest tests/test_dmmsy_transform.py tests/test_dmmsy_blocklist.py tests/test_dmmsy_find_pivots.py tests/test_no_third_party_imports.py
```

Result:

```text
17 passed
```

Full nested test suite:

```powershell
python -m pytest tests
```

Result:

```text
107 passed
```

Focused coverage:

```powershell
python -m coverage run --include='src/sssp/dmmsy/find_pivots.py' -m pytest tests/test_dmmsy_find_pivots.py
python -m coverage report --include='src/sssp/dmmsy/find_pivots.py'
```

Recorded focused coverage:

- `src/sssp/dmmsy/find_pivots.py`: 95%

Syntax/import and diff hygiene:

```powershell
python -m compileall src tests
git diff --check
```

Both checks passed for the release scope.

## Pitfalls

- Do not treat this as the completed modern shortest-path implementation; recursive processing and the public driver are still pending.
- Do not replace the bounded relaxation with Dijkstra. The helper is intentionally shaped around the published pivot-selection step.
- Do not use `<=`, `>`, `>=`, subtraction, or numeric conversion on `Weight` values when extending this module. The implementation expresses non-strict relaxation through `<` plus `==`.
- Do not assume the returned `visited` set is a final shortest-path result. It is a bounded helper output for the later recursive routine.

## Next Steps

1. Add the recursive bounded shortest-path routine that consumes the selected pivots.
2. Add top-level driver coverage against the Dijkstra baseline on randomized non-negative graphs.
3. Keep the transform, block-list, and pivot-selection tests in the regression suite as the driver comes together.
4. Add benchmark and report material only after the complete modern implementation is correctness-checked.
