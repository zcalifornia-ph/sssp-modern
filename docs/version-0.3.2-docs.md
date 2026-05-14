# Version 0.3.2 Documentation

## Quick Diagnostic Read

This release reconciles the public documentation after the A*, Thorup, and Bellman-Ford implementation work. It does not change runtime code. The goal is to make the README, changelog, version notes, and third-party notices describe the same current repository state.

You are ready to review this release if you can:

- distinguish completed reference implementations from future benchmark and report work,
- follow the difference between A* path output, Dijkstra/Bellman-Ford distance output, and Thorup's undirected integer-weight distance-map scope,
- run the Python tests from the nested `sssp-modern/` project directory.

## One-Sentence Objective

Bring the public documentation set back into agreement with the current implementation status while keeping release notes, roadmap entries, and notices public-safe and actionable.

## What Changed

Version `v0.3.2` updates:

- `README.md`
- `CHANGELOG.md`
- `THIRD-PARTY-NOTICES.md`
- `docs/version-0.3.0-docs.md`
- `docs/version-0.3.2-docs.md`

The runtime source and tests are unchanged by this release.

## Why It Matters

The repository already contains Dijkstra, Bellman-Ford, A*, and Thorup reference implementations. Some public documentation still described A* as future work or split the A* and Thorup version details inconsistently. That made the roadmap harder to trust and obscured what readers can already run.

This release fixes that drift by making the public docs agree on three points:

- A* and Thorup are completed reference implementations in the `v0.3.0` release line.
- Bellman-Ford validation remains the `v0.3.1` release line.
- The next implementation milestone is the modern directed-sparse SSSP result, followed by benchmarks, comparative analysis, and report/presentation packaging.

## Documentation Map

`README.md` now marks `v0.3.2` as the current public documentation version, lists A* and Thorup as implemented algorithms, and moves benchmark/report work into later roadmap entries.

`CHANGELOG.md` now has a dedicated `v0.3.2` entry for the documentation reconciliation and a corrected `v0.3.0` entry that treats A* and Thorup as one completed release instead of mixing completed work into cleanup notes.

`THIRD-PARTY-NOTICES.md` now records visible documentation adaptations and clarifies that runtime source is intended to remain standard-library/local-module only while tests may use development tools such as pytest, coverage.py, and optional NetworkX oracle checks.

`docs/version-0.3.0-docs.md` now describes the combined A* and Thorup release coherently, including API summaries, validation themes, and pitfalls.

## Validation Summary

The documentation reconciliation was checked with:

```powershell
git diff --check
```

```powershell
cd sssp-modern
$env:PYTHONPATH='src'
python -m pytest tests
```

Result:

```text
91 passed
```

Focused algorithm coverage was also measured for the currently completed reference implementations:

```powershell
python -m coverage run --include='src/sssp/bellman_ford.py,src/sssp/astar.py,src/sssp/heuristics.py,src/sssp/thorup99.py' -m pytest tests/test_bellman_ford.py tests/test_astar.py tests/test_thorup99.py
python -m coverage report -m src/sssp/bellman_ford.py src/sssp/astar.py src/sssp/heuristics.py src/sssp/thorup99.py
```

Recorded focused coverage:

- `src/sssp/astar.py`: 100%
- `src/sssp/bellman_ford.py`: 100%
- `src/sssp/heuristics.py`: 100%
- `src/sssp/thorup99.py`: 99%

## Pitfalls

- Do not read this release as a runtime feature release; it is documentation-only.
- Do not move the 2025 directed-sparse SSSP implementation into the completed roadmap until the implementation, tests, and documentation land.
- Do not describe the Python Thorup reference as achieving the original word-RAM linear-time bound.

## Next Steps

1. Implement the modern directed-sparse SSSP reference module.
2. Build the benchmark harness after the remaining algorithm work lands.
3. Complete comparative analysis, report material, and presentation packaging from the validated implementations.
