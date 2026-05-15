# Version 0.4.0 Documentation

## Quick Diagnostic Read

This release adds the top-level public driver for the 2025 sub-`O(m + n log n)` directed-sparse SSSP reference implementation. It is the first version that exposes the modern algorithm through a single callable entry point with the same shape as the existing Dijkstra baseline, so the benchmark harness and the eventual report can treat all five algorithms uniformly.

You are ready to review this release if you can:

- run the Python tests from the nested `sssp-modern/` project directory,
- read a shortest-path driver as a small wrapper that wires parameters into a published recursive structure,
- compare two algorithms' distance maps for equality and reason about wall-clock cost on small graphs.

## One-Sentence Objective

Add a tested top-level public driver `dmmsy_sssp(graph, source)` that wires the existing recursive bounded multi-source shortest-path routine with paper-faithful parameters derived from graph order, mirrors the existing Dijkstra contract, and stays compatible with the strict comparison-addition wrapper used elsewhere in the modern SSSP reference implementation.

## What Changed

Version `v0.4.0` adds:

- `sssp-modern/src/sssp/dmmsy/README.md`
- `sssp-modern/tests/test_dmmsy.py`
- `docs/version-0.4.0-docs.md`

It also updates:

- `sssp-modern/src/sssp/dmmsy/__init__.py`
- `README.md`
- `CHANGELOG.md`

## Why It Matters

The modern directed-sparse SSSP algorithm is structured as a recursive bounded multi-source shortest-path call with an external choice of three coupled parameters: a relaxation-and-pivot parameter `k`, a level-scaling parameter `t`, and a top-level recursion depth `level`. Earlier versions implemented the constant-degree transformation, the block-list frontier partitioning data structure, the bounded pivot-selection helper, and the recursion itself, but kept all parameter choices on the caller.

This release ties those pieces together with one small driver so callers do not need to know about levels, block sizes, half-open boundary intervals, or sentinel infinities:

- `dmmsy_sssp(graph, source)` is the only public entry point a benchmark or report figure needs.
- `dmmsy_parameters(n)` and `dmmsy_top_level(n, t)` expose the parameter formulas for tests and the future report so the parameter choice is reproducible and auditable.
- An internal positive-infinity sentinel models the paper's unbounded upper bound without breaking the strict comparison-addition behavior used by the project's `Weight` wrapper.

The driver intentionally calls the recursive bounded shortest-path routine on the input graph directly, rather than first applying the constant-degree graph transformation. The transformation remains exported for callers that need it, but the recursion itself works on any directed weighted graph that the existing Dijkstra baseline accepts, which keeps the driver path straightforward and lets the benchmark harness compare algorithms on identical inputs.

## API Summary

`dmmsy_sssp(graph, source, *, zero=0.0, k=None, t=None)` returns a `dict[Vertex, Any]` containing every vertex reachable from `source`, mirroring the existing `dijkstra(graph, source)` contract. Unreachable vertices are absent.

Inputs:

- `graph`: a directed weighted graph as produced by `sssp.graph.Graph` or the existing IO and generator helpers.
- `source`: the starting vertex, which must be a vertex of `graph`.
- `zero`: the source distance label, defaulting to `0.0`. Callers using the strict comparison-addition `Weight` wrapper should pass `zero=Weight(0)` so the entire run remains inside the comparison-addition behavior.
- `k`: an optional override for the relaxation-and-pivot parameter. Defaults to the value returned by `dmmsy_parameters(n)`.
- `t`: an optional override for the level-scaling parameter. Defaults to the value returned by `dmmsy_parameters(n)`.

`dmmsy_parameters(n)` returns the paper-faithful tuple `(k, t)` derived from graph order. The implementation uses base-2 logarithms to align with the binary-heap framing used elsewhere in the repository and clamps each value to be at least one so the recursion preconditions hold on tiny graphs.

`dmmsy_top_level(n, t)` returns the non-negative top-level recursion depth `ceil(log2(n) / t)` derived from graph order and the level-scaling parameter.

Previously exported names remain available, including the constant-degree graph transformation, the block-list frontier partitioning data structure, the bounded pivot-selection helper, and the recursive bounded shortest-path routine with both lowercase and paper-style spellings.

## Validation Summary

Focused driver tests:

```powershell
cd sssp-modern
$env:PYTHONPATH='src'
python -m pytest tests/test_dmmsy.py
```

Result:

```text
16 passed
```

Nearby modern-SSSP regression coverage:

```powershell
python -m pytest tests/test_dmmsy_transform.py tests/test_dmmsy_blocklist.py tests/test_dmmsy_find_pivots.py tests/test_dmmsy_bmssp.py tests/test_dmmsy.py tests/test_no_third_party_imports.py
```

Result:

```text
39 passed
```

Full nested test suite:

```powershell
python -m pytest tests
```

Result:

```text
129 passed
```

Focused coverage:

```powershell
python -m coverage run --include='src/sssp/dmmsy/__init__.py' -m pytest tests/test_dmmsy.py
python -m coverage report --include='src/sssp/dmmsy/__init__.py'
```

Recorded focused coverage:

- `src/sssp/dmmsy/__init__.py`: 93%

Syntax/import and diff hygiene:

```powershell
python -m compileall src tests
git diff --check
```

Both checks passed for the release scope.

The performance sanity test builds a seeded directed random graph at one thousand vertices, runs both Dijkstra and the modern driver, asserts that the two distance maps match on every reachable vertex, and asserts a generous absolute wall-clock budget on the modern driver. The strict ratio comparison between the two algorithms across multiple sizes and densities is intentionally deferred to the benchmark harness release.

## Pitfalls

- Do not treat this as the completed modern shortest-path implementation against all stated portfolio targets. The strict performance ratio comparison and the multi-size benchmark sweep are owned by the next release.
- Do not pass the internal positive-infinity sentinel into your own code. It is intentionally private and lives only for the duration of one driver call. The returned distance map is always populated with real labels of the caller's chosen type.
- Do not assume the driver applies the constant-degree graph transformation. It does not. The transformation remains exported and validated as a separate helper for callers that explicitly want it.
- Do not use `<=`, `>`, `>=`, subtraction, or numeric conversion on `Weight` values when extending this module. The implementation expresses non-strict comparisons through `<` plus `==`, mirroring the rest of the modern SSSP reference implementation.

## Next Steps

1. Add the benchmark harness that times the five reference implementations across multiple graph sizes and densities, records a results CSV plus at least one chart, and verifies the modern driver against the stated performance target with the proper benchmark methodology.
2. Reuse the existing Dijkstra baseline as the oracle for the benchmark harness so the modern driver is always cross-checked for correctness on every comparison run.
3. Keep the constant-degree transform, block-list, pivot-selection, recursive bounded shortest-path, and top-level driver tests in the regression suite as the benchmark and report work comes together.
4. Add the comparative complexity analysis material, the report sections, and the presentation slides only after the benchmark harness produces reproducible measurements.
