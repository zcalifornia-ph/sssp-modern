"""Weight wrapper for comparison-addition fidelity.

DMMSY 2025 describes the comparison-addition model: edge weights are handled
through comparison and addition operations only. Weight makes that constraint
executable in tests by rejecting unrelated numeric operations.
"""

from __future__ import annotations

from dataclasses import dataclass
from numbers import Real
from typing import Any


@dataclass(frozen=True, slots=True, init=False)
class Weight:
    """Immutable numeric value that permits only `==`, `<`, and `+`."""

    _value: int | float

    def __init__(self, value: int | float) -> None:
        if isinstance(value, bool) or not isinstance(value, Real):
            raise TypeError("Weight value must be an int or float")
        object.__setattr__(self, "_value", value)

    @property
    def value(self) -> int | float:
        """Return the wrapped value for fixtures, reports, and debug output."""

        return self._value

    def __repr__(self) -> str:
        return f"Weight({self._value!r})"

    def __hash__(self) -> int:
        return hash(self._value)

    def __eq__(self, other: object) -> bool:
        other_value = self._coerce(other)
        if other_value is NotImplemented:
            return False
        return self._value == other_value

    def __lt__(self, other: object) -> bool:
        other_value = self._coerce(other)
        if other_value is NotImplemented:
            return NotImplemented
        return self._value < other_value

    def __add__(self, other: object) -> Weight:
        other_value = self._coerce(other)
        if other_value is NotImplemented:
            return NotImplemented
        return Weight(self._value + other_value)

    def __radd__(self, other: object) -> Weight:
        other_value = self._coerce(other)
        if other_value is NotImplemented:
            return NotImplemented
        return Weight(other_value + self._value)

    def __le__(self, other: object) -> bool:
        _forbidden()

    def __gt__(self, other: object) -> bool:
        _forbidden()

    def __ge__(self, other: object) -> bool:
        _forbidden()

    def __sub__(self, other: object) -> Weight:
        _forbidden()

    def __rsub__(self, other: object) -> Weight:
        _forbidden()

    def __mul__(self, other: object) -> Weight:
        _forbidden()

    def __rmul__(self, other: object) -> Weight:
        _forbidden()

    def __truediv__(self, other: object) -> Weight:
        _forbidden()

    def __rtruediv__(self, other: object) -> Weight:
        _forbidden()

    def __floordiv__(self, other: object) -> Weight:
        _forbidden()

    def __rfloordiv__(self, other: object) -> Weight:
        _forbidden()

    def __mod__(self, other: object) -> Weight:
        _forbidden()

    def __rmod__(self, other: object) -> Weight:
        _forbidden()

    def __pow__(self, other: object) -> Weight:
        _forbidden()

    def __rpow__(self, other: object) -> Weight:
        _forbidden()

    def __neg__(self) -> Weight:
        _forbidden()

    def __pos__(self) -> Weight:
        _forbidden()

    def __abs__(self) -> Weight:
        _forbidden()

    def __float__(self) -> float:
        _forbidden()

    def __int__(self) -> int:
        _forbidden()

    def __index__(self) -> int:
        _forbidden()

    @staticmethod
    def _coerce(other: object) -> int | float | Any:
        if isinstance(other, Weight):
            return other._value
        if isinstance(other, bool):
            return NotImplemented
        if isinstance(other, Real):
            return other
        return NotImplemented


def _forbidden() -> None:
    raise TypeError("Weight supports only ==, <, and + in the comparison-addition model")
