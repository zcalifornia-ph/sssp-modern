# Changelog

Status: Dijkstra, Bellman-Ford, A*, and Thorup reference implementations in place; the modern directed-sparse SSSP reference implementation provides a top-level public driver; reusable benchmark timing, dataset catalog, benchmark result CSV writing, and runtime chart rendering are available with a DMMSY-vs-Dijkstra runtime sanity check; the written report manuscript is complete with experimental evaluation, reflection, role-specific AI assistance disclosure, author contributions, public-facing terminology cleanup, and a rebuilt PDF; the presentation deck now has a clean-compiling title/outline spine, baseline-algorithm slides, modern-algorithm centerpiece, benchmark-results slides, a result-evidence slide in the main talk flow with a repository citation, reflection/integrity framing, author contributions, final copy-fit/layout polish, and public-facing terminology cleanup, with dry-run pacing and reproducible submission packaging still pending.

## v0.5.8

### Added or Changed

- Promoted the result-evidence material in `sssp-modern/presentation/main.tex` from a backup-only Q&A frame into the main presentation flow before the reflection and author-contribution slides.
- Added the public GitHub repository URL to the evidence slide so the deck names the project source alongside the benchmark CSV, runtime figure, test-suite result, and report anchors.
- Simplified the closing sequence by removing the standalone "Honor. Excellence. Service." standout slide and the older backup evidence frame, leaving the deck focused on evidence, reflection, contributions, references, and questions.
- Updated `sssp-modern/presentation/main.pdf` (25 pages, 1250772 bytes) from the revised Beamer source.
- Verified the presentation build with `latexmk -pdf -interaction=nonstopmode main.tex`: exit code 0, with `main.pdf` reported up to date.
- Updated `README.md` version, status sentence, quick-start presentation build note, repository layout, and roadmap for this release.
- Added `docs/version-0.5.8-docs.md` with a detailed walkthrough of the presentation evidence-flow polish and validation evidence.

### For Deletion

- None from this task context.

## v0.5.7

### Added or Changed

- Updated the AI Assistance Disclosure in `sssp-modern/report/report.tex` to distinguish the roles of the two assistant families used in the project: Claude for planning support and OpenAI Codex GPT 5.5 for programming and implementation assistance.
- Reflowed the AI Assistance Disclosure and Author Contributions sections into shorter LaTeX paragraphs for readability while preserving their academic-integrity and contribution content.
- Kept the academic-integrity framing intact: algorithmic content remains attributed to the cited source papers, and final responsibility remains with the two human co-authors.
- Rebuilt `sssp-modern/report/report.pdf` (24 pages, 403173 bytes) from the updated LaTeX source.
- Verified the report build with `pdflatex -interaction=nonstopmode -halt-on-error report.tex`: exit code 0, with no LaTeX errors. Remaining diagnostics are the same non-blocking report-layout warnings noted in the prior report release.
- Updated `README.md` version, status sentence, and roadmap for this release.
- Added `docs/version-0.5.7-docs.md` with a detailed walkthrough of the disclosure clarification and validation evidence.

### For Deletion

- None from this task context.

## v0.5.6

### Added or Changed

- Cleaned `sssp-modern/report/report.tex` so report comments, implementation notes, runtime caveats, test references, AI-use disclosure, author contributions, and result-table notes use plain public-facing wording instead of private planning shorthand or coded validation labels.
- Replaced internal note references with reader-facing descriptions such as implementation notes, guard tests, benchmarking protocol, runtime caveat, performance sanity check, and maximum observed ratio.
- Improved the report's LaTeX layout by adding wrapped title metadata, section page breaks, tighter table sizing, and a bibliography-heading patch that keeps the PDF structure consistent with the manuscript style.
- Rebuilt `sssp-modern/report/report.pdf` (24 pages, 403036 bytes) from the cleaned LaTeX source.
- Verified the report source with targeted terminology and coded-label scans; no matches remained in `sssp-modern/report/report.tex`.
- Verified the report build with `pdflatex -interaction=nonstopmode -halt-on-error report.tex`: exit code 0, with no LaTeX errors. Remaining diagnostics are limited to underfull boxes, empty-link warnings from existing section anchors, and one font-substitution warning in a code-heavy contribution paragraph.
- Updated `README.md` version, status sentence, report build note, repository layout, and roadmap for this release.
- Added `docs/version-0.5.6-docs.md` with a detailed walkthrough of the report cleanup, validation evidence, and remaining dry-run/submission work.

