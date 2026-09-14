"""Tests for the LRU cache."""

import pytest

from lru_cache import LRUCache


def test_put_and_get():
    cache = LRUCache(capacity=2)
    cache.put("a", 1)
    assert cache.get("a") == 1


def test_missing_key_returns_default():
    cache = LRUCache(capacity=2)
    assert cache.get("nope") is None
    assert cache.get("nope", default=0) == 0


def test_update_existing_key_does_not_grow():
    cache = LRUCache(capacity=2)
    cache.put("a", 1)
    cache.put("a", 2)
    assert len(cache) == 1
    assert cache.get("a") == 2


def test_evicts_when_over_capacity():
    cache = LRUCache(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    assert len(cache) == 2
    assert "a" not in cache


def test_rejects_non_positive_capacity():
    with pytest.raises(ValueError):
        LRUCache(capacity=0)


def test_stats_track_hits_and_misses():
    cache = LRUCache(capacity=2)
    cache.put("a", 1)
    cache.get("a")
    cache.get("b")
    assert cache.stats() == {"hits": 1, "misses": 1, "size": 1}


def test_clear_resets_everything():
    cache = LRUCache(capacity=2)
    cache.put("a", 1)
    cache.get("a")
    cache.clear()
    assert len(cache) == 0
    assert cache.stats() == {"hits": 0, "misses": 0, "size": 0}
