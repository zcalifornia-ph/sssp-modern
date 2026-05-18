# Version 0.5.7 Documentation

## Quick Diagnostic Read

This release clarifies the written report's AI Assistance Disclosure. The disclosure now separates planning assistance from programming and implementation assistance, naming Claude for planning support and OpenAI Codex GPT 5.5 for programming and implementation support.

You are ready to review this release if you can:

- inspect `sssp-modern/report/report.tex` at the AI Assistance Disclosure section,
- compile the report with `pdflatex` or `latexmk -pdf`,
- confirm the generated PDF has 24 pages.

## One-Sentence Objective

Make the written report's AI-use disclosure more precise by naming which assistant was used for planning and which was used for programming and implementation assistance.

## What Changed

Version `v0.5.7` updates the following public files:

- `sssp-modern/report/report.tex` (AI Assistance Disclosure paragraph).
- `sssp-modern/report/report.pdf` (rebuilt 24-page report PDF).
- `README.md` (version bump, status sentence, and roadmap entry).
- `CHANGELOG.md` (v0.5.7 entry).

It also adds:

- `docs/version-0.5.7-docs.md` (this document).

## Why It Matters

The disclosure is part of the report's academic-integrity record. The previous wording grouped AI assistance broadly. The new wording is clearer:

- Claude is identified as planning support for the project structure, implementation sequence, report outline, and presentation outline.
- OpenAI Codex GPT 5.5 is identified as programming and implementation assistance for code, tests, validation notes, report prose, Beamer prose, and editorial revisions.
- The report still states that AI assistance did not invent algorithmic content.
- The report still states that final design decisions, parameter choices, reflection, faculty-review responses, and academic-integrity responsibility belong to the two human co-authors.
- The AI Assistance Disclosure and Author Contributions sections are reflowed into shorter LaTeX paragraphs so the source is easier to review without changing the underlying attribution content.

## Validation Summary

Disclosure check from the repository root:

```text
The updated disclosure names both Claude and OpenAI Codex GPT 5.5 with distinct roles.
```

Clean compile in `sssp-modern/report/`:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error report.tex
```

Result:

```text
Output written on report.pdf (24 pages, 403173 bytes).
exit: 0
```

Build notes:

- no LaTeX errors,
- remaining diagnostics are the same non-blocking underfull-box, empty-link, and font-substitution warnings already present in the report build.

## Pitfalls

- Keep the disclosure factual and role-specific.
- Do not imply either assistant invented source-paper algorithmic content.
- Rebuild the PDF after any disclosure wording change.
- Keep the human responsibility statement in place.

## Next Steps

1. Re-read the disclosure against the CMSC 142 AI-use policy.
2. Run the timed 10-12 minute presentation dry run.
3. Prepare the reproducible submission package after final report and deck wording are frozen.
