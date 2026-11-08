#!/usr/bin/env python3
"""Neutral content guard for the published overflow project.

The detector stores SHA-256 digests of normalized restricted phrases and hashes
word n-grams in candidate text. It never reproduces the phrases themselves in
the repository. Standard library only.
"""
from __future__ import annotations

import hashlib
import re

# Digests of normalized restricted wording. Do not replace these with literals.
RESTRICTED_DIGESTS = frozenset({
    "d907028bf48105b3e003eb5d77c17b56b6ff2e5ce3bf20b1676001c02bc6b1b3",
    "dfc4f5aaebb1e4c7680c3d55022eaa8289c46f5c0ce829e9776271d7bd2309a8",
    "4ac29ab46a79f5ff87b48b8c2400f1a92e41613030ad3f38d9bf1ba796e1cfb0",
    "42ec7b0c78d05dfa3607a956cb282a1329ef436af74c8078ac5f4710122234c1",
    "08da8b6233b46f210e3b197b9612d0e79748cc88312904d7afef3f093d0b48d2",
    "00550185ae7603f662277edbeb5622dd70ef7321bca744204c8313a8340c0f0a",
    "de52bf66fd8c472a0d76feac60064c15eb5a9b901321464d3861d94dbffa3b11",
    "7aecb3e0aaac699f3a56dfdf1f28ff168ced488dd4cae56d2ab350be4641747c",
    "d987b2cf443b790b2c775c518c47fca8fa3175e921e8158a5f80c44024d44de3",
    "a71f1b5a32e79501ea7cc7196cebf88c4dea8243ecd92b83711165c41261b4a1",
    "6137fae9474ea2ff4818f2832451b0ffd23e19e0f5911d7ec47c8266d550f901",
    "fdce2657a204ff896fd77d12f9b20d91036d79eca59030c875597be296f09c35",
    "23ec0ca8559e8e2db902c3b20a9451797bd8f30808259ff06de13309e3835500",
    "ee22dfa9cbb44813a32fffbe6fa5f05c5e0ba17779a127c1940fce17d901234a",
    "6e0e32ac140569de0958b62c4c0dac6fc4b826a56fff0b0dafa95567f15bde6c",
    "cdfbf4d4f553c47351f6b0b5946535d8f38b77dd858cc16b08c798f9affbd158",
    "e0521c8a7d0cc86f7a87041535825d42fa44007b3f77c484bdbfe83f7ce036ad",
    "fb11cb1cfb2266e30723103df385d0e2004ee9f448c8636c6a94cb578442e81d",
    "6bfec4b02ea23a9aca389ecdb0d92dc9991bbf71ef5924c4d049684c733a2792",
    "328c9160465d2262a89dc457eab55087d15e103baf4b03b2c8e4f2419fad4315",
    "860c1509d2e826d2797a822742d7871b311c15025e971c11502d1dd453ef7838",
    "2d3dac6de8e70e8355852e8bf0e9fab8b4c3beb0c3d8d19e8ccd00acdfe6e9e0",
    "aa5422d7aff45eedf40d7f7369a1a668aa965338caab309bff183f8f94a5936a",
    "4094961e015e6143a7b673d3ff8ffb709aed26e361af1dc9ce7e71ba143b2fc3",
    "207c0c243413850f7aaabb55b52bb5a98046564d028bcbe2a004127ba61dbcd9",
})
MIN_WORDS = 2
MAX_WORDS = 11


def normalized_words(text: str) -> list[str]:
    """Return lower-case alphanumeric word tokens from any text."""
    return re.findall(r"[a-z0-9]+", text.lower())


def restricted_hits(text: str) -> set[str]:
    """Return digests of restricted normalized n-grams found in ``text``."""
    words = normalized_words(text)
    hits: set[str] = set()
    for width in range(MIN_WORDS, MAX_WORDS + 1):
        for start in range(0, max(0, len(words) - width + 1)):
            phrase = " ".join(words[start:start + width])
            digest = hashlib.sha256(phrase.encode("utf-8")).hexdigest()
            if digest in RESTRICTED_DIGESTS:
                hits.add(digest)
    return hits


def has_restricted(text: str) -> bool:
    """True when any restricted phrase digest matches."""
    words = normalized_words(text)
    for width in range(MIN_WORDS, MAX_WORDS + 1):
        for start in range(0, max(0, len(words) - width + 1)):
            phrase = " ".join(words[start:start + width])
            if hashlib.sha256(phrase.encode("utf-8")).hexdigest() in RESTRICTED_DIGESTS:
                return True
    return False
