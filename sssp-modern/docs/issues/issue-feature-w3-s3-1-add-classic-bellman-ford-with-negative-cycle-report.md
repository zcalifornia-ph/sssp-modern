# [FEATURE] [docs/issues] [W3 - S3.1] Add classic Bellman-Ford with negative-cycle report

## Summary

Add a classic Bellman-Ford shortest-path implementation for directed weighted graphs with explicit negative-cycle reporting. The work should expose the planned `bellman_ford(graph, source)` public API, reuse the existing graph primitives, and add validation coverage for ordinary shortest paths plus curated negative-cycle cases. This matters because the package needs a negative-weight-capable baseline before later algorithms and report sections can rely on it.

## Issue Type

Primary type: feature

Assigned labels:

- enhancement - pre-existing
- for experienced devs - created before publication

## Readiness Grade

AGENT_READY. Sanitized planning evidence provides the work coordinate, public API shape, linked story IDs, quality requirements, risk, test ID, and prerequisite status. Public repository files confirm the existing graph model, Dijkstra module pattern, pytest fixture style, optional oracle pattern, and static no-third-party-import check. The main gap is the exact `NegativeCycleReport` shape, but that can be resolved inside this issue by documenting the chosen shape and locking it with tests.

## Source Context

Context type: planning-slice context.

Selected public work coordinate: W3 / S3.1.

Sanitized source brief: implement classic Bellman-Ford, including the O(mn) relaxation loop and negative-cycle detection.

Linked story IDs from sanitized planning evidence: US-01, US-02, US-03.

Linked quality requirements from sanitized planning evidence: quality requirement B, quality requirement D, quality requirement G.

Linked risk from sanitized planning evidence: RR-13, negative-cycle detection can be implemented incorrectly.

Public files read for repository context:

- `src/sssp/dijkstra.py`
- `src/sssp/graph.py`
- `src/sssp/weights.py`
- `src/sssp/__init__.py`
- `tests/test_dijkstra.py`
- `tests/oracles.py`
- `tests/conftest.py`
- `tests/golden/README.md`
- `tests/golden/tiny-directed.edge-list.json`
- `tests/golden/tiny-directed.distances-s.json`
- `tests/test_no_third_party_imports.py`

## Detection Context

Detected in branch: `docs/issues`

GitHub repository: `zcalifornia-ph/sssp-modern`

Local artifact path: `docs/issues/issue-feature-w3-s3-1-add-classic-bellman-ford-with-negative-cycle-report.md`

## Blockers and Dependencies

Sanitized planning evidence identifies W1 as a prerequisite and records its listed slices as complete. No unresolved prerequisite issue or dependency was identified from the loaded evidence.

No GitHub issue dependency was attached because no unresolved same-repository blocker issue was identified.

No blockers remain text-only.

## Scope

In scope:

- Add the planned Bellman-Ford implementation surface at `src/sssp/bellman_ford.py`.
- Expose `bellman_ford(graph, source) -> tuple[Distances, NegativeCycleReport]`.
- Define and document the `NegativeCycleReport` shape and no-cycle state.
- Add tests for golden shortest-path behavior and curated negative-cycle cases.
- Add or extend fixtures only as needed for Bellman-Ford validation.
- Update package exports if the new function is intended to match the existing public package pattern in `src/sssp/__init__.py`.
- Add a module docstring with source-paper references, O(mn) complexity, and negative-cycle semantics.

Out of scope:

- Do not change Dijkstra behavior or its tests except for regression compatibility if needed.
- Do not add benchmark charts or performance-result artifacts.
- Do not implement other shortest-path algorithms.
- Do not modify report, presentation, or submission packaging content as part of this issue.
- Do not use third-party algorithm implementations in production code.

## Current / Observed Behavior

The current package has graph primitives in `src/sssp/graph.py` and a binary-heap Dijkstra implementation in `src/sssp/dijkstra.py`. The Dijkstra module returns a distance map, validates a missing source with `ValueError`, rejects negative edges, and uses local graph neighbors as the traversal boundary.

The package export file `src/sssp/__init__.py` exposes existing public algorithms and graph helpers. There is no public Bellman-Ford implementation loaded from the current public files.

The tests use pytest fixtures from `tests/conftest.py`, golden JSON fixtures under `tests/golden/`, and optional NetworkX oracle checks through `tests/oracles.py`. The static import check in `tests/test_no_third_party_imports.py` requires source modules under `src/sssp` to import only standard-library or local package roots.