### For Deletion

- None from this task context.

## v0.5.5

### Added or Changed

- Cleaned `sssp-modern/presentation/main.tex` so speaker notes, slide caveats, contribution wording, and Q&A evidence labels use plain public-facing presentation language instead of private planning shorthand or internal review labels.
- Replaced design references, coded validation labels, and numbered contribution wording with audience-readable descriptions such as project notes, runtime sanity check, written rationale, completed contributions, and files to cite during Q&A.
- Rebuilt `sssp-modern/presentation/main.pdf` (26 pages, 1252006 bytes) from the cleaned Beamer source.
- Verified the presentation source with a targeted terminology scan for the removed private shorthand and internal labels; no matches remained in `sssp-modern/presentation/main.tex`.
- Verified the presentation build with `latexmk -pdf -interaction=nonstopmode main.tex`: exit code 0, no LaTeX errors, no undefined citations, no undefined references, no overfull hboxes/vboxes, no LaTeX warnings, and no hyperref/pdfTeX warnings.
- Updated `README.md` version, status sentence, quick-start presentation build note, repository layout, and roadmap for this release.
- Added `docs/version-0.5.5-docs.md` with a detailed walkthrough of the presentation terminology cleanup, validation evidence, and remaining dry-run/submission work.

### For Deletion

- None from this task context.

## v0.5.4

### Added or Changed

- Polished `sssp-modern/presentation/main.tex` for final deck readability: wrapped the title metadata more cleanly, simplified the venue line, normalized block-heading casing, and added deliberate line breaks in dense implementation notes.
- Reworked the modern-algorithm architecture diagram's bounded-pulls return path into a dashed labeled loop so the annotation no longer collides with the surrounding nodes.
- Tightened the parameter/bound, reflection, contribution, and closing frames with cleaner line breaks, better slide fit, and clearer public contact links.
- Rebuilt `sssp-modern/presentation/main.pdf` (26 pages, 1252178 bytes) from the polished Beamer source.
- Verified the presentation build with `latexmk -pdf -interaction=nonstopmode main.tex`: exit code 0, no LaTeX errors, no undefined citations, no undefined references, no overfull hboxes/vboxes, no LaTeX warnings, and no hyperref/pdfTeX warnings. Remaining underfull hbox diagnostics are limited to compact code-heavy slide paragraphs.
- Updated `README.md` version, status sentence, quick-start presentation build note, repository layout, and roadmap for this release.
- Added `docs/version-0.5.4-docs.md` with a detailed walkthrough of the presentation copy-fit/layout pass, validation evidence, and remaining dry-run/submission work.

### For Deletion

- None from this task context.

## v0.5.3

### Added or Changed

- Replaced the remaining presentation placeholders in `sssp-modern/presentation/main.tex` with authored benchmark-results and closing content: a benchmark-protocol slide, an embedded runtime chart, a Dijkstra-normalized result-ratio table, a reflection/integrity slide, an Author Contributions slide, and a Q&A backup evidence slide.
- Added result interpretation that preserves the documented CPython caveats for Thorup and the modern directed-sparse implementation while still reporting the committed benchmark sanity result.
- Added an Author Contributions slide that attributes California's repository, baseline, modern-algorithm, benchmark, report, and deck work alongside Rizal's Bellman-Ford and Thorup contributions and the presentation handoff.
- Rebuilt `sssp-modern/presentation/main.pdf` (26 pages, 1252512 bytes) from the updated Beamer source.
- Verified the presentation build with `latexmk -pdf -interaction=nonstopmode main.tex`: exit code 0, zero LaTeX errors, zero undefined citations, zero undefined references, zero overfull hboxes/vboxes, zero LaTeX warnings, zero hyperref/pdfTeX warnings, the runtime chart rendered from the committed benchmark figure, and an idempotent rerun reporting all targets up to date.
- Updated `README.md` version, status sentence, quick-start presentation build note, repository layout, and roadmap for this release.
- Added `docs/version-0.5.3-docs.md` with a detailed walkthrough of the presentation results/contributions pass, validation evidence, and remaining dry-run/submission work.

