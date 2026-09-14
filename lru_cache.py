"""
A small fixed-capacity LRU (least-recently-used) cache.

Backed by a plain ``dict``, which preserves insertion order on Python 3.7+.
The oldest entry is therefore the first key produced by iterating the dict,
and eviction pops that key.

Example
-------
::

    cache = LRUCache(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")        # -> 1
    cache.put("c", 3)     # evicts the least recently used entry
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")

__all__ = ["LRUCache"]


class LRUCache(Generic[K, V]):
    """
    A cache that holds at most ``capacity`` entries.

    When the cache is full, inserting a new key evicts the least recently
    used entry to make room.
    """

    def __init__(self, capacity: int) -> None:
        """
        Args:
            capacity: Maximum number of entries to retain. Must be positive.

        Raises:
            ValueError: If ``capacity`` is not positive.
        """
        if capacity <= 0:
            raise ValueError(f"capacity must be positive, got {capacity}")
        self._capacity = capacity
        self._data: dict[K, V] = {}
        self.hits = 0
        self.misses = 0

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def get(self, key: K, default: V | None = None) -> V | None:
        """
        Return the value for ``key``, or ``default`` if it is not cached.

        Records a hit or a miss in the cache statistics.
        """
        if key in self._data:
            self.hits += 1
            return self._data[key]
        self.misses += 1
        return default

    def put(self, key: K, value: V) -> None:
        """
        Insert or update ``key``.

        If the cache is at capacity and ``key`` is new, the least recently
        used entry is evicted first.
        """
        if key in self._data:
            self._data[key] = value
            return

        if len(self._data) >= self._capacity:
            self._evict_one()

        self._data[key] = value

    def _evict_one(self) -> None:
        """Drop the least recently used entry."""
        oldest = next(iter(self._data))
        del self._data[oldest]

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    @property
    def capacity(self) -> int:
        """The maximum number of entries this cache retains."""
        return self._capacity

    def keys(self) -> Iterator[K]:
        """Iterate cached keys, least recently used first."""
        return iter(self._data)

    def stats(self) -> dict[str, int]:
        """Return hit/miss counters and current size."""
        return {"hits": self.hits, "misses": self.misses, "size": len(self._data)}

    def clear(self) -> None:
        """Remove every entry and reset the counters."""
        self._data.clear()
        self.hits = 0
        self.misses = 0

    def __contains__(self, key: object) -> bool:
        return key in self._data

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"LRUCache(capacity={self._capacity}, size={len(self._data)})"
