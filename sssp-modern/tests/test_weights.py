import operator
from dataclasses import FrozenInstanceError

import pytest

from sssp.weights import Weight


def test_weight_allows_equality_strict_less_than_and_addition() -> None:
    light = Weight(1.5)
    heavy = Weight(2)

    assert light == Weight(1.5)
    assert light == 1.5
    assert light < heavy
    assert light + heavy == Weight(3.5)
    assert light + 2 == Weight(3.5)
    assert 2 + light == Weight(3.5)
    assert (light + heavy).value == 3.5


def test_weight_is_immutable() -> None:
    weight = Weight(3)

    with pytest.raises(FrozenInstanceError):
        weight._value = 4


def test_weight_rejects_non_numeric_values() -> None:
    for value in ("3", object(), True):
        with pytest.raises(TypeError):
            Weight(value)


def test_weight_rejects_forbidden_operations() -> None:
    weight = Weight(3)
    other = Weight(2)
    forbidden_operations = [
        lambda: weight <= other,
        lambda: weight > other,
        lambda: weight >= other,
        lambda: weight - other,
        lambda: other - weight,
        lambda: weight * 2,
        lambda: 2 * weight,
        lambda: weight / 2,
        lambda: 2 / weight,
        lambda: weight // 2,
        lambda: 2 // weight,
        lambda: weight % 2,
        lambda: 2 % weight,
        lambda: weight**2,
        lambda: 2**weight,
        lambda: -weight,
        lambda: +weight,
        lambda: abs(weight),
        lambda: float(weight),
        lambda: int(weight),
        lambda: operator.index(weight),
    ]

    for operation in forbidden_operations:
        with pytest.raises(TypeError):
            operation()


def test_forbidden_operation_guard_can_be_intercepted_with_monkeypatch(monkeypatch) -> None:
    calls = []
    original_sub = Weight.__sub__

    def observed_sub(self, other):
        calls.append((self, other))
        return original_sub(self, other)

    monkeypatch.setattr(Weight, "__sub__", observed_sub)

    with pytest.raises(TypeError):
        Weight(3) - Weight(1)

    assert calls == [(Weight(3), Weight(1))]
