# Version 0.3.6 Documentation

## Quick Diagnostic Read

This release adds the recursive bounded multi-source shortest-path routine for the modern directed-sparse shortest-path implementation. The top-level public driver and benchmark harness are still future work.

You are ready to review this release if you can:

- run the Python tests from the nested `sssp-modern/` project directory,
- understand bounded shortest-path relaxation from a labeled frontier,
- read a result object as both algorithm output and test/debug evidence.

## One-Sentence Objective

Add a tested recursive bounded multi-source shortest-path routine that consumes the pivot-selection and block-list helpers, returns a partial-or-complete boundary with the vertices below it, and preserves the strict comparison-addition behavior required by the modern shortest-path implementation.

## What Changed

Version `v0.3.6` adds:

- `sssp-modern/src/sssp/dmmsy/bmssp.py`
- `sssp-modern/tests/test_dmmsy_bmssp.py`
- `docs/version-0.3.6-docs.md`

It also updates:

- `sssp-modern/src/sssp/dmmsy/__init__.py`
- `README.md`
- `CHANGELOG.md`

## Why It Matters

The modern directed-sparse SSSP algorithm is not a single sweep. It alternates a bounded pivot-selection step with a recursive bounded multi-source shortest-path call, using a block-list frontier so the recursion can stop at a partial boundary whenever the workload budget is reached.

This release implements that recursive layer directly:

- a singleton-source base case runs a bounded mini-Dijkstra and stops once `k + 1` vertices have been completed,
- the recursive routine seeds a block list from the pivots returned by the existing pivot-selection helper,
- each recursion pull triggers a child call on a smaller level with a tighter bound,
- relaxations above the child boundary are inserted back into the block list, while relaxations between the child boundary and the current pull bound are batch-prepended for the next iteration,
- vertices visited during pivot selection but still below the final boundary are folded into the completed set before returning.

That gives the next implementation stage a small, tested recursion API to plug into a top-level driver that handles initial labeling, level/parameter selection, and overall result projection.

## API Summary

`bmssp(graph, level, bound, sources, distances, k, t)` returns a `BMSSPResult`.

Inputs:

- `graph`: the directed graph to inspect.
- `level`: the non-negative recursion level (`0` falls back to the base case).
- `bound`: the upper distance bound for this recursive call.
- `sources`: the current source vertices for this call.
- `distances`: a mutable distance-label map shared across the recursion.
- `k`: the bounded relaxation and pivot-size parameter.
- `t`: the level-scaling parameter that drives block size and workload budget.

`base_case(graph, bound, sources, distances, k)` is the singleton-source base case used at level `0`. It runs a bounded binary-heap mini-Dijkstra that stops as soon as `k + 1` vertices have been completed.

Result fields:

- `bound`: the final boundary returned by this call (may equal the input bound or a tighter partial bound).
- `vertices`: the vertices completed below the returned boundary, in completion order.
- `iterations`: the number of recursive pulls processed (`base_case` reports settled-vertex count instead).
- `partial`: whether the call returned a partial boundary instead of the full input bound.

Compatibility helpers:

- `BMSSP(...)` and `BaseCase(...)` mirror the paper-style names while calling the same implementations.

## Validation Summary

Focused recursive bounded shortest-path tests:

```powershell
cd sssp-modern
$env:PYTHONPATH='src'
python -m pytest tests/test_dmmsy_bmssp.py
```

Result:

```text
6 passed
```

Nearby modern-SSSP regression coverage:

```powershell
python -m pytest tests/test_dmmsy_transform.py tests/test_dmmsy_blocklist.py tests/test_dmmsy_find_pivots.py tests/test_dmmsy_bmssp.py tests/test_no_third_party_imports.py
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
113 passed
```

Focused coverage:

```powershell
python -m coverage run --include='src/sssp/dmmsy/bmssp.py' -m pytest tests/test_dmmsy_bmssp.py
python -m coverage report --include='src/sssp/dmmsy/bmssp.py'
```

Recorded focused coverage:

- `src/sssp/dmmsy/bmssp.py`: 94%

Syntax/import and diff hygiene:

```powershell
python -m compileall src tests
git diff --check
```

Both checks passed for the release scope.

## Pitfalls

- Do not treat this as the completed modern shortest-path implementation; the public top-level driver and benchmark harness are still pending.
- Do not replace the bounded recursion with a plain Dijkstra sweep. The structure is intentionally shaped around the published bounded multi-source recursion and its partial-boundary semantics.
- Do not assume the returned `vertices` set is the full shortest-path result for the input source set. It is the set of vertices completed below the returned boundary, which may be tighter than the input bound when the workload budget triggers an early return.
- Do not use `<=`, `>`, `>=`, subtraction, or numeric conversion on `Weight` values when extending this module. The implementation expresses non-strict comparisons through `<` plus `==`.

## Next Steps

1. Add the top-level directed-sparse SSSP driver that handles initial labeling, level and parameter selection, and final distance projection.
2. Add driver coverage against the Dijkstra baseline on randomized non-negative graphs.
3. Keep the transform, block-list, pivot-selection, and recursive bounded shortest-path tests in the regression suite as the driver comes together.
4. Add benchmark and report material only after the complete modern implementation is correctness-checked.
