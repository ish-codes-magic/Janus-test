# Janus-test

A small scratch repository used to exercise the Janus demo agents against a
real GitHub repository and a real issue.

## Contents

- `lru_cache.py` — a fixed-capacity LRU cache backed by a `dict`.
- `test_lru_cache.py` — its test suite.

## Usage

```python
from lru_cache import LRUCache

cache = LRUCache(capacity=2)
cache.put("a", 1)
cache.put("b", 2)
cache.get("a")
cache.put("c", 3)   # evicts the least recently used entry
```

## Running the tests

```bash
pip install pytest
pytest -q
```
