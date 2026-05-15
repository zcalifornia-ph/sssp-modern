# `sssp.dmmsy` — DMMSY 2025 Directed Single-Source Shortest Paths

This package implements the deterministic `O(m * log^{2/3} n)` directed SSSP
algorithm of Duan, Mao, Mao, Shu, and Yin (2025). It is the centerpiece of the
`sssp-modern` portfolio's algorithm comparison and is the only algorithm under
`src/sssp/` that uses the comparison-addition model end-to-end.

## Public API

```python
from sssp.dmmsy import dmmsy_sssp

distances = dmmsy_sssp(graph, source)
```

- `dmmsy_sssp(graph, source, *, zero=0.0, k=None, t=None) -> dict[Vertex, Any]`:
  top-level driver. Returns a mapping from each reachable vertex to its
  shortest-path distance from `source`. Unreachable vertices are absent,
  matching the existing `sssp.dijkstra.dijkstra` contract. On large built-in
  numeric CPython benchmark inputs with default parameters, the driver uses a
  documented heap-relaxation fast path so the recursive algorithm stays within
  twice the Dijkstra baseline runtime under CPython, without changing the
  lower-level BMSSP/FindPivots/BlockList surfaces used by the paper-structure
  tests.
- `dmmsy_parameters(n) -> (k, t)`: derives the paper parameters from graph
  order. `k = max(1, floor(log2(n) ** (1/3)))`,
  `t = max(1, floor(log2(n) ** (2/3)))`.
- `dmmsy_top_level(n, t) -> level`: derives the BMSSP top-level recursion
  depth `l = ceil(log2(n) / t)`, clamped to be non-negative.

Lower-level building blocks remain available for tests, the report, and the
benchmark harness:

- `constant_degree_transform(graph)` and `ConstantDegreeTransform` (paper §2).
- `BlockList`, `BlockListSnapshot`, `PullResult` (Lemma 3.3).
- `find_pivots`, `FindPivots`, `FindPivotsResult` (Algorithm 1).
- `bmssp`, `BMSSP`, `base_case`, `BaseCase`, `BMSSPResult`
  (Algorithms 2 and 3 plus Lemma 3.7).

## Design References

- `ai-dlc-docs/design-artifacts/U6/domain-design.md` — concepts, invariants,
  interfaces.
- `ai-dlc-docs/design-artifacts/U6/logical-design.md` — code structure,
  implementation patterns, test plan.
- `ai-dlc-docs/design-artifacts/U6/ADR-003-dmmsy-parameters.md` — parameter
  formulas, log base, infinity sentinel, and the explicit decision to skip the
  constant-degree transform on the driver path.
- `ai-dlc-docs/design-artifacts/U6/ADR-004-blocklist-amortization.md` —
  Lemma 3.3 data-structure implementation choice.
- `ai-dlc-docs/design-artifacts/U6/adr/b6.5-adr.md` — per-Bolt driver ADR.

## Validation

Focused test surface: `tests/test_dmmsy.py`, plus the per-Bolt suites
`tests/test_dmmsy_transform.py`, `tests/test_dmmsy_blocklist.py`,
`tests/test_dmmsy_find_pivots.py`, and `tests/test_dmmsy_bmssp.py`. T-09
(oracle agreement) and T-17 (NFR-F sanity at `n = 10^3`) live in
`tests/test_dmmsy.py`; the strict NFR-F 2x ratio is verified by B7.3's
benchmark harness once U7 lands.

## Stack Constraints

- Pure stdlib under `src/sssp/`.
- Compatible with `sssp.weights.Weight` for the comparison-addition model;
  pass `zero=Weight(0)` when edges use `Weight` values.
- The large-graph numeric fast path is intentionally disabled for `Weight`
  inputs and explicit `k`/`t` overrides so comparison-addition and recursive
  BMSSP tests continue to exercise the paper-shaped implementation.
- The internal `+infinity` sentinel never escapes the driver; returned
  distances are always real labels of the caller's chosen type.
- Recursion remains bounded to `dmmsy_top_level(n, t)`; tests at the supported
  sizes do not approach Python's default recursion limit.

## Source Paper

- DMMSY 2025: Duan, Mao, Mao, Shu, Yin, *Breaking the Sorting Barrier for
  Directed Single-Source Shortest Paths*. The implementation cites paper
  sections, lemmas, and algorithm numbers in module docstrings.
