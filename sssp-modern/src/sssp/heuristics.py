"""Heuristics for A* shortest-path search.

Hart, Nilsson, and Raphael 1968 define A* around an estimate `h` of remaining
cost. This module keeps the B4.1 heuristic surface explicit: `zero` for
Dijkstra-equivalence checks and `manhattan` for 4-connected grid demos.
"""

from __future__ import annotations

from numbers import Real

from sssp.graph import Vertex

GridPoint = tuple[Real, Real]


def zero(vertex: Vertex, goal: Vertex) -> float:
    """Return the identically-zero heuristic for any vertex-goal pair."""

    return 0.0


def manhattan(vertex: GridPoint, goal: GridPoint) -> float:
    """Return Manhattan distance between two 2D grid points.

    The heuristic is admissible and consistent for unit-cost 4-connected grids.
    """

    x1, y1 = _require_grid_point(vertex, "vertex")
    x2, y2 = _require_grid_point(goal, "goal")
    return float(abs(x1 - x2) + abs(y1 - y2))


def _require_grid_point(value: object, name: str) -> GridPoint:
    if not isinstance(value, tuple):
        raise TypeError(f"{name} must be a 2D grid point tuple")
    if len(value) != 2:
        raise TypeError(f"{name} must have exactly two coordinates")

    x, y = value
    if isinstance(x, bool) or isinstance(y, bool) or not isinstance(x, Real) or not isinstance(y, Real):
        raise TypeError(f"{name} coordinates must be real numbers")
    return x, y
