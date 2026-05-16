# Version 0.5.0 Documentation

## Quick Diagnostic Read

This release completes the written report manuscript at `sssp-modern/report/report.tex`. The Experimental Evaluation section now ties the modern directed-sparse SSSP result to the committed benchmark CSV and runtime chart from `v0.4.3`, the Reflection section interprets those numbers honestly against the Dijkstra baseline, and two academic-integrity sections (AI Assistance Disclosure and Author Contributions) are now present. The bibliography source at `sssp-modern/papers/references.bib` is also deduplicated so `latexmk` produces the report PDF with a clean bibtex log and a zero final-pass exit code.

You are ready to review this release if you can:

- compile a LaTeX document with `latexmk -pdf` from a fresh clone,
- read a small results table and tell a per-size-bucket median ratio from a single per-row sample,
- reason about why a Python-hosted implementation of a word-RAM algorithm or a deeply recursive routine can move differently from its abstract complexity bound under CPython.

## One-Sentence Objective

Complete the written report manuscript by adding the experimental evaluation, reflection, AI assistance disclosure, and author contributions sections, and deduplicate the bibliography source so the compiled PDF is clean.

## What Changed

Version `v0.5.0` updates the following files:

- `sssp-modern/report/report.tex` (Experimental Evaluation, Reflection, AI Assistance Disclosure, and Author Contributions content blocks filled).
- `sssp-modern/report/report.pdf` (rebuilt 22-page manuscript with the new content blocks).
- `sssp-modern/papers/references.bib` (duplicate `ford1956network` entry removed; six unique bibliography entries remain).
- `README.md` (version bump, status sentence, repository layout, and roadmap entry for this release).
- `CHANGELOG.md` (v0.5.0 entry).

It also adds:

- `docs/version-0.5.0-docs.md` (this document).

## Why It Matters

The benchmark CSV and runtime chart shipped in `v0.4.3` produced reproducible measurement evidence, but the written report did not yet read those artifacts back out as a comparative narrative. This release closes that gap so a reader can follow the manuscript end-to-end:

- the Experimental Evaluation section explicitly cites `sssp-modern/bench/results/sssp-benchmark-seed-2026.csv` as the per-row evidence source and embeds `sssp-modern/bench/figures/runtime-by-algorithm.pdf` as the visual companion,
- a summary results table compresses the 60-row CSV into per-algorithm medians across the small (`n = 64`), medium (`n = 256`), and large (`n = 1024`) size buckets, with the Dijkstra baseline normalized to `1.00x`,
- the Reflection section names when each algorithm is most useful, what the four salient limitations are, and how to read the headline DMMSY result honestly against the Dijkstra baseline at the committed sample sizes,
- the AI Assistance Disclosure paragraph documents the AI tooling that contributed to the work and disclaims AI invention of any algorithmic content,
- the Author Contributions paragraph names each author's primary scope and the work that was joint.

The bibliography dedup is the last hygiene item that prevented `latexmk` from exiting `0` on the final pass. With it cleared, the PDF build is fully clean: zero LaTeX errors, zero undefined citations, zero undefined references, zero overfull hboxes, zero LaTeX warnings, and zero bibtex `Repeated entry` lines.

## Report Manuscript Sections Filled

This release fills the four remaining content blocks in `report/report.tex` and leaves every earlier section intact:

1. **Experimental Evaluation** at `sec:experimental-evaluation`. Four ordered blocks: a Methodology paragraph that names the dataset catalog (geometric and Barabasi-Albert generators across three size points and two density profiles), the master seed (`2026`), the warmup-excluded one-recorded-repeat protocol, the `integer-undirected` graph view adaptation that lets Thorup compete on the same input as the other four algorithms, and the per-row evidence path; a `tab:results-by-class` summary table reporting median `ratio_vs_dijkstra` per algorithm per size bucket with Dijkstra normalized to `1.00x`; a `fig:runtime-by-algorithm` chart float importing `bench/figures/runtime-by-algorithm.pdf` via `\includegraphics[width=\linewidth]{...}`; and a Findings paragraph naming the visible patterns (A* tracks or beats Dijkstra on geometric graphs thanks to its admissible heuristic; Bellman-Ford rises monotonically because no early-exit triggers on dense and Barabasi-Albert profiles; Thorup sits steadily above Dijkstra on CPython because Python's arbitrary-precision integers and `bit_length` are not constant-time on the abstract word-RAM model; DMMSY collapses to roughly Dijkstra at `n = 1024` because the documented numeric fast path engages for default numeric inputs at that size).
2. **Reflection** at `sec:reflection`. Three ordered paragraphs: when each algorithm is most useful in practice; four limitations (Thorup's word-RAM gap under CPython, DMMSY's recursive-call overhead, the `n = 1024` sample cap, and the integer-undirected graph view restriction); and an honest framing of the DMMSY result that cites the recorded maximum DMMSY/Dijkstra ratio of `1.093x` at `n >= 1000`, explains that this number reflects the documented CPython fast-path engagement rather than a recursive comparison-addition run, and frames the centerpiece value of the modern algorithm as its structural novelty plus the correctness of its realized implementation.
3. **AI Assistance Disclosure** at `sec:ai-disclosure`. One paragraph naming the AI tooling used (the Anthropic Claude family of large language models, accessed primarily through Claude Code and equivalent assistant tooling), enumerating the kinds of work AI assistance contributed to (drafting Python implementations and unit tests for all five algorithms against the cited source papers; drafting and reviewing internal design documentation; drafting the prose and pseudocode of the report and deck; proposing structural and editorial revisions), explicitly disclaiming AI invention of any algorithmic content (every algorithm in the study is taken from the cited source papers and validated against the Dijkstra oracle plus curated golden test fixtures plus the comparison-addition fidelity invariant enforced by the `Weight` wrapper), pegging final intellectual and academic-integrity responsibility on the two human co-authors, and naming the course syllabus's "Statement on the Use of AI" clause that the disclosure is made against.
4. **Author Contributions** at `sec:author-contributions`. One paragraph naming both authors in order: California led the modern directed-sparse SSSP centerpiece (the constant-degree graph transformation, the block-list frontier partitioning data structure, the bounded pivot-selection helper, the recursive bounded multi-source shortest-path routine, and the top-level driver with the runtime sanity bound), the two anchoring architecture decision records, the report front matter and section skeleton, the modern algorithm's subsection in the report, this AI Assistance Disclosure paragraph, and the presentation opening and centerpiece slides; Rizal led the Bellman-Ford implementation including curated negative-cycle test fixtures, the Thorup implementation including the Python-vs-word-RAM caveat, the benchmark harness and dataset catalog and runtime chart, the report's Experimental Evaluation and Reflection sections, and the presentation's Bellman-Ford, Thorup, and results slides; the foundation (graph and weight types, edge-list IO, the random graph generators, the test-harness scaffolding), the Dijkstra baseline, the A* implementation with its Manhattan and zero heuristics, the four per-algorithm subsections of the report's Algorithm Design section, the dry-run timing pass, the live Q&A, and the cross-review pass on every change set were joint work.

## Bibliography Dedup

`sssp-modern/papers/references.bib` previously carried seven `@article{...}` blocks because `ford1956network` appeared twice: a more complete copy with both the `apps.dtic.mil` URL and a `note` line pointing at the RAND mirror, and a shorter copy with only the RAND mirror URL. Bibtex silently skipped the second copy and resolved `\cite{ford1956network}` against the first, but it still emitted `Repeated entry---line 45 of file ../papers/references.bib` on every `latexmk` pass, which forced the final-pass exit code to `12` even though the LaTeX build itself succeeded.

The shorter second copy is removed. The kept first copy already carries both URLs, so no information is lost. The deduped bibliography now contains six entries: `ford1956network`, `hart1968astar`, `bellman1958routing`, `thorup1999linear`, `dijkstra1959note`, and `duan2025breaking`.

## Validation Summary

Clean compile (in `sssp-modern/report/`):

```powershell
latexmk -C report.tex
latexmk -pdf -interaction=nonstopmode -f report.tex
```

Result:

```text
Output written on report.pdf (22 pages, 405387 bytes).
Latexmk: All targets (report.pdf) are up-to-date
exit: 0
```

Build-quality checks against the regenerated log files:

```powershell
Select-String -Pattern "^! "                       -Path report.log    # 0 matches
Select-String -Pattern "Citation .* undefined"      -Path report.log    # 0 matches
Select-String -Pattern "Reference .* undefined"     -Path report.log    # 0 matches
Select-String -Pattern "Overfull \\hbox"            -Path report.log    # 0 matches
Select-String -Pattern "^LaTeX Warning:"            -Path report.log    # 0 matches
Select-String -Pattern "Repeated entry"             -Path report.blg    # 0 matches
```

Citation key coverage (six unique keys resolve):

```text
\citation{bellman1958routing}
\citation{dijkstra1959note}
\citation{duan2025breaking}
\citation{ford1956network}
\citation{hart1968astar}
\citation{thorup1999linear}
```

Hyperref anchor coverage:

```text
14 section anchors retained from the existing skeleton.
2 new anchors: tab:results-by-class on page 16, fig:runtime-by-algorithm on page 17.
```

Bibliography entry count after dedup:

```powershell
Select-String -Pattern "^@article" -Path ../papers/references.bib   # 6 matches
```

Idempotent rerun:

```text
Latexmk: Nothing to do for 'report.tex'.
Latexmk: All targets (report.pdf) are up-to-date
exit: 0
```

Diff hygiene:

```powershell
git diff --check    # exit 0
```

Python regression suite is unaffected by this release. The most recent full-suite evidence remains:

```text
147 passed
```

from `python -m pytest tests` in `sssp-modern/` on the prior release.

## Pitfalls

- Do not treat the median `ratio_vs_dijkstra` numbers in the summary results table as a portable cross-machine ranking. The reproducibility guarantee is the protocol and the seed; absolute wall-clock numbers will move with hardware, interpreter version, and concurrent load.
- Do not infer that the modern directed-sparse SSSP algorithm is asymptotically observed as faster than Dijkstra at the committed sample sizes. The recorded `1.093x` maximum ratio at `n >= 1000` reflects the documented CPython fast-path engagement for default numeric inputs; the asymptotic crossover predicted by the source paper is on the abstract comparison-addition model and is not directly observable on CPython at `n = 1024`.
- Do not edit `sssp-modern/papers/references.bib` to add the duplicate `ford1956network` block back. The deduplicated state is what keeps `latexmk` exiting `0` on the final pass.
- Do not assume the AI Assistance Disclosure paragraph generalizes beyond this submission. It documents the AI tooling and activity scope for the work captured in this manuscript only.

## Next Steps

1. Fill the Beamer presentation deck under `sssp-modern/presentation/` with the report's content, dedicating the opening and the longest content slot to the modern directed-sparse algorithm and reusing the Author Contributions wording on the deck's contributions slide.
2. Run a dry-run timing pass on the deck to confirm the presentation lands inside the course's allotted slot.
3. Package the submission bundle: the compiled `report/report.pdf`, the compiled `presentation/main.pdf`, the source zip of `sssp-modern/src/`, a grader-facing README, and the committed benchmark CSV plus chart artifacts.
4. Reconcile root governance docs against the final submission state (`README.md`, `CHANGELOG.md`, `THIRD-PARTY-NOTICES.md`) and emit the merge commit ahead of the course deadline.
