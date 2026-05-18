# Version 0.5.1 Documentation

## Quick Diagnostic Read

This release starts the presentation deck for `sssp-modern`. The Beamer source now opens with the two-author study metadata, gives the audience a clear outline, frames the single-source shortest-path problem, walks through the historical arc, and includes one slide each for Dijkstra, Bellman-Ford, A*, and Thorup. The modern-algorithm centerpiece, experimental-results slides, author-contribution slide, and final dry-run pacing pass remain pending.

You are ready to review this release if you can:

- compile a Beamer deck with `latexmk -pdf`,
- distinguish presentation content changes from theme/style changes,
- check whether bibliography keys resolve and whether a PDF build is clean.

## One-Sentence Objective

Replace the generic Beamer showcase with the first clean-compiling presentation scaffold for the SSSP study while preserving the checked-in UP theme assets.

## What Changed

Version `v0.5.1` updates the following files:

- `sssp-modern/presentation/main.tex` (deck metadata, title page, outline, problem framing, baseline-algorithm slides, placeholders for later content, references, and closing frame).
- `sssp-modern/presentation/references.bib` (six SSSP source-paper entries appended for the deck).
- `sssp-modern/presentation/main.pdf` (rebuilt 20-page deck PDF).
- `README.md` (version bump, status sentence, presentation build step, repository layout, and roadmap entry).
- `CHANGELOG.md` (v0.5.1 entry).

It also adds:

- `docs/version-0.5.1-docs.md` (this document).

## Why It Matters

The written report was complete in `v0.5.0`, but the presentation folder still primarily showed the reusable Beamer theme. This release turns that folder into a project-specific deck that can be expanded slide-by-slide without disturbing the theme files.

The current deck gives reviewers a working spine:

- the title slide names the project, course context, and both authors in order,
- the outline mirrors the intended talk flow,
- the opening section defines the SSSP problem and locates all five algorithms on the historical arc,
- the baseline section gives compact, source-cited slides for Dijkstra, Bellman-Ford, A*, and Thorup,
- the remaining sections are explicit placeholders for the modern-algorithm centerpiece, experimental evaluation, reflection, and author contributions.

That keeps the remaining presentation work bounded: fill the remaining content slides, add the results chart, complete the author-contribution slide, and time the talk.

## Deck Structure

The updated `presentation/main.tex` now contains:

1. A two-author title slide using the UP Beamer theme's supported multi-author layout.
2. An outline frame generated from the deck sections.
3. Two problem-and-motivation frames: one for the formal SSSP problem and one for the five-algorithm historical arc.
4. Four baseline-algorithm frames:
   - Dijkstra: non-negative weighted graphs, heap relaxation, complexity, implementation anchor, source citation.
   - Bellman-Ford: negative-weight support, repeated edge relaxation, negative-cycle reporting, source citations.
   - A*: heuristic-guided search, admissibility framing, zero-heuristic equivalence with Dijkstra, source citation.
   - Thorup: undirected integer-weight setting, word-RAM caveat, structural reference implementation, source citation.
5. Placeholder frames for the modern directed-sparse SSSP centerpiece, experimental evaluation, and reflection/author contributions.
6. A closing frame and a references frame.

Speaker-note comments in the source keep the planned two-presenter handoffs visible while leaving the rendered PDF clean.

## Bibliography Update

The presentation bibliography now carries deck-local entries for the same six source papers used by the report:

- `dijkstra1959note`
- `bellman1958routing`
- `ford1956network`
- `hart1968astar`
- `thorup1999linear`
- `duan2025breaking`

The existing Beamer and UP Visual Identity Guidebook entries remain in place because the references frame still credits the deck infrastructure.

## Validation Summary

Clean compile in `sssp-modern/presentation/`:

```powershell
latexmk -pdf -interaction=nonstopmode main.tex
```

Result:

```text
Output written on main.pdf (20 pages, 1138392 bytes).
Latexmk: All targets (main.pdf) are up-to-date
exit: 0
```

Build-quality checks against the regenerated log files:

```powershell
Select-String -Path main.log -Pattern "^! "                    # 0 matches
Select-String -Path main.log -Pattern "Citation .* undefined"  # 0 matches
Select-String -Path main.log -Pattern "Reference .* undefined" # 0 matches
Select-String -Path main.log -Pattern "^Overfull \\hbox"       # 0 matches
Select-String -Path main.log -Pattern "^LaTeX Warning:"        # 0 matches
```

Resolved citation coverage:

```text
dijkstra1959note
bellman1958routing
ford1956network
hart1968astar
thorup1999linear
duan2025breaking
tantau2004
upvig2017
```

Idempotent rerun:

```text
Latexmk: Nothing to do for 'main.tex'.
Latexmk: All targets (main.pdf) are up-to-date
exit: 0
```

The checked-in UP Beamer theme files and logo assets were not modified.

## Pitfalls

- Do not treat this release as the final course presentation. The centerpiece and results sections still need full content.
- Do not edit the UP Beamer theme files for content work. Keep project-specific slide text in `presentation/main.tex` and bibliography entries in `presentation/references.bib`.
- Do not remove the placeholder frames until their replacement slides compile cleanly; they preserve the talk structure and make unfinished scope obvious.
- Do not read the 20-page PDF length as final pacing. Several current pages are placeholders and the dry-run pass has not happened yet.

## Next Steps

1. Fill the modern directed-sparse SSSP centerpiece with the recursion, pivot-selection, block-list, parameter, and complexity slides.
2. Add the benchmark results chart and concise interpretation slides.
3. Add the reflection and author-contribution slide.
4. Run a timed 10-12 minute dry run and trim or expand slides based on actual speaking time.
5. Prepare the final reproducible submission package after the deck is complete.
