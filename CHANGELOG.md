# Changelog

Status: Dijkstra, Bellman-Ford, A*, and Thorup reference implementations in place; the modern directed-sparse SSSP reference implementation now provides a top-level public driver; reusable benchmark timing support is available; benchmark datasets, CSV/chart output, and report/deck content pending.

## v0.4.1

### Added or Changed

- Added `sssp-modern/src/bench/runner.py` with a reusable benchmark timing harness built around immutable configuration, workload, algorithm, and result records.
- Added `sssp-modern/src/bench/__init__.py` to expose `BenchmarkConfig`, `BenchmarkCase`, `AlgorithmSpec`, `BenchmarkResult`, and `run_benchmark` from the benchmark package.
- Added focused tests in `sssp-modern/tests/test_bench_runner.py` for fixed-seed reproducibility under an injected clock, warmup exclusion, setup outside the timed interval, median/IQR reporting, and protocol input validation.
- Updated `README.md` version, status sentence, quick-start validation commands, repository layout, and roadmap for the benchmark timing harness release.
- Added `docs/version-0.4.1-docs.md` with a detailed walkthrough of the harness API, timing methodology, validation evidence, and remaining benchmark-output work.

### For Deletion

- Local validation byproducts generated during test and compile runs are intentionally uncommitted and can be cleaned manually when convenient.

## v0.4.0

### Added or Changed

- Added the top-level public driver `dmmsy_sssp(graph, source)` in `sssp-modern/src/sssp/dmmsy/__init__.py`, wiring the recursive bounded multi-source shortest-path routine with paper-faithful parameters derived from graph order and an internal positive-infinity sentinel that preserves the strict comparison-addition behavior of the `Weight` wrapper.
- Added pure parameter helpers `dmmsy_parameters(n)` and `dmmsy_top_level(n, t)` that expose the `k`, `t`, and top-level recursion-depth choices used by the driver for tests, the benchmark harness, and the eventual report.
- Exported `dmmsy_sssp`, `dmmsy_parameters`, `dmmsy_top_level`, and `Distances` from the `sssp.dmmsy` package, while keeping the constant-degree transform, block-list, bounded pivot-selection, and recursive bounded shortest-path names available.
- Added `sssp-modern/src/sssp/dmmsy/README.md` summarizing the public API surface and pointing readers at validation entry points.
- Added focused tests for end-to-end agreement with the Dijkstra baseline on path and branching graphs, isolated-source behavior, single-vertex graphs, strict `Weight` compatibility, parameter-formula spot checks, top-level recursion-depth clamping, input validation, parameter overrides, oracle agreement on seeded real-weighted and integer-weighted random graphs, and a performance sanity check at one thousand vertices that asserts oracle agreement and a generous absolute wall-clock budget.
- Updated `README.md` version, status sentence, repository layout, quick-start coverage commands, and roadmap for the new top-level driver release.
- Added `docs/version-0.4.0-docs.md` with a detailed walkthrough of the driver, parameter helpers, validation evidence, and remaining benchmark-harness work.

### For Deletion

- Local validation byproducts generated during test, compile, and coverage runs are intentionally uncommitted and can be cleaned manually when convenient.

## v0.3.6

### Added or Changed

- Added `sssp-modern/src/sssp/dmmsy/bmssp.py` with a recursive bounded multi-source shortest-path routine and its singleton-source base case for the modern directed-sparse SSSP implementation.
- Exported `bmssp`, `BMSSP`, `base_case`, `BaseCase`, and `BMSSPResult` from the `sssp.dmmsy` package for later top-level driver integration.
- Added focused tests for base-case success and partial-boundary behavior, single-level agreement with the Dijkstra baseline below the active bound, multi-level recursion, strict `Weight` compatibility, input validation, and the paper-named wrappers.
- Updated `README.md` version, status sentence, quick-start coverage command, repository layout, and roadmap for the new recursive bounded shortest-path support.
- Added `docs/version-0.3.6-docs.md` with a detailed walkthrough of the recursive bounded shortest-path routine and validation evidence.

### For Deletion

- Local validation byproducts generated during test, compile, and coverage runs are intentionally uncommitted and can be cleaned manually when convenient.

