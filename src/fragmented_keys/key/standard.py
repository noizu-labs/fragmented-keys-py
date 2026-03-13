from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fragmented_keys.tag.base import BaseTag


class StandardKey:
    """A composite cache key built from multiple versioned tags.

    The final key string is an MD5 hash of the base key name combined
    with each tag's name and current version, so that any tag version
    change produces a completely different key.
    """

    def __init__(
        self,
        key: str,
        tags: list[BaseTag] | None = None,
        group_id: str = "",
    ) -> None:
        self._key = key
        self._tags: list[BaseTag] = list(tags) if tags else []
        self._group_id = group_id

    def add_tag(self, tag: BaseTag) -> None:
        self._tags.append(tag)

    # -- bulk version fetching -------------------------------------------------

    def _gather_group_versions(self) -> None:
        """Fetch all tag versions in bulk, grouped by cache handler.

        Tags sharing the same handler are fetched with a single
        ``get_multi`` call rather than N individual requests.
        """
        groups: dict[str, list[BaseTag]] = {}
        for tag in self._tags:
            group = tag.get_cache_handler().group_name()
            if tag.delegate_cache_query(group):
                groups.setdefault(group, []).append(tag)

        for group_name, group_tags in groups.items():
            keys = [t.get_tag_name() for t in group_tags]
            handler = group_tags[0].get_cache_handler()
            results = handler.get_multi(keys)
            for tag in group_tags:
                cached = results.get(tag.get_tag_name())
                if cached is not None:
                    tag.set_tag_version(float(cached))

    # -- key generation --------------------------------------------------------

    def get_key_str(self, hash: bool = True) -> str:
        """Build the composite key string.

        When *hash* is ``True`` (default) the key is returned as an MD5
        hex digest suitable for use as a cache key.  Pass ``False`` to
        get the raw string for debugging.
        """
        self._gather_group_versions()

        parts = [f"{self._key}_{self._group_id}"]
        for tag in self._tags:
            parts.append(f":t{tag.get_tag_name()}:v{tag.get_tag_version()}")

        raw = "".join(parts)
        if not hash:
            return raw
        return hashlib.md5(raw.encode("utf-8")).hexdigest()
