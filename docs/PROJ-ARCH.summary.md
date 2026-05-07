# Project Architecture — Summary

## Overview

Cache invalidation library that composes cache keys from independently versioned tag-instance pairs. Incrementing a tag version changes all dependent key hashes, causing cache misses without deleting entries. Python port of the PHP fragmented-keys library, using Redis. Published as `fragmented-keys` on PyPI.

## Core Components

- **Configuration** — Class-level singleton for global default handler and prefix (`@classmethod` only)
- **CacheHandler Protocol** — `@runtime_checkable`; 4 methods: `group_name`, `get`, `set`, `get_multi`
- **Tag/Key/KeyRing Protocols** — `@runtime_checkable` type contracts for all core abstractions
- **BaseTag** — Version storage, lazy seeding (`time.time()*1000`), cache delegation logic
- **StandardTag** — Incrementable cached version (+0.1 per increment)
- **ConstantTag** — Fixed version (`default=1.0`), all mutations no-ops, excluded from bulk fetches
- **StandardKey** — Composes tags into MD5-hashed cache key with grouped bulk version fetching
- **FragmentedKeyRing** — Template factory: define keys, 3-tier option layering, dynamic `get_{name}_key_obj()` accessors, `list_defined_keys()` introspection
- **RedisHandler** — Redis backend via injected client (`MGET`/`SETEX`, bytes decoding)
- **MemoryHandler** — In-memory dict for testing (no TTL support)

## Key Generation Flow

1. Group tags by `handler.group_name()`, exclude ConstantTags from bulk fetch
2. Bulk-fetch versions via `get_multi()` per handler group (M calls for N tags across M handlers)
3. Build raw string: `"{key}_{groupId}:t{tag}:v{version}..."`
4. Return MD5 hex digest (32 chars)

## Design Decisions

- Redis over Memcache (modern, `MGET`/`SETEX`)
- `@runtime_checkable` Protocols over ABCs (duck typing, no inheritance tax)
- Orphan invalidation (old keys expire via TTL, no bulk deletes)
- MD5 hashing (fixed-length, backend-safe, acceptable collision risk for ephemeral keys)
- Injected Redis client (`TYPE_CHECKING` import, clean module load)
- Class-level Configuration (all `@classmethod`, `reset()` for test isolation)
- Sync-only interfaces (no async support currently)

## Stack

Python 3.13+, redis-py >= 5.0, uv_build, pytest + pytest-asyncio, Sphinx + Furo (Read the Docs), PEP 561 typed, MIT license

## Testing

26+ tests across 4 classes (StandardTag, ConstantTag, StandardKey, KeyRing). Auto-use fixture resets Configuration per test. MemoryHandler with "Test" prefix for isolation.