## Expected / Target Behavior

The package should provide `bellman_ford(graph, source)` for the existing `Graph` model. It should compute shortest-path distances for reachable vertices when no reachable negative cycle invalidates the result, and it should return an explicit negative-cycle report when a negative cycle is detected. The implementation should follow the classic relaxation-loop algorithm, document complexity and report semantics, and keep production imports limited to the standard library and local package modules.

## Reproduction Steps or Validation Steps

1. From the nested project root, add the Bellman-Ford module and tests without changing unrelated algorithms.
2. Run the Bellman-Ford test target with `PYTHONPATH` pointing at `src`.
3. Confirm the tiny directed golden fixture still produces the expected reachable distances and omits unreachable vertices.
4. Confirm curated negative-cycle fixtures cause the returned report to indicate a detected cycle instead of silently returning ordinary distances.
5. Run the static source-import check and confirm no third-party algorithm import is used by production code.
6. Run the relevant existing Dijkstra tests as regression coverage and confirm they still pass.
7. The pass/fail oracle is that T-06 behavior is covered, public API semantics are documented, and existing graph/Dijkstra behavior remains unchanged.

## Environment and Evidence

- Operating system: not verified by this task.
- Runtime version: not verified by this task.
- Framework versions: not verified by this task.
- Test runner convention: sanitized planning evidence says tests live under `tests/` and run with pytest from the nested project root; existing public tests confirm pytest usage.
- Existing algorithm pattern: `src/sssp/dijkstra.py` uses a small module-level `Distances` alias, validates source membership, documents preconditions, and returns only reachable distances.
- Existing graph model: `src/sssp/graph.py` provides `Graph`, `Edge`, `vertices()`, `neighbors(vertex)`, and `edges()`.
- Existing weight boundary: `src/sssp/weights.py` defines `Weight` with `==`, `<`, and `+` only.
- Existing test style: `tests/test_dijkstra.py`, `tests/conftest.py`, and `tests/golden/README.md` show pytest fixtures, golden JSON fixtures, and optional oracle checks.
- Logs, stack traces, screenshots, and failure output: not provided / not verified.
- Tests run by this task: none. This task is issue authoring only.

## Relevant Files, Symbols, and Tests

- `src/sssp/dijkstra.py` - read; direct pattern for a small algorithm module, source validation, docstring, and distance return shape.
- `src/sssp/graph.py` - read; direct graph interface for vertices, neighbors, and edge iteration.
- `src/sssp/weights.py` - read; relevant value-object boundary for comparison and addition behavior.
- `src/sssp/__init__.py` - read; public package export pattern.
- `tests/test_dijkstra.py` - read; direct pattern for golden fixture tests and optional oracle tests.
- `tests/oracles.py` - read; direct pattern for optional NetworkX oracle use in tests only.
- `tests/conftest.py` - read; direct fixture-loading pattern for golden graph data.
- `tests/golden/README.md` - read; direct fixture directory convention.
- `tests/test_no_third_party_imports.py` - read; direct production-import constraint.

## Agent Handoff Notes

Start with the existing `Graph` API: `vertices()`, `neighbors(vertex)`, and possibly `edges()` are enough to implement the relaxation loop without changing graph storage. Use `src/sssp/dijkstra.py` as the local style reference for module docstring, source validation, and reachable-distance behavior.

Search terms likely to localize the relevant conventions: `Distances`, `source must be a vertex`, `networkx_dijkstra_distances`, `tiny_directed_graph`, and `ALLOWED_IMPORT_ROOTS`.

The negative-cycle report shape is not defined in the public files read. A reasonable implementation hypothesis is to add a small local dataclass with a boolean detection state and optional witness data, then document exactly what callers can rely on. Verify that shape with tests instead of leaving it implicit.

Keep NetworkX and any other third-party shortest-path implementation out of production code. Optional oracle use belongs in tests only, following `tests/oracles.py`.

## Acceptance Criteria

