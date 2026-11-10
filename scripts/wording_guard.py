#!/usr/bin/env python3
"""Wording guard for the trip-lever project (standard library only).

Project rule: everything tracked in this repository is written in neutral
repair-scope language. Record what was checked and what was found, in plain terms.

This script enforces the rule mechanically over every tracked text file. The
wordings it rejects are held only as digests, so the checker itself stays inside
the rule and there is no readable list to copy from.

    python scripts/wording_guard.py                  scan every tracked text file
    python scripts/wording_guard.py FILE [FILE ...]  scan the given files
    python scripts/wording_guard.py --stdin          scan piped text (commit message, PR text)
    python scripts/wording_guard.py --digest TEXT    print the ENTRIES line for TEXT

Exit status: 0 clean, 1 at least one hit, 2 usage error.

If it reports a hit, open the file at the reported line and rewrite the sentence
so that it states what was checked and what was found. Rewrite it where it
stands; do not move it to another file and do not describe it.

Matching is on whole words, ignores case and punctuation, and follows a phrase
across line breaks. A digest is the truncated SHA-256 of the normalised words;
the CRC-32 next to it is only a fast pre-filter.
"""
from __future__ import annotations

import bisect
import hashlib
import pathlib
import re
import subprocess
import sys
import zlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOKEN = re.compile(rb"[A-Za-z0-9]+")
NEWLINE = re.compile(rb"\n")
PREFIX = b"k8-wording-v1:"
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "build", "dist"}

# Each entry is "<word count>:<crc32>:<sha256 prefix>". Add one with --digest.
ENTRIES: tuple[str, ...] = (
    "2:0cb68e1f:124cdc99a15a9204",
    "2:0ceac2dc:41bc04d8174a9198",
    "2:180bbf56:6dfe5d1d7a1a12a9",
    "2:1fd06137:fd52880bd97abfd1",
    "2:21f931fe:b184bc7619e07cfa",
    "2:2735b356:a7afb9c01a594aaf",
    "2:2be07b9c:e617c74abb2ddf2d",
    "2:3cb21795:3a33a89029720f8a",
    "2:4aa1c2e8:1da6bdd052f93216",
    "2:4ac84683:d8e3b8b97fdd66ce",
    "2:536e7ffa:61c8462bd163187c",
    "2:595582b0:cf53e5eb888edd88",
    "2:5d4b6d8a:58f66956adad128c",
    "2:65347f31:9961c6fe6a2f2bc6",
    "2:66d4caa6:1e44c64c576402c2",
    "2:6ec56913:eddfeb8e70145c95",
    "2:72e7440b:4991c4e081c0395d",
    "2:76f0ebc3:4b7622f6b8bb7e0a",
    "2:7a4c7f71:48bba6f2bcb17ea9",
    "2:7e7ee3b1:5f9961b4b75fe3f3",
    "2:81c19494:68b2907c49b0ced1",
    "2:837fceaa:4e3611f784ddc3ea",
    "2:85031f5a:61fbb758626593a5",
    "2:88163f51:e1ddf19901f29643",
    "2:8e7857ef:a08a58f8a97bb2e4",
    "2:960a7470:71e1118f69a955ef",
    "2:991e3075:5fd48247fd72d4a1",
    "2:9933824f:23d157381694ff65",
    "2:9d8c17b7:2b9a285bb063a790",
    "2:9fde4bbc:b09a84a928a8f0c8",
    "2:a7f9748d:b1a08ee3823e871a",
    "2:ac0c9005:e2216822d9dc7df8",
    "2:b2c3d223:80e5cb25c6ba7211",
    "2:bf6e03db:743abe7cfc73524c",
    "2:c14750f5:6cb8f2fcb1377a94",
    "2:d0362905:a403737b93b10d0e",
    "2:e18e4a09:3349210282e38093",
    "2:ed18d1b3:6b0d2a76046a7503",
    "2:ee8c5fab:b3c4e401a70c2080",
    "2:f432a63c:bea82b21071159d5",
    "2:f77f2975:8966b517e974b6ee",
    "2:f848fcd8:9848a1c3f12003e2",
    "2:f9d77938:bacea67301bb330e",
    "2:fe47046c:1c27b2626fcb48ce",
    "3:03c5433e:edcb1ef36ffee287",
    "3:15557ef9:d177fcd39beef578",
    "3:1ab8f046:dbf92360b4bfe321",
    "3:1c1d793c:47b0aea6637bd1b0",
    "3:2e85f9ce:a69a7f3c0bedc41c",
    "3:32e17c82:a7f0655776382232",
    "3:3f8a5022:61a1b1164e17f419",
    "3:4ad2b703:b60627cfb87ccc2a",
    "3:4b05996f:922f4e89cd2d3ebf",
    "3:4c1ae5f1:3186fad59a6c03c8",
    "3:5f96e82d:9b6071415c95b7b0",
    "3:70e16ffe:d4ac1ed2463d7f3d",
    "3:728ec9a3:4bdab9dcd67a442f",
    "3:7ce2345c:56a3a1f489def000",
    "3:7fd1bb1f:d25fac81b0f8e0aa",
    "3:814eae8b:50673c934250b5d3",
    "3:93ea1f74:6477a32973b3283d",
    "3:96149af1:01f6a57f4dd92df4",
    "3:ac030602:d7b373f80ec5b490",
    "3:b4dcd419:aacf506d76dfd84e",
    "3:b8759a7e:3e96fade304297b5",
    "3:bbfb6d35:41a1f93a9ca51029",
    "3:c9b22217:827de5cfe70e1e19",
    "3:cb86ae5a:26697b4c389bf8ca",
    "3:ccba354d:97c13b89e577da9d",
    "3:d23d35f4:245cbf45dae6fb7d",
    "3:d6e25b9a:6361894c1f2acbcd",
    "3:dffd1e0b:6742ee06147031ea",
    "3:e4cf5656:e722df8e311bec37",
    "3:e5c908a2:c14a63c130847c09",
    "3:e7a39348:6ad5a1dcf33e4531",
    "3:f33aa3c2:44bf8215699a3e33",
    "4:01bce1cb:33bbb3ce924a1b26",
    "4:064d40e4:d4c0c072e98febb4",
    "4:083d1797:a99a3d18df24d75d",
    "4:21884caf:2518dbd45ecba9d7",
    "4:434e812c:60db2fc8a7c4d8a4",
    "4:4e49479f:f104660d48c7c27b",
    "4:8c3aaf7c:b81fac8fd2db8768",
    "4:94900b99:8c788efa64086708",
    "4:991228c7:4efcf4b0ad179a7f",
    "4:c4b42cd0:dd92003e09b20e31",
    "4:c874b8c9:b8fb4efbdc72f481",
    "4:c8d25382:2768275fad50176e",
    "4:f745b5fd:3fc4f67f5ab4bc3d",
    "5:806a6991:09935e74964a883a",
    "5:b96ec50c:e7a970d73dee5c8b",
    "6:07359a5f:45d2a2249482c67a",
)


