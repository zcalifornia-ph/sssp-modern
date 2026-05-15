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

import heapq
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


@dataclass(frozen=True, slots=True)
class _HeapEntry:
    value: Any
    serial: int
    key: Key


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
        self._values: dict[Key, Any] = {}
        self._heap: list[tuple[Any, int, Key]] = []
        self._serial = 0
        self._insert_operations = 0
        self._batch_prepend_operations = 0
        self._pull_operations = 0

    @property
    def block_size(self) -> int:
        """Return the configured maximum live entries per block."""

        return self._block_size

    def __len__(self) -> int:
        return len(self._values)

    def is_empty(self) -> bool:
        """Return whether no live key/value pairs remain."""

        return not self._values

    def insert(self, key: Key, value: Any) -> bool:
        """Insert or improve one key/value pair in `D1`.

        Returns `True` when the live structure changed. If `key` already has a
        value that is smaller than or equal to `value`, the call is ignored and
        returns `False`.
        """

        self._insert_operations += 1
        if not self._should_replace(key, value):
            return False

        self._values[key] = value
        self._push_heap(key, value)
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

        for key, value in candidates:
            self._values[key] = value
            self._push_heap(key, value)
        return len(candidates)

    def pull(self) -> PullResult:
        """Remove and return at most `M` smallest keys plus the next bound."""

        self._pull_operations += 1
        if not self._values:
            return PullResult((), (), self._upper_bound)

        selected: list[tuple[Key, Any]] = []
        while len(selected) < self._block_size and self._values:
            entry = self._pop_valid_heap_entry()
            if entry is None:
                break
            selected.append((entry.key, entry.value))
            del self._values[entry.key]

        bound = self._minimum_value()
        if bound is None:
            bound = self._upper_bound

        pairs = tuple(selected)
        return PullResult(tuple(key for key, _ in selected), pairs, bound)

    def snapshot(self) -> BlockListSnapshot:
        """Return immutable block and counter state for tests and traceability."""

        return BlockListSnapshot(
            size=len(self),
            d0_blocks=(),
            d1_blocks=_snapshot_blocks(self._ordered_pairs(), self._block_size),
            d1_upper_bounds=tuple(
                block[-1][1]
                for block in _snapshot_blocks(self._ordered_pairs(), self._block_size)
            ),
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
        current = self._values.get(key, _MISSING)
        if current is _MISSING:
            return True
        return _less(value, current)

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

    def _push_heap(self, key: Key, value: Any) -> None:
        entry = (value, self._serial, key)
        self._serial += 1
        heapq.heappush(self._heap, entry)

    def _minimum_value(self) -> Any | None:
        entry = self._peek_valid_heap_entry()
        if entry is None:
            return None
        return entry.value

    def _peek_valid_heap_entry(self) -> _HeapEntry | None:
        while self._heap:
            value, serial, key = self._heap[0]
            current = self._values.get(key, _MISSING)
            if current is not _MISSING and current == value:
                return _HeapEntry(value, serial, key)
            heapq.heappop(self._heap)
        return None

    def _pop_valid_heap_entry(self) -> _HeapEntry | None:
        while self._heap:
            value, serial, key = heapq.heappop(self._heap)
            current = self._values.get(key, _MISSING)
            if current is not _MISSING and current == value:
                return _HeapEntry(value, serial, key)
        return None

    def _ordered_pairs(self) -> tuple[Pair, ...]:
        return tuple(sorted(self._values.items(), key=lambda pair: (pair[1], repr(pair[0]))))


_MISSING = object()


def _less(left: Any, right: Any) -> bool:
    return bool(left < right)


def _snapshot_blocks(
    pairs: tuple[Pair, ...],
    block_size: int,
) -> tuple[tuple[Pair, ...], ...]:
    return tuple(
        pairs[index : index + block_size]
        for index in range(0, len(pairs), block_size)
    )
