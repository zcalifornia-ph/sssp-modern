# Version 1.0.0 Docs

## Quick Diagnostic Read

This release promotes `sssp-modern` to a stable public baseline. It does not change the Python algorithm implementations, benchmark datasets, benchmark results, runtime chart, or written report. The tracked release change is the final presentation pacing/layout pass plus documentation reconciliation.

## One-Sentence Objective

Finalize the presentation deck and release documentation so the implementation, benchmarks, report, and deck are all represented as the stable `1.x` baseline.

## Why This Matters

The repository now has a complete public story: algorithms, validation, benchmark evidence, written report, and presentation are all available from tracked sources. The final deck pass keeps the visual examples readable without changing the underlying technical claims.

## What Changed

- Promoted the project version marker to `v1.0.0`.
- Tightened the presentation's visual walkthroughs by adjusting diagram connectors, labels, stale-entry notation, and dense layout points across the Dijkstra, Bellman-Ford, A*, Thorup, and DMMSY slides.
- Rebuilt the presentation PDF from the revised Beamer source.
- Updated release notes, roadmap text, and status text to describe the stable baseline.
- Reconciled internal completion notes for the final presentation pacing/layout milestone.

## Artifact Map

- `sssp-modern/presentation/main.tex`: final pacing/layout refinements.
- `sssp-modern/presentation/main.pdf`: compiled 30-page deck.
- `README.md`: stable-release version marker, status text, deck build note, repository layout, and roadmap.
- `CHANGELOG.md`: stable-release summary and validation evidence.
- `docs/version-1.0.0-docs.md`: this detailed release note.

## Validation Evidence

Command run from `sssp-modern/presentation`:

```powershell
latexmk -pdf -interaction=nonstopmode main.tex
```

Result:

- Exit code: `0`.
- `latexmk` reported `main.pdf` up to date.
- `pdfinfo sssp-modern/presentation/main.pdf` reports `30` pages.
- `sssp-modern/presentation/main.pdf` is `1317126` bytes.
- Log scans found no LaTeX errors, undefined citations, undefined references, overfull hboxes/vboxes, LaTeX warnings, hyperref warnings, or pdfTeX warnings.
- The runtime chart path still renders from `../bench/figures/runtime-by-algorithm.pdf`.

## What Did Not Change

- No algorithm source files changed.
- No tests changed.
- No benchmark CSV, dataset, or runtime chart changed.
- No written report source or report PDF changes are part of this release scope.
- No security, contributor, code-of-conduct, or third-party notice update was needed.

## Stable Baseline

Use `v1.0.0` as the first stable public reference point for the study repository. Future changes should be versioned as maintenance, documentation, or feature updates depending on whether they change release documentation, presentation/report assets, or implementation behavior.
