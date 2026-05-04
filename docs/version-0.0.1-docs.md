# Version 0.0.1 Bootstrap

## Title

`sssp-modern` v0.0.1 Repository Bootstrap

## Quick Diagnostic Read

You are likely ready to use this release if you can:

- read project `README` files,
- understand the difference between a permissive and copyleft open-source license,
- run `git clone` and inspect a repository.

What is new (and high-value) in this version:

- a complete first-pass set of root governance documents,
- an explicit MIT License with copyright retained by the named maintainers,
- a third-party notices file aligned with the chosen license,
- the supporting screenshot asset referenced by the `README` hero image.

## One-Sentence Objective

Establish a clean, legible, and license-clear public surface for the `sssp-modern` study repository so that contributors and readers can orient quickly before reference implementations land.

## Why This Version Matters

`sssp-modern` is a study repository whose intended audience is readers and contributors interested in the single-source shortest-path problem and its modern complexity story. Before any reference implementation lands, the public surface needs to:

- explain what the project is and is not,
- spell out who the maintainers are,
- declare a license with clear copyright handling,
- describe contribution and security expectations,
- give a stable starting point for changelog discipline.

`v0.0.1` is the version that establishes all of those. Future releases can add reference implementations against a known, license-clear baseline rather than mixing governance work into algorithm pull requests.

## What Shipped (Artifact Map)

- `README.md`: hero block, project description, scope, planned algorithms, repository layout, roadmap, contributing pointer, MIT license shield, contact, and acknowledgments.
- `CHANGELOG.md`: bootstrap entry for `v0.0.1` and the baseline structure for future release notes.
- `CODE_OF_CONDUCT.md`: independent community policy with maintainer-direct reporting addresses.
- `CONTRIBUTING.md`: contributor onboarding, including algorithm/complexity-study standards, branch naming, and Conventional Commits guidance.
- `SECURITY.md`: coordinated-disclosure policy with maintainer-direct reporting addresses and a pre-1.0 supported-versions table.
- `LICENSE.txt`: MIT License text with copyright retained by the named maintainers.
- `THIRD-PARTY-NOTICES.md`: declares MIT distribution for repository-owned material and preserves attribution for the third-party MIT-derived reference materials retained in this repository.
- `repo/images/project_screen.png`: project screenshot referenced at the top of `README.md`.
- `docs/version-0.0.1-docs.md`: this detail document.

## License Selection Rationale

The MIT License was chosen from the open-source family because:

- it is permissive and broadly compatible with educational and research distribution,
- copyright is explicitly retained on the named authors via the `Copyright (c) <year> <copyright holders>` line, satisfying the maintainers' wish to retain copyright,
- it has minimal ceremony — no `NOTICE`-file or trademark-clause maintenance burden during the study phase,
- it is the most widely understood open-source license for academic and study reference implementations.

Apache-2.0 and BSD-3-Clause were considered. Both would have worked but added clauses (patent grant or non-endorsement) that did not match a clear need at this stage. The license body text was used unmodified except for the standard `<year>` and `<copyright holders>` substitutions.

## Walkthrough: How to Read This Release

For a first-time reader of the repository at this version:

1. Read `README.md` end to end. Pay attention to the **Scope**, **Algorithms In Scope**, and **What sssp-modern Is Not** sections — these define what the study covers.
2. Read `CHANGELOG.md` to confirm you are looking at the bootstrap version.
3. Read `LICENSE.txt` to understand reuse terms.
4. Read `CODE_OF_CONDUCT.md` and `CONTRIBUTING.md` if you intend to contribute.
5. Read `SECURITY.md` if you intend to report a vulnerability.
6. Read `THIRD-PARTY-NOTICES.md` to understand the third-party-material posture.

## Pitfalls

### 1) Expecting code to run

`v0.0.1` is governance only. There are no reference implementations in this version. Trying to compile or run something now will fail because there is nothing yet to run.

### 2) Conflating "study repository" with "graph library"

This is not a graph library. It is a study repository. Reuse the algorithms when they land, but do not import this as a runtime dependency.

### 3) License-mixing without notices updates

When new third-party material is introduced in a future version, attribution must be added to `THIRD-PARTY-NOTICES.md` and any included license text retained alongside the borrowed file. The MIT terms in `LICENSE.txt` do not relicense third-party material.

## Skill Transfer: What You Should Internalize

After this version, you should be able to:

1. Explain why a study repository deserves the same governance discipline as a production project.
2. Choose a permissive open-source license that retains author copyright and justify the choice in writing.
3. Identify which root files are public-facing governance and what each one is for.
4. Maintain a clean changelog for a pre-1.0 study repository.

## Mini Competency Map (For This Topic)

- Level 1: Can navigate the repository and explain what each governance file is for.
- Level 2: Can explain why MIT was chosen over other open-source licenses for this project.
- Level 3: Can extend the governance files when a new third-party component is added without breaking license consistency.
- Level 4: Can mentor another contributor through opening their first pull request to this repository.

## 24-72 Hour Next Steps

1. Decide on the implementation language for the Dijkstra 1959 baseline (`v0.1.0`). A single language for the first reference is recommended; comparative implementations can follow in later versions.
2. Sketch the directory layout you want for reference implementations (e.g., one directory per algorithm, with its own README and tests).
3. Identify a small, hand-checkable graph instance to use as a smoke test across all future implementations.
4. Open issues for the `v0.1.0` milestone using the planned algorithm list in the `README` roadmap as a backbone.

---

This document is intentionally light on code: there is no code yet. Once `v0.1.0` lands, version docs will start tracking implementation walkthroughs alongside any further governance changes.