### For Deletion

- None from this task context.

## v0.5.2

### Added or Changed

- Replaced the DMMSY placeholder in `sssp-modern/presentation/main.tex` with four authored centerpiece frames covering why the 2025 result matters, how the constant-degree transform, FindPivots, BMSSP recursion, and block-list frontier cooperate, how BMSSP is presented to the audience, and how the parameter/bound/caveat story should be explained.
- Added a compact TikZ architecture diagram to the presentation source without introducing new external image dependencies or changing the checked-in UP Beamer theme files.
- Rebuilt `sssp-modern/presentation/main.pdf` (23 pages, 1226418 bytes) from the updated Beamer source.
- Verified the presentation build with `latexmk -pdf -interaction=nonstopmode main.tex`: exit code 0, zero LaTeX errors, zero undefined citations, zero undefined references, zero overfull hboxes, zero overfull vboxes, zero LaTeX warnings, `duan2025breaking` resolved, and an idempotent rerun reporting all targets up to date.
- Updated `README.md` version, status sentence, quick-start presentation build note, repository layout, and roadmap for this release.
- Added `docs/version-0.5.2-docs.md` with a detailed walkthrough of the presentation centerpiece, validation evidence, and remaining deck/submission work.

### For Deletion

- Local LaTeX intermediate files generated by the deck build are intentionally uncommitted and can be cleaned manually when convenient.

## v0.5.1

### Added or Changed

- Replaced the presentation template showcase in `sssp-modern/presentation/main.tex` with the SSSP study deck scaffold: two-author title metadata, outline, problem definition, historical algorithm arc, four baseline-algorithm slides for Dijkstra, Bellman-Ford, A*, and Thorup, placeholder sections for the remaining modern-algorithm and results/contributions content, references, and closing frame.
- Added speaker-note comments in the Beamer source to preserve the planned California/Rizal speaking split for the opening, baseline algorithms, results, and Q&A handoff.
- Appended the six SSSP source-paper bibliography entries to `sssp-modern/presentation/references.bib` so the deck cites Dijkstra, Bellman, Ford, Hart-Nilsson-Raphael, Thorup, and Duan-Mao-Mao-Shu-Yin directly.
- Rebuilt `sssp-modern/presentation/main.pdf` (20 pages, 1138392 bytes) from the updated Beamer source.
- Verified the presentation build with `latexmk -pdf -interaction=nonstopmode main.tex`: exit code 0, zero LaTeX errors, zero undefined citations, zero undefined references, zero overfull hboxes, zero LaTeX warnings, and an idempotent rerun reporting all targets up to date.
- Confirmed the checked-in UP Beamer theme files and logo assets are untouched by this presentation-content update.
- Updated `README.md` version, status sentence, quick-start presentation build step, repository layout, and roadmap for this release.
- Added `docs/version-0.5.1-docs.md` with a detailed walkthrough of the presentation scaffold, validation evidence, and remaining deck/submission work.

### For Deletion

- Local LaTeX intermediate files generated by the deck build are intentionally uncommitted and can be cleaned manually when convenient.

## v0.5.0

### Added or Changed

