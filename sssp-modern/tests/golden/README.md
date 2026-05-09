# Golden Test Fixtures

This directory stores small deterministic fixtures for algorithm correctness tests.

Current fixtures:

- `tiny-directed.edge-list.json`: a directed weighted graph with vertices `s`, `a`, `b`, and `isolated`.
- `tiny-directed.distances-s.json`: expected shortest-path distances from source `s` for the tiny directed graph.

Golden graph fixtures should use the public JSON fixture formats from `sssp.io` so tests exercise the same loading path as examples and later benchmark inputs.
