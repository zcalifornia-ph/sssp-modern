# Contributing

Thanks for your interest in contributing to `sssp-modern`.
This guide follows values of quality, integrity, inclusion, collaboration, service, and continuous improvement.

## Values Framework

Contributions should align with these working values:

- leadership through transparent, constructive collaboration
- professionalism through ethical practice and academic integrity
- expertise through strong technical and domain quality
- inquiry through evidence, testing, and open learning
- service through useful outcomes for communities and users
- diversity through inclusive and rights-respecting participation
- collaboration through interdisciplinary and cross-functional teamwork
- sustainability through maintainable and responsible engineering

## Before You Start

- Review open issues and pull requests to avoid duplicate work.
- Open an issue first for significant changes to align scope and approach.
- Keep changes focused and easy to review.
- Confirm your contribution aligns with `CODE_OF_CONDUCT.md` and `SECURITY.md`.
- For algorithm work, cite the original paper or source whenever a reference implementation tracks a specific published result.

## Contribution Standards

- Quality: include tests, validation, or clear verification steps. Reference implementations should ship with correctness tests against small hand-checkable instances before any larger benchmarking effort.
- Integrity: provide accurate claims, reproducible evidence, and proper attribution. Complexity claims should specify the model of computation (e.g., comparison-based, word-RAM) and the assumed weight model.
- Inclusion: write docs and comments for broad readability and accessibility. Prefer clarity over micro-optimized cleverness in study material.
- Service: prioritize improvements that deliver real learning and reference value to readers studying SSSP.
- Sustainability: prefer maintainable solutions over short-lived complexity.

## Development Workflow

1. Fork and create a branch from `main`.
2. Implement the change with tests and documentation updates where applicable.
3. Run project checks locally for the implementation language(s) you touched.
4. Open a pull request containing:
   - problem statement
   - approach summary
   - validation evidence (test output, logs, screenshots)
   - risks, tradeoffs, and rollback notes when relevant

## Branch Naming

- Use kebab-case.
- Start with a Conventional Commit type.
- Keep names concise and descriptive.

Example:

```text
feat/dijkstra-binary-heap-baseline
```

## Commit Conventions

Use Conventional Commits.
Examples:

```text
feat: add binary-heap Dijkstra reference implementation
fix: correct relaxation order in Bellman-Ford reference
docs: clarify weight-model assumptions in complexity notes
```

Common types:

- `feat`
- `fix`
- `docs`
- `refactor`
- `test`
- `chore`

## Merge Strategy

Use short-lived branches and squash before merge, unless project maintainers specify otherwise.

- Keep each pull request scoped to one logical change.
- Use a final squashed commit message that clearly describes the full change.
- Ensure branch checks pass before merge.

## Security Reporting

Do not report vulnerabilities in public issues.
Follow `SECURITY.md` for coordinated disclosure.

## Community Conduct

Participation requires compliance with `CODE_OF_CONDUCT.md`.
