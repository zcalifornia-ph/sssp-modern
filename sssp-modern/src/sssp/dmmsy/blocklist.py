"""Block-list data structure from DMMSY 2025 Lemma 3.3.

The structure stores key/value distance labels in two ordered block sequences:
`D0` receives `BatchPrepend` records whose values are smaller than the current
minimum, and `D1` receives ordinary `Insert` records routed by per-block upper
bounds. `Pull` removes at most `M` smallest labels and returns the next
separating bound for BMSSP recursion.

The paper implements the upper-bound index with a Red-Black tree. This
portfolio implementation keeps the same block invariants with a stdlib
list-backed index so the later BMSSP code can depend on the Lemma 3.3
operation contract without adding a separate tree implementation.
"""

from __future__ import annotations

from collections.abc import Hashable, Iterable
from dataclasses import dataclass
from typing import Any

Key = Hashable
Pair = tuple[Key, Any]


@dataclass(frozen=True, slots=True)
class PullResult:
    """Result of `BlockList.pull()`."""

    keys: tuple[Key, ...]
    pairs: tuple[Pair, ...]
    bound: Any


@dataclass(frozen=True, slots=True)
class BlockListSnapshot:
    """Immutable debug view used by invariant tests."""

    size: int
    d0_blocks: tuple[tuple[Pair, ...], ...]
    d1_blocks: tuple[tuple[Pair, ...], ...]
    d1_upper_bounds: tuple[Any, ...]
    insert_operations: int
    batch_prepend_operations: int
    pull_operations: int
    max_inserts: int | None


@dataclass(slots=True)
class _Entry:
    key: Key
    value: Any
    serial: int


@dataclass(slots=True)
class _Block:
    entries: list[_Entry]

    def upper_bound(self) -> Any:
        return self.entries[-1].value


@dataclass(slots=True)
class _Location:
    sequence: str
    block: _Block
    entry: _Entry