## v0.3.5

### Added or Changed

- Added `sssp-modern/src/sssp/dmmsy/find_pivots.py` with bounded pivot selection for the modern directed-sparse SSSP implementation.
- Exported `find_pivots`, `FindPivots`, and `FindPivotsResult` from the `sssp.dmmsy` package for later recursive shortest-path integration.
- Added focused tests for bounded relaxation layers, early source-pivot return, pivot promotion, bound handling, existing shorter labels, strict `Weight` compatibility, input validation, and the paper-named wrapper.
- Updated `README.md` version, quick-start coverage command, repository layout, and roadmap for the new pivot-selection support.
- Added `docs/version-0.3.5-docs.md` with a detailed walkthrough of the pivot-selection helper and validation evidence.

### For Deletion

- Local validation byproducts generated during test, compile, and coverage runs are intentionally uncommitted and can be cleaned manually when convenient.

## v0.3.4

### Added or Changed

- Added `sssp-modern/src/sssp/dmmsy/blocklist.py` with the block-list frontier partitioning data structure used by the modern directed-sparse SSSP implementation.
- Exported `BlockList`, `BlockListSnapshot`, and `PullResult` from the `sssp.dmmsy` package for later shortest-path integration.
- Added focused tests for duplicate-key handling, batch-prepend ordering rules, pull bounds, deterministic fuzz behavior against a sorted reference map, block-size invariants, and compatibility with the strict `Weight` wrapper.
- Updated `README.md` version, quick-start coverage command, repository layout, and roadmap for the new block-list support.
- Added `docs/version-0.3.4-docs.md` with a detailed walkthrough of the data structure and validation evidence.

### For Deletion

- Local validation byproducts generated during test, compile, and coverage runs are intentionally uncommitted and can be cleaned manually when convenient.

## v0.3.3

### Added or Changed

- Added `sssp-modern/src/sssp/dmmsy/` as the package area for the 2025 directed-sparse SSSP implementation work.
- Added a constant-degree graph transformation that replaces high-degree vertices with deterministic zero-weight port cycles and preserves original shortest-path distances after projection.
- Added focused tests for distance preservation, transformed in-degree/out-degree bounds, isolated vertices, and import-boundary compliance.
- Updated `README.md` version, status, quick-start coverage command, repository layout, and roadmap for the new graph-transformation support.
- Added `docs/version-0.3.3-docs.md` with a detailed walkthrough of the new transformation support and validation evidence.

### For Deletion

- Local validation byproducts generated during test, compile, and coverage runs are intentionally uncommitted and can be cleaned manually when convenient.

## v0.3.2

### Added or Changed

- Reconciled public release notes and roadmap entries so A* and Thorup are both represented as completed reference implementations rather than pending work.
- Expanded third-party notices to cover visible documentation adaptations and development-only validation tools.
- Rewrote `docs/version-0.3.0-docs.md` so the version detail document accurately describes the combined A* and Thorup release.
- Added `docs/version-0.3.2-docs.md` with a detailed record of the documentation reconciliation.

### For Deletion

- Local validation byproducts generated during test and coverage runs are intentionally uncommitted and can be cleaned manually when convenient.

## v0.3.1

### Added or Changed

- Completed Bellman-Ford release validation with golden shortest-path behavior, curated negative-cycle coverage, import-boundary coverage, Dijkstra regression coverage, and targeted line-coverage evidence.
- Updated `sssp-modern/src/sssp/bellman_ford.py` so the module docstring cites the source papers, states reachable negative-cycle semantics, and includes the O(mn) relaxation-loop complexity.
- Updated the public issue record for GitHub issue #4 with completion evidence and closed the issue after validation.
- Updated `README.md` version, status, quick-start coverage command, repository layout, and roadmap for the Bellman-Ford validation release.
- Added `docs/version-0.3.1-docs.md` with a detailed walkthrough of the Bellman-Ford release and validation evidence.

### For Deletion

- Local validation byproducts generated during test and coverage runs are intentionally uncommitted and can be cleaned manually when convenient.

## v0.3.0

### Added or Changed

