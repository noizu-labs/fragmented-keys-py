# Project Layout — Summary

```
fragmented-keys-py/
├── src/fragmented_keys/            # Library source (PyPI: fragmented-keys)
│   ├── __init__.py                 #   Public API re-exports
│   ├── protocols.py                #   @runtime_checkable Protocol definitions
│   ├── configuration.py            #   Global singleton config
│   ├── key_ring.py                 #   Key template factory + dynamic accessors
│   ├── cache_handler/              #   RedisHandler (production) + MemoryHandler (testing)
│   ├── key/                        #   StandardKey — MD5 composite cache key
│   └── tag/                        #   BaseTag, StandardTag (+0.1), ConstantTag (fixed)
├── tests/                          # pytest — unit (26+) + Redis integration
│   ├── test_fragmented_keys.py     #   Unit tests (MemoryHandler)
│   └── test_redis_integration.py   #   Live Redis integration tests
├── docs/                           # Sphinx (RTD) + agent architecture docs
│   ├── *.rst, conf.py              #   Sphinx sources → readthedocs.io
│   ├── PROJ-ARCH.md + arch/        #   Architecture docs (4 detail files)
│   └── PROJ-LAYOUT.md              #   This layout
├── .readthedocs.yaml               # RTD build config (Python 3.13, Sphinx)
├── pyproject.toml                  # Package metadata, deps (uv_build)
├── uv.lock                         # Locked dependencies
└── README.md                       # Usage guide + API reference
```
