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
    Version: v0.4.1
    <br />
    Status: Dijkstra, Bellman-Ford, A*, Thorup, and the modern directed-sparse SSSP driver are in place; reusable benchmark timing support is now available
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

Status: Dijkstra, Bellman-Ford, A*, Thorup, and the modern directed-sparse SSSP driver are implemented (`v0.4.1`). The repository now includes pure-stdlib Python graph primitives, a comparison-addition `Weight` wrapper, deterministic JSON graph fixtures, seeded graph generators, reusable pytest scaffolding, a binary-heap Dijkstra baseline, a Bellman-Ford implementation with negative-cycle reporting, an A* implementation with reusable heuristics, a Thorup-style hierarchical bucket reference for undirected integer-weight graphs, the top-level driver for the modern directed-sparse SSSP implementation, and a reusable benchmark timing harness for the upcoming empirical comparison work.

### Prerequisites

- Git for cloning the repository.
- CPython 3.11 or later.
- `pytest` for the current test suite.
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

12. Review `CHANGELOG.md` for the latest notable changes.
13. Check `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` before opening issues or pull requests.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Repository Layout

The repository keeps governance, supporting assets, and study material in clearly separated trees:

- Root governance files: `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `LICENSE.txt`, and `THIRD-PARTY-NOTICES.md`.
- `docs/`: per-version detail documents tracking what shipped in each release.
- `repo/images/`: repository-owned image assets, including the project screenshot.
- `sssp-modern/docs/issues/`: structured issue artifacts that capture scoped implementation work before coding begins.
- `sssp-modern/src/sssp/`: pure-stdlib Python graph, weight, IO, generator, Dijkstra, Bellman-Ford, A*, Thorup, and modern directed-sparse SSSP support modules.
- `sssp-modern/src/sssp/dmmsy/`: the 2025 directed-sparse SSSP implementation, including the constant-degree graph transformation, block-list frontier partitioning data structure, bounded pivot-selection helper, recursive bounded multi-source shortest-path routine, and the top-level public driver `dmmsy_sssp(graph, source)` with paper-faithful parameter wiring.
- `sssp-modern/src/bench/`: reusable benchmark timing harness that records warmup-excluded runtime samples, medians, and interquartile ranges for later CSV and chart generation.
- `sssp-modern/tests/`: pytest coverage, shared fixtures, golden test inputs, oracle comparisons, and dependency-boundary checks for the current Python implementation.
- `sssp-modern/examples/graphs/`: small JSON graph fixtures for manual inspection and IO round-trip tests.
- `sssp-modern/examples/dijkstra/`: sample Dijkstra source-distance output for the tiny directed graph.
- `sssp-modern/examples/astar/`: small grid fixture for A* and Manhattan-heuristic inspection.
- Benchmark datasets, CSV/chart output, and report/deck content will expand from this foundation in later versions.

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
- [ ] v0.5.0 - Benchmark dataset suite, result CSV, chart generation, and comparative complexity analysis artifact tying baseline, intermediate, and modern results together.
- [ ] v0.6.0 - Report and presentation completion with reproducible submission packaging.

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
