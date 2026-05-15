from __future__ import annotations

import random

import pytest

from sssp.dmmsy import BlockList
from sssp.weights import Weight


def test_insert_keeps_smallest_value_for_duplicate_key() -> None:
    blocklist = BlockList(block_size=2, upper_bound=99)

    assert blocklist.insert("a", 5)
    assert not blocklist.insert("a", 7)
    assert blocklist.insert("a", 3)

    result = blocklist.pull()

    assert result.keys == ("a",)
    assert result.pairs == (("a", 3),)
    assert result.bound == 99
    assert blocklist.is_empty()


def test_batch_prepend_requires_values_before_current_minimum() -> None:
    blocklist = BlockList(block_size=2, upper_bound=99)
    blocklist.insert("c", 10)

    with pytest.raises(ValueError, match="smaller than the current minimum"):
        blocklist.batch_prepend([("bad", 12)])

    assert blocklist.BatchPrepend([("a", 1), ("b", 2), ("a", 3)]) == 2

    first = blocklist.Pull()
    second = blocklist.Pull()

    assert first.pairs == (("a", 1), ("b", 2))
    assert first.bound == 10
    assert second.pairs == (("c", 10),)
    assert second.bound == 99


def test_pull_returns_smallest_keys_and_next_bound() -> None:
    blocklist = BlockList(block_size=2, upper_bound=99)
    blocklist.Insert("a", 4)
    blocklist.Insert("b", 1)
    blocklist.Insert("c", 3)

    first = blocklist.Pull()
    second = blocklist.Pull()
    empty = blocklist.Pull()

    assert first.keys == ("b", "c")
    assert first.pairs == (("b", 1), ("c", 3))
    assert first.bound == 4
    assert second.pairs == (("a", 4),)
    assert second.bound == 99
    assert empty.pairs == ()
    assert empty.bound == 99


def test_blocklist_fuzz_matches_sorted_reference() -> None:
    block_size = 4
    blocklist = BlockList(block_size=block_size, upper_bound=10_000)
    reference: dict[str, int] = {}
    rng = random.Random(20250515)
    used_values: set[int] = set()

    for step in range(120):
        operation = rng.choice(("insert", "insert", "batch", "pull"))

        if operation == "insert":
            key = f"k{rng.randrange(12)}"
            value = _unused_value(used_values, rng.randrange(0, 500) + step * 10)
            changed = blocklist.insert(key, value)
            expected_changed = key not in reference or value < reference[key]
            assert changed is expected_changed
            if expected_changed:
                reference[key] = value
        elif operation == "batch":
            minimum = min(reference.values()) if reference else 500
            pairs = []
            for offset in range(rng.randrange(1, 5)):
                key = f"k{rng.randrange(12)}"
                value = _unused_value(used_values, minimum - 10 - step * 5 - offset)
                pairs.append((key, value))

            changed = blocklist.batch_prepend(pairs)
            expected = _apply_batch_reference(reference, pairs)
            assert changed == expected
        else:
            result = blocklist.pull()
            expected_pairs = tuple(
                sorted(reference.items(), key=lambda item: item[1])[:block_size]
            )
            assert result.pairs == expected_pairs
            for key, _ in expected_pairs:
                reference.pop(key)
            expected_bound = min(reference.values()) if reference else 10_000
            assert result.bound == expected_bound

        _assert_snapshot_matches_reference(blocklist, reference)


def test_blocklist_snapshot_preserves_block_invariants() -> None:
    blocklist = BlockList(block_size=3, upper_bound=99, max_inserts=20)
    for value in range(10):
        blocklist.insert(f"k{value}", value)

    snapshot = blocklist.snapshot()

    assert snapshot.size == 10
    assert snapshot.max_inserts == 20
    assert all(len(block) <= 3 for block in snapshot.d1_blocks)
    assert len(snapshot.d1_blocks) <= 2 * ((snapshot.size + 2) // 3)
    assert snapshot.insert_operations == 10


def test_blocklist_accepts_weight_values_without_forbidden_operations() -> None:
    blocklist = BlockList(block_size=2, upper_bound=Weight(100))

    assert blocklist.insert("mid", Weight(5))
    assert blocklist.insert("low", Weight(3))
    assert not blocklist.insert("mid", Weight(8))
    assert blocklist.batch_prepend([("front", Weight(1))]) == 1

    first = blocklist.pull()
    second = blocklist.pull()

    assert first.pairs == (("front", Weight(1)), ("low", Weight(3)))
    assert first.bound == Weight(5)
    assert second.pairs == (("mid", Weight(5)),)
    assert second.bound == Weight(100)


def _unused_value(used_values: set[int], candidate: int) -> int:
    while candidate in used_values:
        candidate += 1
    used_values.add(candidate)
    return candidate


def _apply_batch_reference(reference: dict[str, int], pairs: list[tuple[str, int]]) -> int:
    retained: dict[str, int] = {}
    for key, value in pairs:
        if key not in retained or value < retained[key]:
            retained[key] = value

    changed = 0
    for key, value in retained.items():
        if key not in reference or value < reference[key]:
            reference[key] = value
            changed += 1
    return changed


def _assert_snapshot_matches_reference(
    blocklist: BlockList,
    reference: dict[str, int],
) -> None:
    snapshot = blocklist.snapshot()
    live_pairs = [
        pair
        for block in snapshot.d0_blocks + snapshot.d1_blocks
        for pair in block
    ]

    assert snapshot.size == len(reference)
    assert len(live_pairs) == len(reference)
    assert {key for key, _ in live_pairs} == set(reference)
    assert dict(live_pairs) == reference
    assert all(len(block) <= blocklist.block_size for block in snapshot.d0_blocks)
    assert all(len(block) <= blocklist.block_size for block in snapshot.d1_blocks)
