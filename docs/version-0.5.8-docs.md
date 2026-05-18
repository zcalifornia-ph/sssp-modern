# Version 0.5.8 Docs

## Quick Diagnostic Read

This release is a presentation-flow polish pass. It does not change the Python implementations, benchmark data, written report content, or bibliography. The update makes the evidence slide part of the timed deck path instead of leaving it as backup material.

## One-Sentence Objective

Move the project evidence into the main presentation flow so reviewers see the repository, benchmark, test, and report anchors before the reflection and contribution discussion.

## Why This Matters

The presentation already had the right evidence, but the most important validation pointers lived at the end as optional Q&A backup. That made them easy to skip during a timed run. This release places the evidence directly before the reflective and author-contribution material, making the talk easier to defend without adding implementation scope.

## What Changed

- Added a `Result Evidence` frame in `sssp-modern/presentation/main.tex` before the reflection section.
- Added the public repository URL to that frame: `https://github.com/zcalifornia-ph/sssp-modern`.
- Kept the evidence pointers to the committed benchmark CSV, runtime figure, 147-test validation result, maximum recorded DMMSY/Dijkstra ratio for large benchmark inputs, and report table/figure anchors.
- Reworded the evidence caveat as final framing for the main talk: the project centers correctness and implementation structure rather than claiming a CPython timing victory.
- Removed the older backup-only evidence frame from the appendix area.
- Removed the standalone closing standout slide so the deck moves more directly from contributions and references into the questions frame.
- Updated the compiled presentation PDF to match the Beamer source.

## Artifact Map

- `sssp-modern/presentation/main.tex`: source deck update.
- `sssp-modern/presentation/main.pdf`: compiled 25-page deck.
- `README.md`: version marker, status text, quick-start page count, repository layout, and roadmap update.
- `CHANGELOG.md`: release summary and validation evidence.
- `docs/version-0.5.8-docs.md`: this detailed release note.

## Validation Evidence

Command run from `sssp-modern/presentation`:

```powershell
latexmk -pdf -interaction=nonstopmode main.tex
```

Result:

- Exit code: `0`.
- `latexmk` reported all targets up to date.
- `pdfinfo sssp-modern/presentation/main.pdf` reports `25` pages.
- The compiled PDF size is `1250772` bytes.

## What Did Not Change

- No algorithm source files changed.
- No benchmark CSV or runtime chart data changed.
- No written report source or report PDF changes are part of this release scope.
- No security, contributor, code-of-conduct, or third-party notice update was needed.

## Remaining Work

The next public milestone remains presentation dry-run pacing and reproducible submission packaging. This release makes that easier because the deck now surfaces the validation evidence in the main presentation path.
