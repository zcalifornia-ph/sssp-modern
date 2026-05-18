# Version 0.5.9 Docs

## Quick Diagnostic Read

This release is a written-report framing pass. It does not change the Python implementations, benchmark outputs, benchmark chart, or presentation deck. The update makes the report's standard of evidence explicit before the algorithm discussion begins.

## One-Sentence Objective

Strengthen the report opening so the manuscript clearly separates source-backed algorithm claims, benchmark-backed runtime claims, and implementation caveats.

## Why This Matters

The project compares algorithms whose theoretical guarantees come from different computational models. The modern directed-sparse result is an asymptotic breakthrough, while the repository implementation runs in pure CPython and reports measured runtime under a constrained benchmark harness. The new opening makes that distinction visible before the reader reaches the technical sections.

## What Changed

- Updated the report header block so the course title, instructor name, report date, and short title are easier to scan.
- Added a cited opening maxim about evidence and proof.
- Added introductory paragraphs explaining how the portfolio treats theory, implementation fidelity, and measured runtime.
- Added a local report bibliography file for the new non-algorithm citation.
- Updated the report bibliography command so it reads both the shared SSSP paper bibliography and the local report bibliography.
- Replaced one section-number reference with the written section title for clearer prose.
- Reflowed the AI assistance disclosure into a tighter grouped paragraph block while preserving its substantive disclosure.
- Rebuilt the report PDF from the revised LaTeX source.

## Artifact Map

- `sssp-modern/report/report.tex`: report header, opening framing, citation wiring, and disclosure spacing.
- `sssp-modern/report/references.bib`: local report bibliography entry for the new opening citation.
- `sssp-modern/report/report.pdf`: compiled 25-page report.
- `README.md`: version marker, status text, report build note, repository layout, and roadmap update.
- `CHANGELOG.md`: release summary and validation evidence.
- `docs/version-0.5.9-docs.md`: this detailed release note.

## Validation Evidence

Command run from `sssp-modern/report`:

```powershell
latexmk -pdf -interaction=nonstopmode -f report.tex
```

Result:

- Exit code: `0`.
- `latexmk` reported all targets up to date.
- `pdfinfo sssp-modern/report/report.pdf` reports `25` pages.
- The compiled PDF size is `406577` bytes.

## What Did Not Change

- No algorithm source files changed.
- No tests changed.
- No benchmark CSV, dataset, or runtime chart changed.
- No presentation source or presentation PDF changes are part of this release scope.
- No security, contributor, code-of-conduct, or third-party notice update was needed.

## Remaining Work

The next public milestone remains presentation dry-run pacing and reproducible submission packaging.
