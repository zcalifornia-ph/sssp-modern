# Version 0.2.2 Docs

## Quick Diagnostic Read

This release does not add runtime algorithm code. It adds the structured work item that should guide the future Thorup reference implementation and its runtime-model documentation.

You are ready to use this release if you can:

- find the public issue artifact under `sssp-modern/docs/issues/`,
- distinguish issue scoping from implementation work,
- explain why a Python reference implementation should not overstate a word-RAM theoretical bound.

## One-Sentence Objective

Turn the planned Thorup work into an actionable public issue that captures scope, validation, risks, and the required runtime-model caveat before coding begins.

## What Changed

Version `v0.2.2` adds:

- `sssp-modern/docs/issues/issue-feature-w5-s5-1-add-thorup-1999-hierarchical-bucket-sssp.md`
- `docs/version-0.2.2-docs.md`

It also updates:

- `README.md`
- `CHANGELOG.md`

The new issue artifact defines the target for the future Thorup implementation:

- add `src/sssp/thorup99.py`,
- expose `thorup_sssp(graph, source)`,
- restrict the public contract to undirected graphs with non-negative integer weights,
- reject unsupported graph or weight inputs clearly,
- test integer-weight undirected golden cases,
- document the Python runtime-model caveat,
- preserve existing graph and Dijkstra behavior.

## Why It Matters

Thorup's result is important to this study because it introduces model-specific shortest-path ideas for integer-weight graphs. The implementation also carries a high documentation risk: readers must understand that a clear Python reference is not the same as the original word-RAM runtime guarantee.

This release records that risk directly in the issue artifact. The next implementation pass should begin from the issue, then load or create the detailed hierarchy design before writing code.

## System View

```text
current graph foundation
  -> public Thorup issue artifact
  -> GitHub issue #5
  -> future design pass
  -> future implementation and tests
```

The issue is scoped to one implementation surface and its validation path. It does not change graph storage, Dijkstra, benchmark tooling, report content, or presentation content.

## How To Use The Issue

1. Read `sssp-modern/docs/issues/issue-feature-w5-s5-1-add-thorup-1999-hierarchical-bucket-sssp.md`.
2. Resolve the blocking design questions around hierarchy invariants and acceptable integer-weight types.
3. Document the runtime-model caveat before or alongside implementation.
4. Implement only the in-scope module and tests listed in the issue.
5. Run the recommended verification commands from the issue after implementation.
6. Close GitHub issue #5 with a short evidence summary that cites the passing tests.

## Validation Summary

This release validated the issue artifact structure and publication path, not algorithm behavior.

Completed checks:

- local issue artifact created under `sssp-modern/docs/issues/`,
- repository labels verified before GitHub issue creation,
- GitHub issue #5 created with the expected title and labels,
- public docs updated for `v0.2.2`.

Tests were not run for this release because no runtime source code changed.

## Pitfalls

- Do not treat `v0.2.2` as the Thorup implementation release.
- Do not close GitHub issue #5 until source code, tests, and documented verification evidence exist.
- Do not claim Python achieves the original word-RAM bound.
- Do not use third-party shortest-path implementations in runtime source code.
- Do not change Dijkstra or the graph primitives while implementing Thorup unless a separate issue authorizes it.

## Next Steps

1. Resolve the Thorup hierarchy design questions.
2. Implement the Thorup reference module from the published issue.
3. Add integer-weight undirected golden fixtures and tests.
4. Re-run graph, generator, Dijkstra, and import-boundary regression tests after the new module lands.