class BlockList:
    """Mutable block-list for DMMSY BMSSP frontier partitioning.

    Parameters:
    - `block_size` is the paper's `M` and must be at least 1.
    - `upper_bound` is the paper's bound `B`, returned by `pull()` when the
      data structure becomes empty.
    - `max_inserts` records the paper's `N` for diagnostics; this implementation
      does not need it to enforce correctness.

    Values must support strict less-than and equality. No arithmetic or
    non-strict comparison is used, preserving compatibility with `Weight`.
    """

    def __init__(
        self,
        block_size: int,
        upper_bound: Any,
        max_inserts: int | None = None,
    ) -> None:
        if block_size < 1:
            raise ValueError("block_size must be at least 1")
        if max_inserts is not None and max_inserts < 0:
            raise ValueError("max_inserts must be non-negative")

        self._block_size = block_size
        self._upper_bound = upper_bound
        self._max_inserts = max_inserts
        self._d0: list[_Block] = []
        self._d1: list[_Block] = []
        self._locations: dict[Key, _Location] = {}
        self._serial = 0
        self._insert_operations = 0
        self._batch_prepend_operations = 0
        self._pull_operations = 0

    @property
    def block_size(self) -> int:
        """Return the configured maximum live entries per block."""

        return self._block_size

    def __len__(self) -> int:
        return len(self._locations)

    def is_empty(self) -> bool:
        """Return whether no live key/value pairs remain."""

        return not self._locations

    def insert(self, key: Key, value: Any) -> bool:
        """Insert or improve one key/value pair in `D1`.

        Returns `True` when the live structure changed. If `key` already has a
        value that is smaller than or equal to `value`, the call is ignored and
        returns `False`.
        """

        self._insert_operations += 1
        if not self._should_replace(key, value):
            return False

        self._remove_key(key)
        entry = self._new_entry(key, value)
        block = self._find_d1_block(value)
        block.entries.append(entry)
        _sort_entries(block.entries)
        self._locations[key] = _Location("D1", block, entry)

        if len(block.entries) > self._block_size:
            self._split_d1_block(block)
        return True

    def batch_prepend(self, pairs: Iterable[Pair]) -> int:
        """Prepend lower-than-current key/value pairs to `D0`.

        All retained incoming values must be strictly smaller than the current
        minimum live value. Duplicate incoming keys are coalesced by keeping the
        smallest value. The return value is the number of live keys inserted or
        improved.
        """

        self._batch_prepend_operations += 1
        candidates = self._retained_candidates(tuple(pairs))
        if not candidates:
            return 0

        current_minimum = self._minimum_value()
        if current_minimum is not None:
            for _, value in candidates:
                if not _less(value, current_minimum):
                    raise ValueError(
                        "batch-prepended values must be smaller than the current minimum"
                    )

        for key, _ in candidates:
            self._remove_key(key)

        entries = [self._new_entry(key, value) for key, value in candidates]
        _sort_entries(entries)
        new_blocks = [
            _Block(entries[index : index + self._block_size])
            for index in range(0, len(entries), self._block_size)
        ]
        self._d0 = new_blocks + self._d0

        for block in new_blocks:
            for entry in block.entries:
                self._locations[entry.key] = _Location("D0", block, entry)
        return len(entries)

    def pull(self) -> PullResult:
        """Remove and return at most `M` smallest keys plus the next bound."""

        self._pull_operations += 1
        if not self._locations:
            return PullResult((), (), self._upper_bound)

        selected = self._ordered_entries()[: self._block_size]
        for entry in selected:
            self._remove_key(entry.key)

        bound = self._minimum_value()
        if bound is None:
            bound = self._upper_bound

        pairs = tuple((entry.key, entry.value) for entry in selected)
        return PullResult(tuple(entry.key for entry in selected), pairs, bound)

    def snapshot(self) -> BlockListSnapshot:
        """Return immutable block and counter state for tests and traceability."""

        return BlockListSnapshot(
            size=len(self),
            d0_blocks=_snapshot_blocks(self._d0),
            d1_blocks=_snapshot_blocks(self._d1),
            d1_upper_bounds=tuple(block.upper_bound() for block in self._d1),
            insert_operations=self._insert_operations,
            batch_prepend_operations=self._batch_prepend_operations,
            pull_operations=self._pull_operations,
            max_inserts=self._max_inserts,
        )

    def Insert(self, key: Key, value: Any) -> bool:
        """Paper-named wrapper for `insert`."""

        return self.insert(key, value)

    def BatchPrepend(self, pairs: Iterable[Pair]) -> int:
        """Paper-named wrapper for `batch_prepend`."""

        return self.batch_prepend(pairs)

    def Pull(self) -> PullResult:
        """Paper-named wrapper for `pull`."""

        return self.pull()

    def _should_replace(self, key: Key, value: Any) -> bool:
        location = self._locations.get(key)
        if location is None:
            return True
        return _less(value, location.entry.value)

    def _retained_candidates(self, pairs: tuple[Pair, ...]) -> list[Pair]:
        retained: dict[Key, Any] = {}
        for key, value in pairs:
            if key not in retained or _less(value, retained[key]):
                retained[key] = value

        candidates = [
            (key, value)
            for key, value in retained.items()
            if self._should_replace(key, value)
        ]
        candidates.sort(key=lambda pair: (pair[1], repr(pair[0])))
        return candidates

    def _new_entry(self, key: Key, value: Any) -> _Entry:
        entry = _Entry(key, value, self._serial)
        self._serial += 1
        return entry

    def _find_d1_block(self, value: Any) -> _Block:
        for block in self._d1:
            if not _less(block.upper_bound(), value):
                return block

        if self._d1:
            return self._d1[-1]

        block = _Block([])
        self._d1.append(block)
        return block

    def _split_d1_block(self, block: _Block) -> None:
        index = self._d1.index(block)
        _sort_entries(block.entries)
        split_at = (len(block.entries) + 1) // 2
        left = _Block(block.entries[:split_at])
        right = _Block(block.entries[split_at:])
        self._d1[index : index + 1] = [left, right]

        for replacement in (left, right):
            for entry in replacement.entries:
                self._locations[entry.key] = _Location("D1", replacement, entry)

    def _remove_key(self, key: Key) -> bool:
        location = self._locations.pop(key, None)
        if location is None:
            return False

        location.block.entries.remove(location.entry)
        if location.block.entries:
            return True

        sequence = self._d0 if location.sequence == "D0" else self._d1
        sequence.remove(location.block)
        return True

    def _minimum_value(self) -> Any | None:
        ordered = self._ordered_entries()
        if not ordered:
            return None
        return ordered[0].value

    def _ordered_entries(self) -> list[_Entry]:
        entries = [location.entry for location in self._locations.values()]
        _sort_entries(entries)
        return entries


def _sort_entries(entries: list[_Entry]) -> None:
    entries.sort(key=lambda entry: (entry.value, entry.serial))


def _less(left: Any, right: Any) -> bool:
    return bool(left < right)


def _snapshot_blocks(blocks: list[_Block]) -> tuple[tuple[Pair, ...], ...]:
    return tuple(
        tuple((entry.key, entry.value) for entry in block.entries)
        for block in blocks
    )
