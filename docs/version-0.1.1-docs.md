# Version 0.1.1 Docs

## Quick Diagnostic Read

This release adds graph file IO and sample fixtures on top of the existing graph and weight primitives. It still does not implement the shortest-path algorithms themselves. Its job is to make small graphs portable, reviewable, and reproducible before algorithm modules begin consuming them.

You are ready to use this release if you can:

- run the current pytest suite,
- inspect JSON fixture files,
- reason about whether a serialized graph preserves vertices, edges, directedness, and weights.

## One-Sentence Objective

Add deterministic JSON graph IO so small weighted graph examples can be read, written, tested, and reused by later shortest-path implementations.

## What Changed

Version `v0.1.1` adds:

- `sssp-modern/src/sssp/io.py`
- `sssp-modern/tests/test_io.py`
- `sssp-modern/examples/graphs/tiny-directed.edge-list.json`
- `sssp-modern/examples/graphs/tiny-directed.adjacency-list.json`

The new IO module exposes two fixture families:

- `sssp.edge-list.v1`
- `sssp.adjacency-list.v1`

Both are JSON-backed and implemented with Python's standard library.

## Why It Matters

Shortest-path algorithms need repeatable input graphs. A small fixture format gives the project a stable way to:

- keep sample graphs under version control,
- test graph loading before algorithm logic is added,
- preserve isolated vertices as well as edges,
- compare algorithm outputs against the same known inputs later.

The design deliberately uses JSON instead of a custom whitespace parser. JSON gives structured validation, portable files, and readable fixtures without adding dependencies.

## Format Summary

Edge-list fixtures look like this:

```json
{
  "format": "sssp.edge-list.v1",
  "directed": true,
  "vertices": ["s", "a", "b"],
  "edges": [
    {"source": "s", "target": "a", "weight": 1.0}
  ]
}
```

Adjacency-list fixtures look like this:

```json
{
  "format": "sssp.adjacency-list.v1",
  "directed": true,
  "adjacency": {
    "s": [{"target": "a", "weight": 1.0}],
    "a": [],
    "b": []
  }
}
```

The first implementation supports string vertex identifiers and numeric JSON weights. That keeps fixtures portable and easy to inspect.

## How To Run The Checks

From the nested project directory:

```powershell
cd sssp-modern
$env:PYTHONPATH='src'
python -m pytest tests/test_graph.py tests/test_weights.py tests/test_io.py
```

Expected result:

```text
27 passed
```

For a syntax/import sanity check:

```powershell
python -m compileall src tests
```

## System View

```text
Graph
  -> graph_to_edge_list_data()
  -> write_edge_list()
  -> read_edge_list()
  -> Graph

Graph
  -> graph_to_adjacency_list_data()
  -> write_adjacency_list()
  -> read_adjacency_list()
  -> Graph
```

The key invariant is round-trip equality through the public `Graph` API: directedness, vertex order, isolated vertices, edge order, and numeric weights must survive serialization.

## Validation Summary

The release was validated with:

- edge-list read/write round-trip tests,
- adjacency-list read/write round-trip tests,
- sample fixture loading tests,
- malformed fixture validation tests,
- existing graph and weight tests from the previous foundation release,
- compile check over `src` and `tests`.

## Pitfalls

- Run commands from the nested `sssp-modern/` project directory when executing Python tests.
- Set `PYTHONPATH=src` until package metadata is added.
- Fixture vertices are strings in this release, even though in-memory graphs can use any hashable vertex id.
- Fixture weights are JSON numbers. Do not encode weights as strings.
- The fixture formats are for examples and tests, not for high-volume benchmark storage.

## Next Steps

1. Add deterministic random graph generators.
2. Add broader test harness scaffolding and oracle boundaries.
3. Start the Dijkstra reference implementation on top of the graph and fixture foundation.