- Added a pure-stdlib A* reference implementation under `sssp-modern/src/sssp/astar.py`.
- Added reusable zero and Manhattan heuristics under `sssp-modern/src/sssp/heuristics.py`.
- Exported `astar`, `zero`, and `manhattan` from the package root for easier use by examples, tests, and future benchmark code.
- Added focused A* tests for zero-heuristic equivalence with Dijkstra target distances, Manhattan admissibility on a 4-connected unit-cost grid, path reconstruction, unreachable goals, missing-vertex validation, negative-edge rejection, and package exports.
- Added a small grid fixture under `sssp-modern/examples/astar/` for manual inspection and future sample documentation.
- Added `sssp-modern/src/sssp/thorup99.py` as a Thorup-style hierarchical bucket reference implementation for undirected graphs with non-negative integer weights.
- Exported `thorup_sssp` from the package root for public use alongside the existing graph helpers and Dijkstra baseline.
- Converted the tiny undirected golden graph fixture to the public edge-list JSON schema and wired it through the existing fixture loader.
- Added Thorup tests for golden correctness, unreachable vertices, multi-hop paths, missing sources, directed graph rejection, reachable invalid weights, disconnected invalid weights, and optional oracle agreement.
- Clarified the Thorup runtime-model decision note so the Python implementation is framed as a structural reference, not a claim of word-RAM linear-time performance.
- Updated the public issue record for GitHub issue #5 with completion evidence and closed the issue after validation.
- Updated `README.md` version, status, quick-start commands, repository layout, and roadmap for the A* and Thorup implementation release.
- Added `docs/version-0.3.0-docs.md` with a detailed walkthrough of the A* and Thorup release and validation evidence.

### For Deletion

- Local Python cache, coverage, compile, and test-runner outputs generated during validation are intentionally uncommitted and can be cleaned manually when convenient.

## v0.2.2

### Added or Changed

- Added `sssp-modern/docs/issues/issue-feature-w5-s5-1-add-thorup-1999-hierarchical-bucket-sssp.md` as a structured implementation issue artifact for the Thorup reference algorithm.
- Published GitHub issue #5 for the Thorup implementation scope, including acceptance criteria, validation steps, relevant public file context, blocker status, and runtime-model caveat reminders.
- Updated `README.md` version, status, and roadmap to reflect the new Thorup issue-scoping release.
- Added `docs/version-0.2.2-docs.md` with a detailed walkthrough of the Thorup issue artifact and the design context needed before implementation.

### For Deletion

- None from this task context (documentation and issue-tracking only; no build artifacts generated by this update).

## v0.2.1

### Added or Changed

- Added `sssp-modern/docs/issues/issue-feature-w3-s3-1-add-classic-bellman-ford-with-negative-cycle-report.md` as a structured implementation issue artifact for the Bellman-Ford reference algorithm.
- Published GitHub issue #4 for the Bellman-Ford implementation scope, including acceptance criteria, validation steps, relevant public file context, and blocker status.
- Updated `README.md` version, status, repository layout, and roadmap to reflect the new issue-scoping release.
- Added `docs/version-0.2.1-docs.md` with a detailed walkthrough of the Bellman-Ford issue artifact and how it should guide the next implementation pass.

### For Deletion

- None from this task context (documentation and issue-tracking only; no build artifacts generated by this update).

## v0.2.0

### Added or Changed

- Added a pure-stdlib binary-heap Dijkstra reference implementation under `sssp-modern/src/sssp/dijkstra.py`.
- Exported `dijkstra` from the package root for easier use by later examples and benchmarks.
- Added focused Dijkstra tests for golden-fixture correctness, seeded NetworkX oracle agreement, isolated-source behavior, missing-source validation, and negative-edge rejection.
- Added sample Dijkstra source-distance output under `sssp-modern/examples/dijkstra/`.
- Updated `README.md` version, status, quick-start commands, repository layout, and roadmap for the Dijkstra baseline.
- Added `docs/version-0.2.0-docs.md` with a detailed walkthrough of the Dijkstra release.

### For Deletion

- Local validation byproducts generated during test, compile, and coverage runs are intentionally uncommitted and can be cleaned manually when convenient.

## v0.1.3

