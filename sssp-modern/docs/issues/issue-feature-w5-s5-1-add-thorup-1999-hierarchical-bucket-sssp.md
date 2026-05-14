# [FEATURE] [docs/issues] [W5 - S5.1] Add Thorup 1999 hierarchical bucket SSSP

## Summary

Add a Thorup-style shortest-path reference implementation for undirected graphs with non-negative integer weights. The work should expose the planned `thorup_sssp(graph, source)` public API, use the existing graph primitives, and document the runtime-model caveat clearly so readers do not mistake a Python reference implementation for the original word-RAM bound. This issue is a scoped implementation handoff, not proof that the algorithm has already been implemented.

## Issue Type

Primary type: feature

Assigned labels:

- enhancement - pre-existing
- for experienced devs - pre-existing
- question - pre-existing

## Readiness Grade

HUMAN_READY_BUT_AGENT_NEEDS_CONTEXT. Sanitized planning evidence provides the work coordinate, public API shape, linked story IDs, quality requirements, risk, test ID, deliverables, and prerequisite status. Public repository files confirm the graph model, undirected reciprocal-arc behavior, seeded undirected generator conventions, Dijkstra distance-map convention, pytest style, optional oracle boundary, and runtime import constraints. A human implementer can act on this, but a coding agent should first load or create the detailed Thorup hierarchy design and runtime-model decision note before writing code.

## Source Context

Context type: planning-slice context.

Selected public work coordinate: W5 / S5.1.

Sanitized source brief: implement Thorup 1999 hierarchical bucket single-source shortest paths for undirected graphs with non-negative integer weights.

Linked story IDs from sanitized planning evidence: US-01, US-02, US-03, US-05.

Linked quality requirements from sanitized planning evidence: quality requirement B, quality requirement D, quality requirement G.

Linked risk from sanitized planning evidence: RR-03, the implementation must not overstate the original runtime model when implemented in Python.

Public files read for repository context:

- `src/sssp/graph.py`
- `src/sssp/dijkstra.py`
- `src/sssp/generators.py`
- `src/sssp/__init__.py`
- `tests/test_graph.py`
- `tests/test_dijkstra.py`
- `tests/test_generators.py`
- `tests/oracles.py`
- `tests/conftest.py`
- `tests/golden/README.md`
- `tests/test_no_third_party_imports.py`

## Detection Context

Detected in branch: `docs/issues`

GitHub repository: `zcalifornia-ph/sssp-modern`

Local artifact path: `docs/issues/issue-feature-w5-s5-1-add-thorup-1999-hierarchical-bucket-sssp.md`

## Blockers and Dependencies

Sanitized planning evidence identifies W1 as a prerequisite and records its listed slices as complete. No unresolved prerequisite issue or dependency was identified from the loaded evidence.

No GitHub issue dependency was attached because no unresolved same-repository blocker issue was identified.

No blockers remain text-only. A source-paper/design pass is still required before coding because the exact hierarchy invariants were not present in the public files loaded for this issue.

## Scope

In scope:

- Add the planned Thorup implementation surface at `src/sssp/thorup99.py`.
- Expose `thorup_sssp(graph, source) -> Distances`.
- Restrict the public contract to undirected graphs with non-negative integer weights.
- Document the hierarchy structure used by the implementation.
- Document the Python runtime-model caveat clearly in code and the required decision note.
- Add correctness tests on an integer-weight undirected golden set.
- Add validation for unsupported input classes, including directed graphs and non-integer or negative weights.
- Update package exports if the new function is intended to match the existing public package pattern in `src/sssp/__init__.py`.

Out of scope:

- Do not claim Python achieves the original word-RAM linear-time bound.
- Do not implement unrelated shortest-path algorithms as part of this issue.
- Do not change Dijkstra behavior or graph storage semantics.
- Do not add benchmark charts or report/presentation sections in this issue.
- Do not use third-party algorithm implementations in production code.

## Current / Observed Behavior

The current package has an adjacency-list `Graph` type in `src/sssp/graph.py`. Directed graphs store one traversable arc per inserted edge, and undirected graphs store reciprocal arcs. `tests/test_graph.py` confirms this undirected reciprocal-arc behavior.

The current package includes Dijkstra in `src/sssp/dijkstra.py`, which returns reachable distance maps and rejects negative edges. This is a useful local style and regression reference, but it is not the Thorup implementation.

The generator module `src/sssp/generators.py` already has undirected graph generation paths, including random geometric and preferential-attachment graphs. `tests/test_generators.py` confirms undirected shape expectations and non-negative generated weights for those paths.

The package export file `src/sssp/__init__.py` exposes current public algorithms and graph helpers. There is no public Thorup implementation loaded from the current public files.

## Expected / Target Behavior

The package should provide `thorup_sssp(graph, source)` for undirected graphs with non-negative integer weights. It should compute reachable shortest-path distances from `source`, reject unsupported graph or weight inputs with clear errors, and document how the Python implementation relates to the original Thorup runtime model. Tests should prove correctness on at least one deterministic integer-weight undirected golden set.

