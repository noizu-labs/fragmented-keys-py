# Protocols & Public API

## Protocols

All protocols are `@runtime_checkable` (support `isinstance()` checks at runtime). Custom implementations need only satisfy the method signatures — no inheritance required.

### CacheHandler Protocol

```python
class CacheHandler(Protocol):
    def group_name(self) -> str
    def get(self, key: str) -> str | None
    def set(self, key: str, value: str, ttl: int | None = None) -> None
    def get_multi(self, keys: list[str]) -> dict[str, str]
```

`group_name()` is used by `StandardKey._gather_group_versions()` to batch tags sharing the same handler into a single `get_multi()` call.

### Tag Protocol

```python
class Tag(Protocol):
    def get_tag_name(self) -> str
    def get_tag_version(self) -> float
    def get_full_tag(self) -> str               # "{name}@{version}"
    def increment(self) -> None
    def reset_tag_version(self) -> None
    def set_tag_version(self, version: float, update: bool = False) -> None
    def set_cache_handler(self, handler: CacheHandler) -> None
    def get_cache_handler(self) -> CacheHandler
    def delegate_cache_query(self, group: str) -> bool
```

`delegate_cache_query(group)` returns `True` if this tag's handler matches the given group name, meaning its version should be fetched in that group's bulk `get_multi()` call. `ConstantTag` always returns `False`.

### Key Protocol

```python
class Key(Protocol):
    def get_key_str(self, hash: bool = True) -> str
    def add_tag(self, tag: Tag) -> None
```

### KeyRing Protocol

```python
class KeyRing(Protocol):
    def define_key(self, key: str, params: list, globals: dict | None = None) -> None
    def tag(self, tag: str, instance: str, options: dict | None = None) -> Tag
```

## Public API Surface

Exported from `fragmented_keys.__init__`:

| Symbol | Type | Source Module |
|--------|------|---------------|
| `Configuration` | Class | `configuration` |
| `ConstantTag` | Class | `tag.constant` |
| `FragmentedKeyRing` | Class | `key_ring` |
| `MemoryHandler` | Class | `cache_handler.memory` |
| `RedisHandler` | Class | `cache_handler.redis_handler` |
| `StandardKey` | Class | `key.standard` |
| `StandardTag` | Class | `tag.standard` |

## Error Handling

| Location | Error | Condition |
|----------|-------|-----------|
| `Configuration.get_default_cache_handler()` | `RuntimeError` | Called before any handler is set |
| `FragmentedKeyRing._resolve_handler()` | `ValueError` | Unknown handler name |
| `FragmentedKeyRing.get_key_obj()` | `ValueError` | Key not defined, or wrong number of `tag_values` |
| `BaseTag.increment()` | `NotImplementedError` | Called on base class directly |
| `BaseTag.reset_tag_version()` | `NotImplementedError` | Called on base class directly |
