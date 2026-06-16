# Project Layout

```
fragmented-keys-py/
├── src/                                # Library source
│   └── fragmented_keys/                # Main package (PyPI: fragmented-keys)
│       ├── __init__.py                 #   Public API — re-exports all user-facing classes
│       ├── protocols.py                #   @runtime_checkable Protocols: CacheHandler, Tag, Key, KeyRing
│       ├── configuration.py            #   Global singleton (classmethod-only): default handler, prefix
│       ├── key_ring.py                 #   FragmentedKeyRing — template factory, option layering, dynamic accessors
│       ├── py.typed                    #   PEP 561 typed-package marker
│       ├── cache_handler/              #   Cache backend implementations
│       │   ├── __init__.py             #     Re-exports MemoryHandler, RedisHandler
│       │   ├── redis_handler.py        #     RedisHandler — production backend (injected redis.Redis client)
│       │   └── memory.py              #     MemoryHandler — in-memory dict for testing (no TTL)
│       ├── key/                        #   Composite cache key
│       │   ├── __init__.py             #     Re-exports StandardKey
│       │   └── standard.py            #     StandardKey — MD5 hash of versioned tag composition
│       └── tag/                        #   Versioned tag-instance pairs
│           ├── __init__.py             #     Re-exports StandardTag, ConstantTag
│           ├── base.py                #     BaseTag — version storage/retrieval, lazy seeding, cache delegation
│           ├── standard.py            #     StandardTag — incrementable version (+0.1)
│           └── constant.py            #     ConstantTag — fixed version, all mutations are no-ops
│
├── tests/                              # Test suite (pytest)
│   ├── __init__.py
│   ├── conftest.py                     #   Fixtures: memory_handler, auto Configuration.reset()
│   ├── test_fragmented_keys.py         #   26+ unit tests — tags, keys, key ring, delegation
│   └── test_redis_integration.py       #   Integration tests against live Redis on localhost:6379
│
├── docs/                               # Documentation
│   ├── PROJ-ARCH.md                    #   Architecture overview (links to arch/)
│   ├── PROJ-ARCH.summary.md            #   Condensed architecture summary for agents
│   ├── PROJ-LAYOUT.md                  #   This file
│   ├── PROJ-LAYOUT.summary.md          #   Condensed layout summary for agents
│   ├── arch/                           #   Detailed architecture sections
│   │   ├── protocols-api.md            #     Protocol signatures, public API, error catalog
│   │   ├── data-flow.md               #     Sequence diagrams, version lifecycle, option resolution
│   │   ├── cache-handlers.md          #     Handler implementations, custom handler guide
│   │   └── key-ring.md               #     KeyRing constructor, option layering, dynamic accessors
│   ├── conf.py                         #   Sphinx configuration (autodoc, furo theme)
│   ├── index.rst                       #   Sphinx root — landing page with toctree
│   ├── quickstart.rst                  #   Getting started guide
│   ├── api.rst                         #   API reference entry point
│   ├── configuration.rst               #   Configuration class docs
│   ├── cache_handlers.rst              #   Cache handler docs
│   ├── keys.rst                        #   Key class docs
│   ├── keyring.rst                     #   KeyRing class docs
│   ├── tags.rst                        #   Tag class docs
│   ├── requirements.txt                #   Sphinx build deps (sphinx>=7.0, furo)
│   ├── _static/                        #   Sphinx static assets
│   │   └── .gitkeep
│   └── _templates/                     #   Sphinx template overrides
│       └── .gitkeep
│
├── .claude/                            #   Claude Code configuration
│   └── settings.local.json             #     Local permission overrides (gitignored paths)
├── .readthedocs.yaml                   # Read the Docs build config (Python 3.13, Sphinx)
├── .python-version                     # Python 3.13
├── .gitignore                          # Ignores .venv, dist, __pycache__, docs/_build, *.egg-info
├── pyproject.toml                      # Package metadata, deps, build config (uv_build)
├── uv.lock                             # Locked dependency versions
├── LICENSE                             # MIT
└── README.md                           # Usage guide, API reference, installation
```

## Key Entry Points

| File | Role |
|------|------|
| `src/fragmented_keys/__init__.py` | Public API — import everything from here |
| `src/fragmented_keys/key_ring.py` | Primary user-facing class (`FragmentedKeyRing`) |
| `docs/conf.py` | Sphinx documentation build configuration |
| `pyproject.toml` | Package metadata, dependency specs, build system |

## Documentation Structure

Documentation lives in two systems:

| System | Location | Purpose |
|--------|----------|---------|
| **Sphinx / RTD** | `docs/*.rst`, `docs/conf.py` | Published API docs at [fragmented-keys-py.readthedocs.io](https://fragmented-keys-py.readthedocs.io) |
| **Agent docs** | `docs/PROJ-*.md`, `docs/arch/*.md` | Architecture and layout docs for Claude Code and developers |

## Test Organization

| File | Type | Requires |
|------|------|----------|
| `test_fragmented_keys.py` | Unit tests | `MemoryHandler` only (no external services) |
| `test_redis_integration.py` | Integration tests | Live Redis on `localhost:6379` |