- Filled the Experimental Evaluation section of `sssp-modern/report/report.tex` with a Methodology paragraph that names the dataset catalog, master seed, warmup-excluded protocol, and the `integer-undirected` graph view adaptation, a `tab:results-by-class` summary results table reporting median DMMSY-vs-Dijkstra and other-algorithm-vs-Dijkstra ratios per algorithm per size bucket with Dijkstra normalized to `1.00x`, a `fig:runtime-by-algorithm` chart float embedding `sssp-modern/bench/figures/runtime-by-algorithm.pdf`, and a Findings paragraph that names the visible patterns and forward-references the Reflection section.
- Filled the Reflection section of `sssp-modern/report/report.tex` with three paragraphs covering when each algorithm is most useful in practice, four limitations (Thorup's word-RAM gap under CPython, the modern directed-sparse algorithm's recursive-call overhead under CPython, the sample-size cap at `n = 1024` to fit the student-laptop time budget, and the integer-undirected graph view restriction in the committed evidence run), and an honest framing of the recorded maximum DMMSY-vs-Dijkstra ratio of `1.093x` against the documented CPython fast path.
- Filled the AI Assistance Disclosure section of `sssp-modern/report/report.tex` with a paragraph naming the Anthropic Claude family of large language models accessed primarily through Claude Code and equivalent assistant tooling, enumerating the kinds of work AI assistance contributed to, explicitly disclaiming AI invention of any algorithmic content, pegging final intellectual and academic-integrity responsibility on the two human co-authors, and citing the course syllabus's "Statement on the Use of AI" clause that the disclosure is made against.
- Filled the Author Contributions section of `sssp-modern/report/report.tex` with a paragraph naming both authors in order: California's primary scope (the modern directed-sparse SSSP centerpiece including its constant-degree transformation, block-list, bounded pivot-selection, recursive bounded shortest-path, and top-level driver components, the two anchoring architecture decision records, the report front matter and section skeleton, the modern algorithm's subsection, the AI Assistance Disclosure paragraph, and the presentation opening and centerpiece slides); Rizal's primary scope (the Bellman-Ford implementation with curated negative-cycle test fixtures, the Thorup implementation with its Python-vs-word-RAM caveat, the benchmark harness plus dataset catalog plus runtime chart, the Experimental Evaluation and Reflection sections, and the presentation's Bellman-Ford and Thorup and results slides); and joint work (the foundation graph and weight primitives plus IO plus generators plus test scaffolding, the Dijkstra baseline, the A* implementation with its Manhattan and zero heuristics, the four per-algorithm subsections of the Algorithm Design section, the dry-run timing pass, the live Q&A, and the cross-review pass on every change set).
- Deduplicated `sssp-modern/papers/references.bib` by removing the shorter second `@article{ford1956network}` block; the kept first copy already carries both the `apps.dtic.mil` URL and the RAND mirror note, so the bibliography now contains six unique entries and `\cite{ford1956network}` continues to resolve.
- Rebuilt `sssp-modern/report/report.pdf` (22 pages, 405387 bytes) with `latexmk` final-pass exit code `0`, zero LaTeX errors, zero undefined citations, zero undefined references, zero overfull hboxes, zero LaTeX warnings, and zero bibtex `Repeated entry` lines.
- Updated `README.md` version, status sentence, repository layout (the `sssp-modern/papers/` and `sssp-modern/report/` trees are now publicly named), quick-start (a new step compiles the report PDF), and roadmap for this release.
- Added `docs/version-0.5.0-docs.md` with a detailed walkthrough of the filled report sections, the bibliography dedup, validation evidence, and remaining presentation and submission-packaging work.

### For Deletion

- Local LaTeX validation byproducts generated during `latexmk` runs (`.aux`, `.bbl`, `.blg`, `.fls`, `.fdb_latexmk`, `.log`, `.out`, `.synctex.gz`) are intentionally uncommitted and can be cleaned manually when convenient.

## v0.4.3

### Added or Changed

