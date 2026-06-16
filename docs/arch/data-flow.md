# Data Flow

## Key Generation — Detailed Sequence

```mermaid
sequenceDiagram
    participant App
    participant Key as StandardKey
    participant Tag as StandardTag
    participant CT as ConstantTag
    participant Cache as CacheHandler

    App->>Key: get_key_str(hash=True)
    Key->>Key: _gather_group_versions()

    Note over Key: Group tags by handler.group_name()
    Note over Key: ConstantTag.delegate_cache_query() → False (skipped)

    Key->>Cache: get_multi([tag1_name, tag2_name, ...])
    Cache-->>Key: {tag_name: version_str, ...}

    loop Each fetched tag
        Key->>Tag: set_tag_version(float(cached_version))
    end

    Note over Key: Tags not in cache → version seeded on next access

    Key->>Key: Build raw string
    Note over Key: "{key}_{groupId}:t{tag1}:v{ver1}:t{tag2}:v{ver2}..."
    Key->>Key: md5(raw.encode("utf-8")).hexdigest()
    Key-->>App: "a1b2c3d4e5f6..."
```

## Version Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Unset: Tag created (version=None)
    Unset --> Seeded: First get_tag_version() call
    Seeded --> Cached: _store_version() persists to handler

    Cached --> Incremented: increment()
    Incremented --> Cached: _store_version(version + 0.1)

    Cached --> Reset: reset_tag_version()
    Reset --> Cached: _store_version(time.time() * 1000)

    note right of Seeded: Seed = time.time() * 1000\n(millisecond timestamp)
```

### Version Seeding

On first access, if no version exists in cache, `BaseTag._get_version()` generates `time.time() * 1000` (millisecond-precision Unix timestamp) and stores it. This ensures unique initial versions across tags without coordination.

### Version Increment

`StandardTag.increment()` adds `0.1` to the current version and persists immediately. The fractional increment means:
- Integer part: original seed timestamp
- Fractional part: number of invalidations (× 0.1)

### Bulk Fetch Optimization

`StandardKey._gather_group_versions()` reduces cache round-trips:

1. Partition tags into groups by `handler.group_name()`
2. Exclude tags where `delegate_cache_query(group) == False` (i.e., `ConstantTag`)
3. Issue one `get_multi()` per handler group
4. Distribute fetched versions back to individual tags via `set_tag_version()`

For N tags across M handler types, this produces M cache calls instead of N.

## Option Resolution — FragmentedKeyRing

```mermaid
graph LR
    G[global_options] --> M[Merged Options]
    GT[global_tag_options per tag name] --> M
    PC[Per-call overrides] --> M
    M --> TF[Tag Factory]
    TF -->|type=constant| CT[ConstantTag]
    TF -->|type=standard or default| ST[StandardTag]
```

Merge priority (highest wins): per-call overrides > per-tag globals > global options.

Recognized option keys:
- `type` — `"standard"` (default) or `"constant"`
- `version` — explicit initial version (float)
- `cache_handler` — handler name string (resolved via `_resolve_handler`)
- `prefix` — key prefix string