## Reproduction Steps or Validation Steps

1. From the nested project root, add the Thorup module and tests without changing unrelated algorithms.
2. Add or reuse deterministic undirected integer-weight graph fixtures for T-08.
3. Run the Thorup test target with `PYTHONPATH` pointing at `src`.
4. Confirm reachable distances match a trusted expected-distance fixture or test-only oracle on integer-weight undirected graphs.
5. Confirm directed graphs are rejected or explicitly handled according to the documented public contract.
6. Confirm negative, float, and unsupported weight inputs are rejected with clear errors.
7. Run the static source-import check and confirm no third-party algorithm import is used by production code.
8. Run the relevant existing graph and Dijkstra tests as regression coverage.
9. The pass/fail oracle is that T-08 behavior is covered, runtime-model caveat documentation exists, and existing graph/Dijkstra behavior remains unchanged.

## Environment and Evidence

- Operating system: not verified by this task.
- Runtime version: not verified by this task.
- Framework versions: not verified by this task.
- Test runner convention: sanitized planning evidence says tests live under `tests/` and run with pytest from the nested project root; existing public tests confirm pytest usage.
- Existing graph model: `src/sssp/graph.py` provides `Graph`, `Edge`, `vertices()`, `neighbors(vertex)`, `edges()`, `order()`, and `size()`.
- Existing undirected behavior: `tests/test_graph.py` confirms reciprocal arcs for `Graph(directed=False)`.
- Existing generator behavior: `src/sssp/generators.py` and `tests/test_generators.py` show seeded undirected graph generation and shape checks.
- Existing distance-map convention: `src/sssp/dijkstra.py` returns reachable distances only.
- Existing test oracle boundary: `tests/oracles.py` keeps NetworkX optional and test-only.
- Logs, stack traces, screenshots, and failure output: not provided / not verified.
- Tests run by this task: none. This task is issue authoring only.

## Relevant Files, Symbols, and Tests

- `src/sssp/graph.py` - read; direct graph interface and undirected reciprocal-arc storage behavior.
- `src/sssp/dijkstra.py` - read; direct local style reference for source validation and reachable-distance return shape.
- `src/sssp/generators.py` - read; relevant seeded undirected graph-generation conventions.
- `src/sssp/__init__.py` - read; public package export pattern.
- `tests/test_graph.py` - read; direct evidence for undirected graph semantics.
- `tests/test_dijkstra.py` - read; direct test style and distance-map regression pattern.
- `tests/test_generators.py` - read; direct tests for undirected generated graph shape.
- `tests/oracles.py` - read; test-only optional oracle pattern.
- `tests/conftest.py` - read; fixture-loading pattern for golden data.
- `tests/golden/README.md` - read; golden fixture convention.
- `tests/test_no_third_party_imports.py` - read; production-import constraint.

## Agent Handoff Notes

Start with the existing `Graph` API and verify the graph is undirected before running the algorithm. The implementation should not mutate graph storage or change how reciprocal arcs are represented.

Search terms likely to localize the relevant conventions: `Graph(directed=False)`, `is_directed`, `Distances`, `source must be a vertex`, `networkx_dijkstra_distances`, `barabasi_albert_graph`, and `ALLOWED_IMPORT_ROOTS`.

Before coding, load or create the detailed hierarchy design and runtime-model decision note. The issue evidence only identifies the planned public API and required behavior; it does not include the exact Thorup hierarchy invariants.

Keep NetworkX and any other third-party shortest-path implementation out of production code. Optional oracle use belongs in tests only, following `tests/oracles.py`.

## Acceptance Criteria

- [x] `thorup_sssp(graph, source)` exists in `src/sssp/thorup99.py`.
- [x] `thorup_sssp(graph, source)` returns a reachable distance map.
- [x] The public contract accepts undirected graphs with non-negative integer weights.
- [x] Directed graphs are rejected or handled according to documented behavior.
- [x] Negative weights are rejected with a clear error.
- [x] Non-integer weights are rejected with a clear error.
- [x] Missing source vertices raise a clear `ValueError`.
- [x] T-08 covers correctness on an integer-weight undirected golden set.
- [x] Tests include at least one unreachable vertex case.
- [x] Tests include at least one multi-hop path that beats a direct heavier edge.
- [x] A test-only oracle or independently checked fixture validates expected distances.
- [x] The module docstring cites the Thorup 1999 source and states the Python runtime-model caveat.
- [x] The required runtime-model decision note exists or is updated.
- [x] The public API meets the >=90% line coverage quality target.
- [x] Production source imports remain standard-library or local package imports only.
- [x] Existing graph and Dijkstra behavior remains unchanged.

## Test / Verification Plan

Existing tests to run:

- `$env:PYTHONPATH='src'; python -m pytest tests/test_graph.py` - regression check for graph and undirected reciprocal-arc behavior; recommended, not run by this task.
- `$env:PYTHONPATH='src'; python -m pytest tests/test_dijkstra.py` - regression check for existing Dijkstra behavior; recommended, not run by this task.
- `$env:PYTHONPATH='src'; python -m pytest tests/test_generators.py` - regression check for seeded undirected generator behavior; recommended, not run by this task.
- `$env:PYTHONPATH='src'; python -m pytest tests/test_no_third_party_imports.py` - production-import boundary check; recommended, not run by this task.

New tests likely needed:

- `$env:PYTHONPATH='src'; python -m pytest tests/test_thorup99.py` - expected new test target for T-08; recommended after adding the test file.
- Add an integer-weight undirected golden graph fixture and expected-distance fixture.
- Add unsupported-input tests for directed graphs, negative weights, non-integer weights, and missing source vertices.
- Add an unreachable-vertex case.
- Add an oracle-agreement case when the optional test-only oracle is available.

Manual checks:

- Inspect the module docstring for the source-paper reference and runtime-model caveat.
- Inspect the decision note to confirm it does not claim Python achieves the original word-RAM bound.
- Import the public function from the package export if `src/sssp/__init__.py` is updated.

Regression checks:

- Re-run graph, generator, Dijkstra, and import-boundary tests.
- Re-run compile checks for `src` and `tests`; recommended, not run by this task.

Security checks:

- Confirm no secrets, tokens, or local paths are introduced in fixtures or docstrings.
- Confirm no third-party production algorithm import is introduced.

Performance checks:

- Confirm the documented runtime caveat is accurate for Python.
- Do not use benchmark timing as the correctness oracle for this issue.

## Implementation Boundaries

Do not change the `Graph` or `Edge` public contracts unless a separate issue explicitly authorizes that change. Preserve existing Dijkstra behavior and public tests. Keep production code pure standard library plus local package imports. Do not use benchmark speed to justify correctness. Do not overstate runtime guarantees: the implementation may be faithful as a reference while still documenting that Python does not provide the original word-RAM execution model.

## Risks and Review Focus

- Correctness: review hierarchy construction, bucket transitions, and relaxation behavior against the source algorithm.
- Runtime-model honesty: verify docs and comments distinguish the reference implementation from the original theoretical model.
- Regression: run graph and Dijkstra tests to catch accidental shared-behavior changes.
- Data compatibility: verify reachable-only distance-map semantics match the existing package convention.
- Test quality: ensure the golden undirected integer graph would fail under a naive one-hop-only implementation.
- Import hygiene: verify production source remains standard-library/local only.

## Work Mapping

Goal or source brief -> Story IDs -> Work coordinate -> Blocker references -> Acceptance Criteria -> Test IDs -> Release-check IDs -> Monitoring-signal IDs

Thorup 1999 hierarchical bucket SSSP -> US-01, US-02, US-03, US-05 -> W5 / S5.1 -> no unresolved blocker issue identified -> acceptance criteria in this issue -> T-08 -> DC-01, DC-04 -> OS-01, OS-02, OS-03

## Resolution Evidence

Resolved on 2026-05-14 PHT after fixing the failed scrutiny blockers:

- Fixed `tests/conftest.py` to load the undirected golden fixture through the existing `read_edge_list(path)` contract.
- Converted `tests/golden/tiny-undirected.edge-list.json` to the `sssp.edge-list.v1` object schema with `"directed": false`.
- Added upfront full-graph weight validation in `src/sssp/thorup99.py`, including disconnected invalid-weight components.
- Added tests for negative and non-integer edges in unreachable components.
- Reworded `docs/decision-thorup-runtime-model.md` so the simplified bucket design is described as a structural analogue, not a Python word-RAM runtime guarantee.

Validation data:

- `$env:PYTHONPATH='src'; python -m pytest tests/test_thorup99.py` -> 11 passed.
- `$env:PYTHONPATH='src'; python -m pytest tests` -> 70 passed.
- `python -m compileall src tests` -> completed successfully.
- `$env:PYTHONPATH='src'; python -m coverage run --source=sssp.thorup99 -m pytest tests/test_thorup99.py; python -m coverage report --include='src/sssp/thorup99.py'` -> 11 passed, `src/sssp/thorup99.py` 99% line coverage.

## Open Questions

- Resolved: hierarchy invariants and simplifications are documented in `src/sssp/thorup99.py` and `docs/decision-thorup-runtime-model.md`.
- Resolved: `thorup_sssp` rejects all non-`int` weights and rejects `bool`, including invalid weights in unreachable graph components.
- Resolved: `thorup_sssp` is exported from `src/sssp/__init__.py`.

## Definition of Done

- [x] Code change is scoped to the in-scope list.
- [x] All acceptance criteria are observably met.
- [x] Tests in the verification plan are added or updated and passing.
- [x] Documentation, decision notes, or runbooks are updated when the change requires it.
- [x] Reviewer focus areas from the risk section are addressed.
- [x] Work-mapping links are populated.
- [x] Blocker/dependency status is resolved or explicitly carried forward.
- [x] Issue is closed with a brief evidence summary referencing the verifying tests, commands, or screenshots.