### Added or Changed

- Added shared pytest fixtures for resolving the nested Python project root, golden fixture directory, and a tiny directed graph fixture.
- Added golden test inputs and expected source-distance data for later algorithm correctness checks.
- Added a test-only optional NetworkX oracle adapter for future shortest-path comparisons without adding runtime package dependencies.
- Added a static import test that confirms runtime source modules use only Python standard-library and local package imports.
- Added harness coverage for golden fixture loading, expected-distance loading, optional oracle skip behavior, and runtime dependency-boundary checks.
- Updated `README.md` status, quick-start test command, repository layout, and roadmap for the test harness baseline.
- Added `docs/version-0.1.3-docs.md` with a detailed walkthrough of the test harness release.

### For Deletion

- Local validation byproducts generated during test and compile runs are intentionally uncommitted and can be cleaned manually when convenient.

## v0.1.2

### Added or Changed

- Added pure-stdlib deterministic graph generators under `sssp-modern/src/sssp/generators.py`.
- Added seeded generator coverage for Erdos-Renyi, random geometric, directed acyclic, Barabasi-Albert, and signed-edge graph families.
- Exported generator helpers from the package root for easier use by later benchmarks and examples.
- Added pytest coverage for fixed-seed reproducibility, local random-state isolation, graph shape invariants, directedness behavior, signed weights, and parameter validation.
- Updated `README.md` status, quick-start test command, repository layout, and roadmap for the generator baseline.
- Added `docs/version-0.1.2-docs.md` with a detailed walkthrough of the generator release.

### For Deletion

- Local Python cache and test-runner outputs generated during validation are intentionally uncommitted and can be cleaned manually when convenient.

## v0.1.1

### Added or Changed

- Added pure-stdlib JSON graph IO helpers under `sssp-modern/src/sssp/io.py`.
- Added edge-list and adjacency-list fixture formats for deterministic graph examples.
- Added sample directed graph fixtures under `sssp-modern/examples/graphs/`.
- Added pytest coverage for graph IO round trips, fixture loading, malformed fixture validation, and `Weight` serialization into fixture output.
- Updated `README.md` status, quick-start test command, repository layout, and roadmap for the graph IO baseline.
- Added `docs/version-0.1.1-docs.md` with a detailed walkthrough of the graph IO and fixture release.

### For Deletion

- Local Python cache and test-runner outputs generated during validation are intentionally uncommitted and can be cleaned manually when convenient.

## v0.1.0

### Added or Changed

- Added pure-stdlib Python package scaffolding under `sssp-modern/src/sssp`.
- Added immutable `Edge` records and a minimal adjacency-list `Graph` type supporting directed and undirected weighted graphs.
- Added a `Weight` value object that permits equality, strict less-than comparison, and addition while rejecting unrelated numeric operations.
- Added focused pytest coverage for graph construction, adjacency behavior, immutable query snapshots, malformed graph inputs, allowed weight operations, forbidden weight operations, and monkeypatch interception of a forbidden operation.
- Updated `README.md` status, quick-start commands, repository layout, and roadmap to reflect the first implementation baseline.
- Added `docs/version-0.1.0-docs.md` with a detailed public walkthrough of the foundation release.

### For Deletion

- Local Python test cache artifacts generated during validation are intentionally uncommitted and can be cleaned manually when convenient.

## v0.0.1

### Added or Changed

- Initialized repository governance documents: `README.md`, `CHANGELOG.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, and `SECURITY.md` with project-specific scope, maintainer contacts, and contributor guidelines.
- Added `LICENSE.txt` declaring the project under the MIT License with copyright retained by the named maintainers.
- Updated `THIRD-PARTY-NOTICES.md` to declare MIT distribution for repository-owned material and to preserve attribution for the third-party MIT-derived reference materials retained in this repository.
- Updated `README.md` license shield and License section to explicitly name the MIT License.
- Added `repo/images/project_screen.png` as the project screenshot referenced from `README.md`.
- Added `docs/version-0.0.1-docs.md` with a detailed walkthrough of the bootstrap release beyond the changelog summary.

### For Deletion

- None from this task context (initialization only; no build artifacts generated by this update).