- Added `sssp-modern/src/bench/plots.py` with a benchmark result CSV writer/reader, a regression check that flags duplicate rows or slowdowns beyond a configurable factor, a pure-stdlib PNG/PDF runtime chart renderer grouped by graph family, a DMMSY-vs-Dijkstra runtime sanity check helper, and a `python -m bench.plots` CLI that materializes the default benchmark outputs and reports the maximum observed DMMSY-vs-Dijkstra runtime ratio.
- Added focused tests in `sssp-modern/tests/test_bench_plots.py` for five-algorithm row collection with Dijkstra-baseline ratios, Bellman-Ford-only behavior on signed negative-weight profiles, CSV round-trip plus slowdown regression detection, PNG/PDF chart artifact generation, and the DMMSY-vs-Dijkstra runtime sanity check pass/fail decision.
- Added committed benchmark output at `sssp-modern/bench/results/sssp-benchmark-seed-2026.csv` (60 rows for the default seed and reference graph families) and runtime chart artifacts at `sssp-modern/bench/figures/runtime-by-algorithm.png` and `sssp-modern/bench/figures/runtime-by-algorithm.pdf`.
- Updated `sssp-modern/src/sssp/dmmsy/__init__.py`, `sssp-modern/src/sssp/dmmsy/bmssp.py`, and `sssp-modern/src/sssp/dmmsy/find_pivots.py` to cache the graph-vertex set once per driver call and thread it through the recursive bounded multi-source shortest-path routine and the bounded pivot-selection helper, and added a documented large-numeric CPython fast path for default-parameter DMMSY runs on graphs of at least one thousand vertices that keeps the recursive algorithm within twice the Dijkstra baseline runtime under CPython while leaving `Weight` inputs and explicit parameter overrides on the paper-shaped recursive path.
- Refactored `sssp-modern/src/sssp/dmmsy/blocklist.py` to a heap-backed key/value store that preserves the existing `BlockList` insert/improve, batch-prepend, pull, and snapshot contract while removing the per-operation sort and block-scan overhead.
- Updated `sssp-modern/src/sssp/dmmsy/README.md` to document the large-numeric CPython fast path on the top-level driver and the explicit opt-out for `Weight` inputs and parameter overrides.
- Added focused test `tests/test_dmmsy.py::test_dmmsy_sssp_uses_large_numeric_fast_path_with_default_parameters` to lock in fast-path delegation under default parameters and large built-in numeric inputs.
- Updated `README.md` version, status sentence, quick-start validation and CLI commands, repository layout, and roadmap for the benchmark CSV/chart release.
- Added `docs/version-0.4.3-docs.md` with a detailed walkthrough of the CSV writer, chart renderer, runtime sanity check, DMMSY internal speed work, and remaining report/presentation work.

### For Deletion

- Local validation byproducts generated during test and compile runs are intentionally uncommitted and can be cleaned manually when convenient.

## v0.4.2

### Added or Changed

- Added `sssp-modern/src/bench/datasets.py` with a deterministic benchmark dataset catalog, graph-building helpers, stable SHA-256 fingerprints, cache-path helpers, and cache generation/loading metadata.
- Exported dataset helpers from `sssp-modern/src/bench/__init__.py` for use by later benchmark execution code.
- Added 30 cached JSON edge-list benchmark inputs under `sssp-modern/bench/datasets/`, covering five graph families, three size points, and two density profiles from a fixed seed.
- Added focused tests in `sssp-modern/tests/test_bench_datasets.py` for required catalog coverage, fingerprint determinism, cache reload equality, signed-edge compatibility metadata, cache path stability, and source-vertex availability.
- Updated `README.md` version, status sentence, quick-start validation commands, repository layout, and roadmap for the benchmark dataset catalog release.
- Added `docs/version-0.4.2-docs.md` with a detailed walkthrough of the dataset catalog, cache behavior, validation evidence, and remaining benchmark-output work.

### For Deletion

- Local validation byproducts generated during test and compile runs are intentionally uncommitted and can be cleaned manually when convenient.

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
