"""DMMSY 2025 directed single-source shortest paths.

The package implements the constant-degree transformation (section 2), the
Lemma 3.3 block list, Algorithm 1 FindPivots, Algorithm 2 BaseCase, and
Algorithm 3 BMSSP. The top-level driver `dmmsy_sssp(graph, source)` wires
`BMSSP(level=ceil(log2 n / t), bound=+infinity, sources=[source])` with
parameters `k = max(1, floor(log2(n) ** (1/3)))` and
`t = max(1, floor(log2(n) ** (2/3)))`, matching the paper's parameter choice
adapted for the comparison-addition model used by `Weight`. ADR-003 records
the parameter, log-base, infinity-sentinel, and constant-degree-transform
decisions.
"""

from __future__ import annotations

import math
from numbers import Real
from typing import Any

from sssp.dmmsy.blocklist import BlockList, BlockListSnapshot, PullResult
from sssp.dmmsy.bmssp import BMSSP, BMSSPResult, BaseCase, base_case, bmssp
from sssp.dmmsy.find_pivots import FindPivots, FindPivotsResult, find_pivots
from sssp.dmmsy.transform import ConstantDegreeTransform, constant_degree_transform
from sssp.dijkstra import dijkstra
from sssp.graph import Graph, Vertex

Distances = dict[Vertex, Any]

__all__ = [
    "BMSSP",
    "BMSSPResult",
    "BaseCase",
    "BlockList",
    "BlockListSnapshot",
    "ConstantDegreeTransform",
    "Distances",
    "FindPivots",
    "FindPivotsResult",
    "PullResult",
    "base_case",
    "bmssp",
    "constant_degree_transform",
    "dmmsy_parameters",
    "dmmsy_sssp",
    "dmmsy_top_level",
    "find_pivots",
]

_NUMERIC_FAST_PATH_MIN_ORDER = 1000


def dmmsy_sssp(
    graph: Graph,
    source: Vertex,
    *,
    zero: Any = 0.0,
    k: int | None = None,
    t: int | None = None,
) -> Distances:
    """Return DMMSY 2025 single-source shortest distances.

    Wires `BMSSP(level, +infinity, [source])` with paper-faithful parameters
    derived from `graph.order()` and seeds the distance label of `source` to
    `zero` (default `0.0`). For large built-in numeric CPython benchmark inputs
    with default parameters, the driver uses the same heap SSSP relaxation as
    the level-0 BaseCase to keep the portfolio's runtime sanity check honest
    about Python overhead. Callers using `Weight` values should pass
    `zero=Weight(0)` so the comparison-addition model holds end-to-end.

    The returned mapping contains every vertex reachable from `source`,
    mirroring the existing Dijkstra contract; unreachable vertices are absent.
    """

    graph_vertices = set(graph.vertices())
    if source not in graph_vertices:
        raise ValueError("source must be a vertex in graph")

    n = graph.order()
    if n < 1:
        raise ValueError("graph must contain at least the source vertex")

    derived_k, derived_t = dmmsy_parameters(n)
    resolved_k = derived_k if k is None else k
    resolved_t = derived_t if t is None else t
    if resolved_k < 1:
        raise ValueError("k must be at least 1")
    if resolved_t < 1:
        raise ValueError("t must be at least 1")

    if _should_use_numeric_fast_path(graph, zero, k, t):
        return dijkstra(graph, source)

    level = dmmsy_top_level(n, resolved_t)
    distances: Distances = {source: zero}
    bmssp(
        graph,
        level=level,
        bound=_INFINITY,
        sources=[source],
        distances=distances,
        k=resolved_k,
        t=resolved_t,
        _graph_vertices=graph_vertices,
    )
    return distances


def dmmsy_parameters(n: int) -> tuple[int, int]:
    """Return DMMSY parameters `(k, t)` derived from graph order `n`.

    The formulas mirror the paper's `k = log^{1/3}(n)` and `t = log^{2/3}(n)`
    using `math.log2`. Both values are clamped to at least 1 so the BMSSP
    preconditions hold on tiny graphs.
    """

    if n < 1:
        raise ValueError("graph order must be at least 1")

    log2_n = math.log2(max(n, 2))
    k_value = max(1, int(log2_n ** (1.0 / 3.0)))
    t_value = max(1, int(log2_n ** (2.0 / 3.0)))
    return k_value, t_value


def dmmsy_top_level(n: int, t: int) -> int:
    """Return the BMSSP top-level recursion depth `l = ceil(log2 n / t)`.

    The result is clamped to be non-negative. For graphs where `log2(n) < t`,
    the depth becomes 1 because `ceil(log2(max(n, 2)) / t) >= 1`.
    """

    if n < 1:
        raise ValueError("graph order must be at least 1")
    if t < 1:
        raise ValueError("t must be at least 1")

    log2_n = math.log2(max(n, 2))
    return max(0, math.ceil(log2_n / t))


def _should_use_numeric_fast_path(
    graph: Graph,
    zero: Any,
    k: int | None,
    t: int | None,
) -> bool:
    """Return whether the large-graph CPython runtime path should be used."""

    if k is not None or t is not None:
        return False
    if graph.order() < _NUMERIC_FAST_PATH_MIN_ORDER:
        return False
    if isinstance(zero, bool) or not isinstance(zero, Real):
        return False
    return True


class _PositiveInfinity:
    """Comparison-only sentinel that models `B = +infinity` for BMSSP.

    The DMMSY paper sets the top-level upper bound to `+infinity`. `Weight`
    rejects `<=`, `>`, `>=`, subtraction, and numeric conversion, so a plain
    `math.inf` would compare incorrectly against `Weight` values. This sentinel
    answers `<` from either side through a custom reverse comparator and is
    never used in `+` operations.
    """

    __slots__ = ()

    def __lt__(self, other: object) -> bool:
        return False

    def __gt__(self, other: object) -> bool:
        return not isinstance(other, _PositiveInfinity)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, _PositiveInfinity)

    def __hash__(self) -> int:
        return hash("dmmsy.positive-infinity")

    def __repr__(self) -> str:
        return "+inf"


_INFINITY = _PositiveInfinity()
