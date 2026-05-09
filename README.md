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
    Version: v0.1.2
    <br />
    Status: Foundation implementation (graph primitives, weight checks, IO fixtures, generators, and tests)
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

Planned reference implementations and comparative notes include:

- Dijkstra's algorithm (1959 baseline, binary-heap, and Fibonacci-heap variants).
- Bellman–Ford for context on negative edges and dynamic-programming structure.
- Thorup-style results for integer-weight SSSP under the word-RAM model (reference notes only).
- The 2025 sub-`O(m + n log n)` directed-sparse SSSP result, with implementation following the published structure.

### What sssp-modern Is Not

- Not a production-grade graph library and not a drop-in replacement for established graph frameworks.
- Not a benchmark of real-world routing or network-routing platforms.
- Not a tutorial on graph theory fundamentals; readers are assumed to be comfortable with graphs, asymptotic analysis, and standard data structures.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Status: foundation implementation (`v0.1.2`). The repository now includes the first pure-stdlib Python primitives used by the planned shortest-path implementations: weighted graph structures, a comparison-addition `Weight` wrapper, deterministic JSON graph fixtures, and seeded graph generators for repeatable benchmark inputs.

### Prerequisites

- Git for cloning the repository.
- CPython 3.11 or later.
- `pytest` for the current test suite.

### Quick Start

1. Clone the repo.

   ```sh
   git clone https://github.com/zcalifornia-ph/sssp-modern.git
   cd sssp-modern
   ```

2. Install test tooling if needed.

   ```sh
   python -m pip install pytest
   ```

3. Run the current foundation tests.

   ```sh
   cd sssp-modern
   PYTHONPATH=src python -m pytest tests/test_graph.py tests/test_weights.py tests/test_io.py tests/test_generators.py
   ```

   PowerShell equivalent:

   ```powershell
   cd sssp-modern
   $env:PYTHONPATH='src'
   python -m pytest tests/test_graph.py tests/test_weights.py tests/test_io.py tests/test_generators.py
   ```

4. Review `CHANGELOG.md` for the latest notable changes.
5. Check `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` before opening issues or pull requests.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Repository Layout

The repository keeps governance, supporting assets, and study material in clearly separated trees:

- Root governance files: `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `LICENSE.txt`, and `THIRD-PARTY-NOTICES.md`.
- `docs/`: per-version detail documents tracking what shipped in each release.
- `repo/images/`: repository-owned image assets, including the project screenshot.
- `sssp-modern/src/sssp/`: pure-stdlib Python graph, weight, IO, and generator primitives for reference implementations.
- `sssp-modern/tests/`: pytest coverage for the current Python foundation.
- `sssp-modern/examples/graphs/`: small JSON graph fixtures for manual inspection and IO round-trip tests.
- Algorithm modules, benchmark tooling, and report/deck content will expand from this foundation in later versions.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [x] v0.0.1 - Repository bootstrap: governance documents, MIT licensing, and initial project metadata.
- [x] v0.1.0 - Foundation graph and weight primitives with focused pytest coverage.
- [x] v0.1.1 - Graph IO helpers and sample fixtures.
- [x] v0.1.2 - Deterministic random graph generators for benchmark inputs.
- [ ] v0.1.3 - Test harness scaffolding and oracle boundaries.
- [ ] v0.2.0 - Dijkstra 1959 baseline reference implementation with correctness tests and walkthrough notes.
- [ ] v0.3.0 - Bellman–Ford reference implementation and negative-edge context discussion.
- [ ] v0.4.0 - A* and Thorup reference modules with model-specific notes.
- [ ] v0.5.0 - Reference implementation following the 2025 sub-`O(m + n log n)` directed-sparse SSSP result.
- [ ] v0.6.0 - Comparative complexity analysis artifact tying baseline, intermediate, and modern results together.

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
