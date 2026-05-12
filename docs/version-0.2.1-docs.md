# Version 0.2.1 Docs

## Quick Diagnostic Read

This release does not add runtime algorithm code. It adds the structured work item that should guide the next implementation pass for Bellman-Ford and its negative-cycle report behavior.

You are ready to use this release if you can:

- find the public issue artifact under `sssp-modern/docs/issues/`,
- distinguish issue scoping from implementation work,
- use acceptance criteria as a checklist before coding.

## One-Sentence Objective

Turn the planned Bellman-Ford work into an actionable, public issue that a human maintainer or coding agent can implement and verify without guessing the scope.

## What Changed

Version `v0.2.1` adds:

- `sssp-modern/docs/issues/issue-feature-w3-s3-1-add-classic-bellman-ford-with-negative-cycle-report.md`
- `docs/version-0.2.1-docs.md`

It also updates:

- `README.md`
- `CHANGELOG.md`

The new issue artifact defines the target for the upcoming Bellman-Ford implementation:

- add `src/sssp/bellman_ford.py`,
- expose `bellman_ford(graph, source)`,
- return distances plus an explicit negative-cycle report,
- test golden shortest-path behavior,
- test curated negative-cycle cases,
- keep production imports standard-library or local package only,
- preserve existing Dijkstra behavior.

## Why It Matters

Bellman-Ford is the next reference algorithm after Dijkstra because it covers negative-edge handling and establishes the negative-cycle semantics that later discussion and comparisons will need.

This release keeps the repository honest: it records the implementation target, evidence, tests, risks, and non-goals before source code changes begin. That makes the next coding pass easier to review and less likely to drift into unrelated algorithm or report work.

## System View

```text
current graph foundation
  -> public Bellman-Ford issue artifact
  -> GitHub issue #4
  -> future implementation and tests
```

The issue is intentionally scoped to one implementation surface and its validation path. It does not change the graph model, Dijkstra baseline, benchmark harness, report, or presentation content.

## How To Use The Issue

1. Read `sssp-modern/docs/issues/issue-feature-w3-s3-1-add-classic-bellman-ford-with-negative-cycle-report.md`.
2. Confirm the scope and acceptance criteria still match the desired Bellman-Ford behavior.
3. Implement only the in-scope files and tests listed in the issue.
4. Run the recommended verification commands from the issue after implementation.
5. Close the GitHub issue with a short evidence summary that cites the passing tests.

## Validation Summary

This release validated the issue artifact structure and publication path, not algorithm behavior.

Completed checks:

- local issue artifact created under `sssp-modern/docs/issues/`,
- repository labels verified before GitHub issue creation,
- GitHub issue #4 created with the expected title and labels,
- public docs updated for `v0.2.1`.

Tests were not run for this release because no runtime source code changed.

## Pitfalls

- Do not treat `v0.2.1` as the Bellman-Ford implementation release.
- Do not close GitHub issue #4 until source code, tests, and documented verification evidence exist.
- Do not use third-party shortest-path implementations in runtime source code.
- Do not change Dijkstra behavior while implementing Bellman-Ford unless a separate issue authorizes it.

## Next Steps

1. Implement Bellman-Ford from the published issue.
2. Add tests for no-cycle negative-edge graphs and reachable negative cycles.
3. Re-run Dijkstra regression tests after the new module lands.
4. Use the passing evidence to prepare the next implementation release.
