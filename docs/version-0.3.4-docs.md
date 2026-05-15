# Version 0.3.4 Documentation

## Quick Diagnostic Read

This release adds the block-list frontier partitioning data structure needed by the modern directed-sparse shortest-path implementation. The full shortest-path algorithm is still future work.

You are ready to review this release if you can:

- run the Python tests from the nested `sssp-modern/` project directory,
- understand key/value distance labels as tentative frontier entries,
- compare a specialized data structure against a simple sorted dictionary reference.

## One-Sentence Objective

Add a tested block-list data structure that stores tentative shortest-path labels, keeps the smallest live value per key, and pulls bounded-size frontiers for later recursive shortest-path work.

## What Changed

Version `v0.3.4` adds:

- `sssp-modern/src/sssp/dmmsy/blocklist.py`
- `sssp-modern/tests/test_dmmsy_blocklist.py`
- `docs/version-0.3.4-docs.md`

It also updates:

- `sssp-modern/src/sssp/dmmsy/__init__.py`
- `README.md`
- `CHANGELOG.md`

## Why It Matters

The modern directed-sparse SSSP algorithm repeatedly partitions tentative distance labels into bounded-size frontiers. A plain heap can return small labels, but it does not express the two insertion modes used by the algorithm:

- ordinary single-entry insertion into the main block sequence,
- batch-prepending entries that are known to sit before all current labels.

This release implements that contract directly. It gives later shortest-path code a small API for inserting labels, prepending lower batches, and pulling the next frontier without exposing mutable internals.

## API Summary

`BlockList(block_size, upper_bound, max_inserts=None)` stores live key/value labels.

Primary methods:

- `insert(key, value) -> bool`: inserts or improves one key/value pair.
- `batch_prepend(pairs) -> int`: prepends lower-than-current pairs and keeps only improvements.
- `pull() -> PullResult`: removes at most `block_size` smallest labels and returns the next bound.
- `is_empty() -> bool`: reports whether the structure has live entries.
- `snapshot() -> BlockListSnapshot`: returns an immutable test/debug view.

Compatibility helpers:

- `Insert`
- `BatchPrepend`
- `Pull`

These wrappers mirror the names used in the source paper while the lowercase methods keep normal Python style available for implementation code.

## Validation Summary

Focused block-list tests:

```powershell
cd sssp-modern
$env:PYTHONPATH='src'
python -m pytest tests/test_dmmsy_blocklist.py
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
python -m pytest tests/test_dmmsy_transform.py tests/test_dmmsy_blocklist.py tests/test_no_third_party_imports.py
```

Result:

```text
11 passed
```

Full nested test suite:

```powershell
python -m pytest tests
```

Result:

```text
101 passed
```

Focused coverage:

```powershell
python -m coverage run --include='src/sssp/dmmsy/blocklist.py' -m pytest tests/test_dmmsy_blocklist.py
python -m coverage report --include='src/sssp/dmmsy/blocklist.py'
```

Recorded focused coverage:

- `src/sssp/dmmsy/blocklist.py`: 98%

Syntax/import and diff hygiene:

```powershell
python -m compileall src tests
git diff --check
```

Both checks passed for the release scope.

## Pitfalls

- Do not treat this as the completed 2025 shortest-path implementation; it is one support data structure.
- Do not assume the Python list-backed upper-bound index proves the source paper's exact tree-level asymptotics. The code preserves operation semantics and invariants for the study implementation.
- Do not use non-strict comparisons or arithmetic on `Weight` values when extending this module. The tests intentionally exercise strict comparison-addition compatibility.
- Do not bypass `pull()` removal semantics in later recursive code. A pulled frontier is consumed from the live structure.

## Next Steps

1. Add pivot-selection logic and test its reachable-set and size-bound invariants.
2. Add the recursive shortest-path routine that consumes `BlockList`.
3. Add top-level driver coverage against the Dijkstra baseline on randomized non-negative graphs.
4. Keep the block-list fuzz tests in the regression suite as later modules integrate it.
