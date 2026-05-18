<!-- Adapted from Best-README-Template. Reference-style links live at the bottom of this file. -->
<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

</div>

<!-- ABOUT THE PROJECT -->
[![sssp-modern Screen Shot][product-screenshot]](https://github.com/zcalifornia-ph/sssp-modern)

<div align="center">
<h3 align="center">sssp-modern</h3>

  <p align="center">
    <strong>A study of single-source shortest-path algorithms from Dijkstra's 1959 baseline to the 2025 result that broke its sorting barrier on sparse directed graphs, with reference implementations and comparative complexity analysis.</strong>
    <br />
    Version: v0.5.7
    <br />
    Status: Dijkstra, Bellman-Ford, A*, Thorup, and the modern directed-sparse SSSP driver are in place; benchmark timing, dataset catalog, result CSV writing, runtime chart rendering, and the completed written report are available; the report and presentation now use plain public-facing terminology, and the report's AI assistance disclosure distinguishes Claude planning support from OpenAI Codex GPT 5.5 implementation support, with dry-run pacing and submission packaging still pending
    <br />
    <a href="https://github.com/zcalifornia-ph/sssp-modern"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/zcalifornia-ph/sssp-modern">View Repository</a>
    &middot;
    <a href="https://github.com/zcalifornia-ph/sssp-modern/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/zcalifornia-ph/sssp-modern/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
## Table of Contents

1. [About The Project](#about-the-project)
   - [Scope](#scope)
   - [Algorithms In Scope](#algorithms-in-scope)
   - [What sssp-modern Is Not](#what-sssp-modern-is-not)
2. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Quick Start](#quick-start)
3. [Repository Layout](#repository-layout)
4. [Roadmap](#roadmap)
5. [Contributing](#contributing)
6. [License](#license)
7. [Third-Party Notices](THIRD-PARTY-NOTICES.md)
8. [Contact](#contact)
9. [Acknowledgments](#acknowledgments)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## About The Project

`sssp-modern` is a study repository for the single-source shortest-path (SSSP) problem on directed graphs with non-negative real edge weights. It walks the line of progress from Dijkstra's 1959 baseline algorithm to the 2025 result that broke the long-standing comparison-based sorting barrier of `O(m + n log n)` for sparse directed graphs.

The repository is organized to support three intertwined goals:

- **Reference implementations** of the canonical algorithms in the SSSP literature, written for clarity first and then for measured efficiency.
- **Comparative complexity analysis** that traces tight time and space bounds, the model of computation each result assumes, and the constraints (graph density, weight model, integer vs. real weights) under which each bound applies.
- **An evidence-backed walkthrough** of how the modern result improves on Dijkstra and how it relates to intermediate milestones such as Fibonacci-heap Dijkstra, Thorup's RAM-model results for integer weights, and Bellman–Ford's negative-edge handling.

### Scope

This repository targets the directed, non-negative-weight SSSP problem unless a specific reference implementation states otherwise. Negative-edge variants and all-pairs shortest paths are referenced for context but are not the primary subject.

### Algorithms In Scope

Implemented and planned reference implementations and comparative notes include:

- Dijkstra's algorithm (1959 baseline, binary-heap, and Fibonacci-heap variants).
- A* search with pluggable heuristics, including zero and Manhattan heuristics for goal-directed path demos.
- Bellman–Ford for context on negative edges and dynamic-programming structure.
- Thorup-style results for integer-weight undirected SSSP under the word-RAM model, implemented as a documented Python reference with an explicit runtime-model caveat.
- The 2025 sub-`O(m + n log n)` directed-sparse SSSP result, with implementation following the published structure.

### What sssp-modern Is Not

- Not a production-grade graph library and not a drop-in replacement for established graph frameworks.
- Not a benchmark of real-world routing or network-routing platforms.
- Not a tutorial on graph theory fundamentals; readers are assumed to be comfortable with graphs, asymptotic analysis, and standard data structures.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Status: Dijkstra, Bellman-Ford, A*, Thorup, and the modern directed-sparse SSSP driver are implemented (`v0.5.7`). The repository now includes pure-stdlib Python graph primitives, a comparison-addition `Weight` wrapper, deterministic JSON graph fixtures, seeded graph generators, reusable pytest scaffolding, a binary-heap Dijkstra baseline, a Bellman-Ford implementation with negative-cycle reporting, an A* implementation with reusable heuristics, a Thorup-style hierarchical bucket reference for undirected integer-weight graphs, the top-level driver for the modern directed-sparse SSSP implementation, a reusable benchmark timing harness, a deterministic benchmark dataset catalog with cached JSON graph inputs, a benchmark result CSV writer plus pure-stdlib PNG/PDF runtime chart renderer with a DMMSY-vs-Dijkstra runtime sanity check, a complete written report manuscript whose experimental evaluation and reflection sections cite the committed CSV and runtime chart directly, and a Beamer presentation deck with the title slide, outline, problem framing, four baseline-algorithm slides, four modern-algorithm centerpiece slides, benchmark-results slides, reflection and integrity framing, author contributions, references, closing frame, Q&A evidence backup, final copy-fit/layout polish, and public-facing terminology cleanup already compiling cleanly. The written report source has also been cleaned so report comments, implementation notes, caveats, tables, AI-use disclosure, and author contributions avoid private planning labels and use reviewer-readable wording; the AI assistance disclosure now separately identifies Claude for planning support and OpenAI Codex GPT 5.5 for programming and implementation assistance.

### Prerequisites

- Git for cloning the repository.
- CPython 3.11 or later.
- `pytest` for the current test suite.
- A working TeX distribution that provides `latexmk` (e.g. MiKTeX or TeX Live) for rebuilding the report PDF.
- Optional: `networkx` for oracle comparisons in tests.
- Optional: `coverage` for line-coverage measurement.

### Quick Start

1. Clone the repo.

   ```sh
   git clone https://github.com/zcalifornia-ph/sssp-modern.git
   cd sssp-modern
   ```

2. Install test tooling if needed.

   ```sh
   python -m pip install pytest networkx coverage
   ```

3. Run the current implementation test suite.

   ```sh
   cd sssp-modern
   PYTHONPATH=src python -m pytest tests
   ```

   PowerShell equivalent:

   ```powershell
   cd sssp-modern
   $env:PYTHONPATH='src'
   python -m pytest tests
   ```

4. Measure focused algorithm coverage when `coverage` is installed.

   ```powershell
   python -m coverage run --include='src/sssp/bellman_ford.py' -m pytest tests/test_bellman_ford.py
   python -m coverage report -m src/sssp/bellman_ford.py
   ```

5. Measure Thorup coverage when needed.

   ```powershell
   python -m coverage run --source=sssp.thorup99 -m pytest tests/test_thorup99.py
   python -m coverage report --include='src/sssp/thorup99.py'
   ```

6. Measure the modern directed-sparse graph-transformation coverage when needed.

   ```powershell
   python -m coverage run --include='src/sssp/dmmsy/transform.py' -m pytest tests/test_dmmsy_transform.py
   python -m coverage report --include='src/sssp/dmmsy/transform.py'
   ```

7. Measure the modern directed-sparse block-list coverage when needed.

   ```powershell
   python -m coverage run --include='src/sssp/dmmsy/blocklist.py' -m pytest tests/test_dmmsy_blocklist.py
   python -m coverage report --include='src/sssp/dmmsy/blocklist.py'
   ```

8. Measure the modern directed-sparse pivot-selection coverage when needed.

   ```powershell
   python -m coverage run --include='src/sssp/dmmsy/find_pivots.py' -m pytest tests/test_dmmsy_find_pivots.py
   python -m coverage report --include='src/sssp/dmmsy/find_pivots.py'
   ```

9. Measure the modern directed-sparse recursive bounded shortest-path coverage when needed.

   ```powershell
   python -m coverage run --include='src/sssp/dmmsy/bmssp.py' -m pytest tests/test_dmmsy_bmssp.py
   python -m coverage report --include='src/sssp/dmmsy/bmssp.py'
   ```

10. Measure the modern directed-sparse top-level driver coverage when needed.

    ```powershell
    python -m coverage run --include='src/sssp/dmmsy/__init__.py' -m pytest tests/test_dmmsy.py
    python -m coverage report --include='src/sssp/dmmsy/__init__.py'
    ```

11. Validate the reusable benchmark timing harness when needed.

    ```powershell
    python -m pytest tests/test_bench_runner.py
    ```

12. Validate the benchmark dataset catalog and cache helpers when needed.

    ```powershell
    python -m pytest tests/test_bench_datasets.py
    ```

13. Validate the benchmark result CSV writer, runtime chart renderer, and DMMSY-vs-Dijkstra runtime sanity check when needed.

    ```powershell
    python -m pytest tests/test_bench_plots.py
    ```

14. Materialize a fresh benchmark CSV and runtime chart when needed.

    ```powershell
    python -m bench.plots
    ```

    The CLI writes `bench/results/sssp-benchmark-seed-2026.csv` and `bench/figures/runtime-by-algorithm.{png,pdf}` and reports the maximum observed DMMSY-vs-Dijkstra runtime ratio for graphs of at least one thousand vertices.

15. Rebuild the written report PDF when needed.

    ```powershell
    cd report
    latexmk -pdf -interaction=nonstopmode -f report.tex
    ```

    The build produces `report/report.pdf` (currently 24 pages) and reads the bibliography from `papers/references.bib` plus the runtime chart from `bench/figures/runtime-by-algorithm.pdf`.

16. Rebuild the presentation deck PDF when needed.

    ```powershell
    cd presentation
    latexmk -pdf -interaction=nonstopmode main.tex
    ```

    The current deck build produces `presentation/main.pdf` (26 pages) from the polished, public-facing Beamer source and `presentation/references.bib`.

17. Review `CHANGELOG.md` for the latest notable changes.
18. Check `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` before opening issues or pull requests.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Repository Layout

The repository keeps governance, supporting assets, and study material in clearly separated trees:

- Root governance files: `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `LICENSE.txt`, and `THIRD-PARTY-NOTICES.md`.
- `docs/`: per-version detail documents tracking what shipped in each release.
- `repo/images/`: repository-owned image assets, including the project screenshot.
- `sssp-modern/docs/issues/`: structured issue artifacts that capture scoped implementation work before coding begins.
- `sssp-modern/src/sssp/`: pure-stdlib Python graph, weight, IO, generator, Dijkstra, Bellman-Ford, A*, Thorup, and modern directed-sparse SSSP support modules.
- `sssp-modern/src/sssp/dmmsy/`: the 2025 directed-sparse SSSP implementation, including the constant-degree graph transformation, block-list frontier partitioning data structure, bounded pivot-selection helper, recursive bounded multi-source shortest-path routine, and the top-level public driver `dmmsy_sssp(graph, source)` with paper-faithful parameter wiring.
- `sssp-modern/src/bench/`: reusable benchmark timing harness that records warmup-excluded runtime samples, medians, and interquartile ranges, plus a result CSV writer/reader and a pure-stdlib PNG/PDF runtime chart renderer with a DMMSY-vs-Dijkstra runtime sanity check and a `python -m bench.plots` CLI.
- `sssp-modern/bench/datasets/`: cached JSON edge-list benchmark inputs generated from five graph families across three size points and two density profiles.
- `sssp-modern/bench/results/`: committed benchmark CSV output for the default seed and reference graph families.
- `sssp-modern/bench/figures/`: committed runtime chart artifacts (PNG and PDF) rendered from the benchmark CSV output.
- `sssp-modern/tests/`: pytest coverage, shared fixtures, golden test inputs, oracle comparisons, and dependency-boundary checks for the current Python implementation.
- `sssp-modern/examples/graphs/`: small JSON graph fixtures for manual inspection and IO round-trip tests.
- `sssp-modern/examples/dijkstra/`: sample Dijkstra source-distance output for the tiny directed graph.
- `sssp-modern/examples/astar/`: small grid fixture for A* and Manhattan-heuristic inspection.
- `sssp-modern/papers/`: shared bibliography source (`references.bib`) for the report and presentation, plus the source PDFs of the cited foundational and modern shortest-path papers.
- `sssp-modern/report/`: written report manuscript, including the LaTeX source (`report.tex`), the compiled PDF (`report.pdf`), and the header image asset; the manuscript cites `sssp-modern/papers/references.bib`, embeds the committed runtime chart from `sssp-modern/bench/figures/`, and uses public-facing implementation and validation wording throughout.
- `sssp-modern/presentation/`: UP Beamer presentation source, bibliography, theme assets, logos, and compiled deck PDF; the current deck includes the title/outline spine, problem framing, baseline-algorithm slides, modern directed-sparse SSSP centerpiece slides, benchmark-results slides, reflection and integrity framing, author contributions, references, closing frame, Q&A evidence backup, final copy-fit/layout polish, and public-facing terminology cleanup.
- Dry-run pacing and reproducible submission packaging will expand from this foundation in later versions.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [x] v0.0.1 - Repository bootstrap: governance documents, MIT licensing, and initial project metadata.
- [x] v0.1.0 - Foundation graph and weight primitives with focused pytest coverage.
- [x] v0.1.1 - Graph IO helpers and sample fixtures.
- [x] v0.1.2 - Deterministic random graph generators for benchmark inputs.
- [x] v0.1.3 - Test harness scaffolding and oracle boundaries.
- [x] v0.2.0 - Dijkstra 1959 baseline reference implementation with correctness tests and walkthrough notes.
- [x] v0.2.1 - Bellman-Ford implementation issue artifact and GitHub issue publication.
- [x] v0.2.2 - Thorup implementation issue artifact and GitHub issue publication.
- [x] v0.3.0 - A* and Thorup 1999 reference implementations with heuristic/grid validation and runtime-model caveat.
- [x] v0.3.1 - Bellman-Ford reference implementation with negative-cycle reporting and validation evidence.
- [x] v0.3.2 - Public documentation reconciliation for A*/Thorup release notes, roadmap status, and third-party notices.
- [x] v0.3.3 - Constant-degree graph transformation support for the modern directed-sparse SSSP implementation.
- [x] v0.3.4 - Block-list frontier partitioning support for the modern directed-sparse SSSP implementation.
- [x] v0.3.5 - Bounded pivot selection support following the 2025 sub-`O(m + n log n)` directed-sparse SSSP result.
- [x] v0.3.6 - Recursive bounded multi-source shortest-path support following the 2025 sub-`O(m + n log n)` directed-sparse SSSP result.
- [x] v0.4.0 - Top-level directed-sparse SSSP driver following the 2025 sub-`O(m + n log n)` directed-sparse SSSP result.
- [x] v0.4.1 - Reusable benchmark timing harness with warmup exclusion, setup-outside-timing behavior, median/IQR summaries, and deterministic harness tests.
- [x] v0.4.2 - Deterministic benchmark dataset catalog, cache helpers, JSON graph inputs, and fingerprint validation.
- [x] v0.4.3 - Benchmark result CSV writer, pure-stdlib PNG/PDF runtime chart renderer, DMMSY-vs-Dijkstra runtime sanity check, and DMMSY internal speed work (heap-backed block list, threaded graph-vertex cache, and a documented large-numeric CPython fast path for default-parameter runs).
- [x] v0.5.0 - Written report manuscript completed: experimental evaluation tied to the committed benchmark CSV and runtime chart, honest reflection on the modern algorithm under CPython, AI assistance disclosure, author contributions, and a deduplicated bibliography producing a clean `latexmk` build.
- [x] v0.5.1 - Initial presentation deck scaffold completed: title/outline spine, problem framing, baseline-algorithm slides, references, closing frame, source-paper bibliography entries, and a clean Beamer PDF build.
- [x] v0.5.2 - Presentation modern-algorithm centerpiece completed: DMMSY motivation, architecture, BMSSP recursion, parameter/bound/caveat slides, and a clean 23-page Beamer PDF build.
- [x] v0.5.3 - Presentation results and contribution pass completed: benchmark protocol, runtime chart, Dijkstra-normalized result ratios, reflection/integrity framing, author contributions, Q&A evidence backup, and a clean 26-page Beamer PDF build.
- [x] v0.5.4 - Presentation copy-fit/layout polish completed: title and metadata wrapping, block-heading casing, dense-slide line breaks, diagram-loop cleanup, contribution-slide wrapping, closing contact links, and a clean 26-page Beamer PDF build.
- [x] v0.5.5 - Presentation terminology cleanup completed: speaker notes, caveat language, contribution wording, and Q&A evidence labels now use plain public-facing wording, with a clean 26-page Beamer PDF build.
- [x] v0.5.6 - Written report terminology and layout cleanup completed: report source comments, implementation notes, caveat language, AI-use disclosure, author contributions, and tables now use plain public-facing wording, with a clean 24-page PDF build.
- [x] v0.5.7 - Written report AI assistance disclosure clarified: Claude is identified for planning support and OpenAI Codex GPT 5.5 for programming and implementation assistance, with a rebuilt 24-page PDF.
- [ ] v0.6.0 - Presentation dry-run pacing and reproducible submission packaging.

See the [open issues](https://github.com/zcalifornia-ph/sssp-modern/issues) for proposed features and known gaps.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are welcome, especially around algorithm correctness, complexity-analysis clarity, and reproducible measurement methodology.
See [CONTRIBUTING.md](CONTRIBUTING.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), and [SECURITY.md](SECURITY.md) for process, behavior, and vulnerability reporting.

1. Fork the project.
2. Create your feature branch (`git checkout -b feat/your-feature`).
3. Commit your changes (`git commit -m 'feat: add some feature'`).
4. Push to your branch (`git push origin feat/your-feature`).
5. Open a pull request.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors

<a href="https://github.com/zcalifornia-ph/sssp-modern/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=zcalifornia-ph/sssp-modern" alt="contrib.rocks image" />
</a>

<!-- LICENSE -->
## License

This project is licensed under the MIT License. Copyright is retained by the
named maintainers in [LICENSE.txt](LICENSE.txt).
See [LICENSE.txt](LICENSE.txt) for the full license text and
[THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md) for third-party and adaptation notices.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Maintainers:

- Zildjian E. California - [@zcalifornia-ph](https://github.com/zcalifornia-ph) - <zecalifornia@up.edu.ph>
- Rey Marvin C. Rizal - [@marverickdev](https://github.com/marverickdev) - <rcrizal@up.edu.ph>

Project Link: [https://github.com/zcalifornia-ph/sssp-modern](https://github.com/zcalifornia-ph/sssp-modern)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

- E. W. Dijkstra, whose 1959 note on shortest paths in connected graphs set the baseline for this entire line of work.
- The decades of researchers whose results on heap structures, the word-RAM model, and graph-theoretic preprocessing made the 2025 breakthrough possible.
- The open educational materials and lecture notes on shortest-path algorithms that informed the comparative-analysis structure of this study.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/zcalifornia-ph/sssp-modern.svg?style=for-the-badge
[contributors-url]: https://github.com/zcalifornia-ph/sssp-modern/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/zcalifornia-ph/sssp-modern.svg?style=for-the-badge
[forks-url]: https://github.com/zcalifornia-ph/sssp-modern/network/members
[stars-shield]: https://img.shields.io/github/stars/zcalifornia-ph/sssp-modern.svg?style=for-the-badge
[stars-url]: https://github.com/zcalifornia-ph/sssp-modern/stargazers
[issues-shield]: https://img.shields.io/github/issues/zcalifornia-ph/sssp-modern.svg?style=for-the-badge
[issues-url]: https://github.com/zcalifornia-ph/sssp-modern/issues
[license-shield]: https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge
[license-url]: https://github.com/zcalifornia-ph/sssp-modern/blob/main/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/zcalifornia
[product-screenshot]: repo/images/project_screen.png