def _normalise(text: bytes) -> bytes:
    return b" ".join(token.lower() for token in TOKEN.findall(text))


def _sha(chunk: bytes) -> str:
    return hashlib.sha256(PREFIX + chunk).hexdigest()[:16]


def entry(text: str) -> str:
    """Return the ENTRIES line for a wording, without storing the wording."""
    chunk = _normalise(text.encode("utf-8", "ignore"))
    if not chunk:
        raise ValueError("no words to digest")
    return f"{chunk.count(b' ') + 1}:{zlib.crc32(chunk):08x}:{_sha(chunk)}"


def build_table(entries=ENTRIES) -> dict[int, dict[int, set[str]]]:
    table: dict[int, dict[int, set[str]]] = {}
    for item in entries:
        size, crc, sha = item.split(":")
        table.setdefault(int(size), {}).setdefault(int(crc, 16), set()).add(sha)
    return table


_DEFAULT_TABLE = None


def scan_bytes(data: bytes, table=None) -> list[tuple[int, str]]:
    """Return (line number, digest) for each rejected wording found in data."""
    global _DEFAULT_TABLE
    if table is None:
        if _DEFAULT_TABLE is None:
            _DEFAULT_TABLE = build_table()
        table = _DEFAULT_TABLE
    spans = [(match.start(), match.group().lower()) for match in TOKEN.finditer(data)]
    if not spans or not table:
        return []
    norm = b" ".join(token for _, token in spans)
    starts, ends, position = [], [], 0
    for _, token in spans:
        starts.append(position)
        position += len(token)
        ends.append(position)
        position += 1
    newlines = [match.start() for match in NEWLINE.finditer(data)]
    crc32 = zlib.crc32
    hits = []
    total = len(spans)
    for size, crcs in table.items():
        last = size - 1
        for index in range(total - last):
            chunk = norm[starts[index]:ends[index + last]]
            candidates = crcs.get(crc32(chunk))
            if candidates:
                digest = _sha(chunk)
                if digest in candidates:
                    hits.append((bisect.bisect_right(newlines, spans[index][0]) + 1, digest))
    return sorted(set(hits))


def tracked_files(root: pathlib.Path = ROOT) -> list[pathlib.Path]:
    """Tracked files plus new files that are not ignored; falls back to a walk."""
    try:
        out = subprocess.run(
            ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            cwd=root, capture_output=True, check=True,
        ).stdout
        names = [name.decode("utf-8", "surrogateescape") for name in out.split(b"\0") if name]
        return [root / name for name in names]
    except (OSError, subprocess.CalledProcessError):
        return [
            path for path in sorted(root.rglob("*"))
            if path.is_file() and not (set(path.relative_to(root).parts) & SKIP_DIRS)
        ]


def scan_paths(paths, root: pathlib.Path = ROOT, table=None) -> list[tuple[str, int, str]]:
    hits = []
    for path in paths:
        path = pathlib.Path(path)
        try:
            data = path.read_bytes()
        except OSError:
            continue
        if b"\0" in data[:8192]:
            continue  # binary
        try:
            name = str(path.resolve().relative_to(root.resolve()))
        except ValueError:
            name = str(path)
        hits.extend((name, line, digest) for line, digest in scan_bytes(data, table))
    return hits


def scan_repo(root: pathlib.Path = ROOT) -> list[tuple[str, int, str]]:
    return scan_paths(tracked_files(root), root)


def format_hits(hits) -> str:
    lines = [f"{name}:{line}: wording outside the neutral repair-scope rule [{digest}]"
             for name, line, digest in hits]
    if lines:
        lines.append(
            f"{len(lines)} hit(s). Rewrite each sentence where it stands so that it states what was "
            "checked and what was found; see the docstring of scripts/wording_guard.py."
        )
    return "\n".join(lines)


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv[:1] == ["--digest"]:
        if len(argv) != 2:
            print("usage: wording_guard.py --digest TEXT", file=sys.stderr)
            return 2
        print(f'    "{entry(argv[1])}",')
        return 0
    if argv == ["--stdin"]:
        hits = [("<stdin>", line, digest) for line, digest in scan_bytes(sys.stdin.buffer.read())]
    elif any(arg.startswith("--") for arg in argv):
        print(__doc__, file=sys.stderr)
        return 2
    elif argv:
        hits = scan_paths(argv)
    else:
        hits = scan_repo()
    if hits:
        print(format_hits(hits))
        return 1
    print("wording guard: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
