# Version 0.5.11 Docs

## Quick Diagnostic Read

This release is a presentation baseline-visuals pass. It does not change the Python implementations, benchmark outputs, benchmark chart, or written report. The update adds worked examples for the remaining baseline algorithms so the presentation now has visual mechanics for all five algorithms in the study arc.

## One-Sentence Objective

Make the presentation easier to teach by adding concrete Bellman-Ford, A*, and Thorup walkthrough slides beside the existing Dijkstra and modern directed-sparse visual examples.

## Why This Matters

The deck now shows each algorithm through the data structure or update rule that makes it distinctive. Bellman-Ford becomes repeated edge sweeps, A* becomes `g + h` frontier ordering, Thorup becomes integer-bucket movement, and the modern directed-sparse method remains bounded local pulling. That gives the audience a consistent visual bridge from baseline algorithms to the centerpiece result.

## What Changed

- Added a Bellman-Ford worked example showing edge scan order, a negative relaxation, round-by-round distance changes, early exit, and a clean cycle-check pass.
- Added an A* worked example showing a tight chain heuristic, a looser dead-end heuristic, and the reason the dead-end branch never gets expanded.
- Added a Thorup worked example showing how tentative labels move through bucket positions keyed by most-significant differing bits.
- Updated the author-contribution slide to wrap dense wording and point to public repository history plus closed issues and pull requests.
- Rebuilt the presentation PDF from the revised Beamer source.

## Artifact Map

- `sssp-modern/presentation/main.tex`: new Bellman-Ford, A*, and Thorup worked-example frames plus contribution-slide wording cleanup.
- `sssp-modern/presentation/main.pdf`: compiled 30-page deck.
- `README.md`: version marker, status text, presentation build note, repository layout, and roadmap update.
- `CHANGELOG.md`: release summary and validation evidence.
- `docs/version-0.5.11-docs.md`: this detailed release note.

## Validation Evidence

Command run from `sssp-modern/presentation`:

```powershell
latexmk -pdf -interaction=nonstopmode main.tex
```

Result:

- Exit code: `0`.
- `latexmk` reported `main.pdf` up to date.
- `pdfinfo sssp-modern/presentation/main.pdf` reports `30` pages.
- `sssp-modern/presentation/main.pdf` is `1317006` bytes.

The presentation source and PDF are the only project artifacts changed by the deck update itself.

## What Did Not Change

- No algorithm source files changed.
- No tests changed.
- No benchmark CSV, dataset, or runtime chart changed.
- No written report source or report PDF changes are part of this release scope.
- No security, contributor, code-of-conduct, or third-party notice update was needed.

## Remaining Work

The next public milestone remains presentation dry-run pacing and reproducible submission packaging.