- [ ] `bellman_ford(graph, source)` exists in `src/sssp/bellman_ford.py`.
- [ ] `bellman_ford(graph, source)` returns a two-item tuple containing a distance map and a negative-cycle report.
- [ ] The distance map contains reachable shortest-path distances when no reachable negative cycle is detected.
- [ ] Unreachable vertices are not reported as reachable distances.
- [ ] A missing source raises a clear `ValueError`.
- [ ] A reachable negative cycle is detected by a final relaxation check.
- [ ] Negative-cycle report semantics are documented in code.
- [ ] T-06 covers golden shortest-path behavior.
- [ ] T-06 covers curated negative-cycle cases.
- [ ] A brute-force or independently checked tiny-instance oracle is used for small correctness cases.
- [ ] The Bellman-Ford module docstring cites the source papers and states O(mn) time complexity.
- [ ] The Bellman-Ford public API meets the >=90% line coverage quality target.
- [ ] Production source imports remain standard-library or local package imports only.
- [ ] Existing Dijkstra behavior remains unchanged.

## Test / Verification Plan

Existing tests to run:

- `$env:PYTHONPATH='src'; python -m pytest tests/test_dijkstra.py` - regression check for existing Dijkstra behavior; recommended, not run by this task.
- `$env:PYTHONPATH='src'; python -m pytest tests/test_no_third_party_imports.py` - production-import boundary check; recommended, not run by this task.

New tests likely needed:

- `$env:PYTHONPATH='src'; python -m pytest tests/test_bellman_ford.py` - expected new test target for T-06; recommended after adding the test file.
- Add a golden fixture test that reuses `tiny-directed` or an equivalent small directed graph.
- Add a curated reachable negative-cycle case.
- Add a no-cycle negative-edge case to show Bellman-Ford accepts negative edges when no negative cycle exists.
- Add a missing-source validation case.
- Add a tiny brute-force agreement case when feasible.

Manual checks:

- Import the public function from the package export if `src/sssp/__init__.py` is updated.
- Inspect the returned negative-cycle report in both no-cycle and detected-cycle cases.

Regression checks:

- Re-run Dijkstra tests and golden fixture tests to confirm graph fixture semantics were not changed.
- Re-run compile checks for `src` and `tests`; recommended, not run by this task.

Security checks:

- Confirm no secrets, tokens, or local paths are introduced in fixtures or docstrings.
- Confirm no third-party production algorithm import is introduced.

Performance checks:

- Confirm the documented complexity is O(mn).
- No benchmark target is required for this issue.

## Implementation Boundaries

Do not change the `Graph`, `Edge`, or `Weight` public contracts unless a separate issue explicitly authorizes that change. Preserve the existing Dijkstra behavior and public tests. Keep production code pure standard library plus local package imports. Do not hide negative-cycle detection behind exceptions unless the documented `NegativeCycleReport` contract still returns enough structured information for callers and tests. Do not add broad benchmark, report, presentation, or deployment work to this issue.

## Risks and Review Focus

- Correctness: review the n-1 relaxation loop and final negative-cycle pass against the classic algorithm.
- Regression: run Dijkstra tests to catch accidental changes to shared graph behavior.
- Data compatibility: verify reachable-only distance-map semantics match the existing package convention.
- Test quality: ensure curated negative-cycle fixtures would fail if the final detection pass were removed.
- Maintainability: verify the report object is small, documented, and covered by tests.
- Import hygiene: verify production source remains standard-library/local only.

## Work Mapping

Goal or source brief -> Story IDs -> Work coordinate -> Blocker references -> Acceptance Criteria -> Test IDs -> Release-check IDs -> Monitoring-signal IDs

Classic Bellman-Ford with negative-cycle detection -> US-01, US-02, US-03 -> W3 / S3.1 -> no unresolved blocker issue identified -> acceptance criteria in this issue -> T-06 -> DC-01, DC-03, DC-04 -> OS-01, OS-03

## Open Questions

- Non-blocking, for implementer/reviewer: Should `NegativeCycleReport` include a concrete cycle witness, an affected edge, or only a detected/no-detected state plus documentation?
- Non-blocking, for reviewer: Should the package export `bellman_ford` immediately in `src/sssp/__init__.py`, or should direct module import be accepted until the next public API pass?

## Definition of Done

- [ ] Code change is scoped to the in-scope list.
- [ ] All acceptance criteria are observably met.
- [ ] Tests in the verification plan are added or updated and passing.
- [ ] Documentation, decision notes, or runbooks are updated when the change requires it.
- [ ] Reviewer focus areas from the risk section are addressed.
- [ ] Work-mapping links are populated.
- [ ] Blocker/dependency status is resolved or explicitly carried forward.
- [ ] Issue is closed with a brief evidence summary referencing the verifying tests, commands, or screenshots.
