#!/usr/bin/env python3
"""Assert catalog.h, catalog.cpp and the ESPHome platform .py files agree.

The Python `ENT_*` constants must stay in lockstep with
`catalog.h`'s `EntityId`, because a mismatch is silent — codegen emits
`::atlantic_v5::ENT_SOMETHING` as raw text, so a renamed or reordered enum
member surfaces as a compile error at best and as an entity publishing another
entity's value at worst.

Four sources are checked against each other:

1. `EntityId` in catalog.h            — the ids themselves, in order
2. `NAMES[]` in catalog.cpp           — `entity_name(id)`, used in replay JSON
3. `SENSORS` / `BINARY_SENSORS` / `TEXT_SENSORS` in the platform .py files
   — the YAML keys users write, and the id each maps to
4. `header::MAPPED` / `header::UNMAPPED` — one raw-frame text entity per key,
   plus the unknown-frame catch-all
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

COMPONENT_DIR = Path(__file__).resolve().parent.parent.parent / "components" / "atlantic_v5"

ENUM_RE = re.compile(r"enum EntityId : uint16_t \{(.*?)\n\};", re.DOTALL)
# One member per line; comment lines start with `//` and so never match.
ENUM_MEMBER_RE = re.compile(r"^\s*(ENT_[A-Z0-9_]+)\b", re.MULTILINE)
NAMES_RE = re.compile(r"constexpr const char \*NAMES\[ENT_COUNT\] = \{(.*?)\n\};", re.DOTALL)
STRING_RE = re.compile(r'"([^"]*)"')
HEADER_CONST_RE = re.compile(r"constexpr uint64_t ([A-Z0-9_]+) = (0x[0-9A-Fa-f]+)ULL;")
HEADER_ARRAY_RE = re.compile(r"constexpr uint64_t (MAPPED|UNMAPPED)\[\] = \{(.*?)\n\};", re.DOTALL)
HEADER_ITEM_RE = re.compile(r"(0x[0-9A-Fa-f]+ULL|[A-Z][A-Z0-9_]*)")
# Matches `"yaml_key": ("ENT_X", ...)` and `"yaml_key": "ENT_X"`, across newlines.
PY_ENTRY_RE = re.compile(r'"([a-z0-9_]+)"\s*:\s*\(?\s*"(ENT_[A-Z0-9_]+)"')

PLATFORM_FILES = ("sensor.py", "binary_sensor.py", "text_sensor.py")

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def extract_block(pattern: re.Pattern[str], text: str, what: str, path: Path) -> str:
    match = pattern.search(text)
    if match is None:
        # A silently-renamed block would turn every check below into a vacuous pass.
        print(f"FATAL: could not find {what} in {path}", file=sys.stderr)
        sys.exit(2)
    return match.group(1)


def main() -> int:
    catalog_h = COMPONENT_DIR / "catalog.h"
    catalog_cpp = COMPONENT_DIR / "catalog.cpp"

    members = ENUM_MEMBER_RE.findall(extract_block(ENUM_RE, catalog_h.read_text(), "enum EntityId", catalog_h))
    check(bool(members), "enum EntityId parsed as empty")
    check(members[-1] == "ENT_COUNT", f"expected ENT_COUNT last in EntityId, got {members[-1]}")
    ids = members[:-1]
    check(len(set(ids)) == len(ids), "duplicate member names in EntityId")

    names = STRING_RE.findall(extract_block(NAMES_RE, catalog_cpp.read_text(), "NAMES[]", catalog_cpp))
    check(
        len(names) == len(ids),
        f"catalog.cpp NAMES[] has {len(names)} entries but EntityId has {len(ids)} ids before ENT_COUNT",
    )
    check(len(set(names)) == len(names), "duplicate entity names in catalog.cpp NAMES[]")

    catalog_h_text = catalog_h.read_text()
    header_values = {name: int(value, 16) for name, value in HEADER_CONST_RE.findall(catalog_h_text)}
    header_arrays = {
        table: [
            int(item[:-3], 16) if item.startswith("0x") else header_values[item]
            for item in HEADER_ITEM_RE.findall(body)
            if item.startswith("0x") or item in header_values
        ]
        for table, body in HEADER_ARRAY_RE.findall(catalog_h_text)
    }
    expected_frame_names = [
        f"frame_{key:010x}"
        for table in ("MAPPED", "UNMAPPED")
        for key in header_arrays.get(table, [])
    ] + ["unknown_frame"]
    frame_names = [name for name in names if name.startswith("frame_") or name == "unknown_frame"]
    check(
        frame_names == expected_frame_names,
        "raw-frame entity names must cover MAPPED and UNMAPPED headers in catalog order, plus unknown_frame",
    )

    index_of = {name: i for i, name in enumerate(ids)}
    exposed: dict[str, str] = {}

    for filename in PLATFORM_FILES:
        path = COMPONENT_DIR / filename
        for yaml_key, ent_id in PY_ENTRY_RE.findall(path.read_text()):
            if ent_id not in index_of:
                failures.append(f"{filename}: {ent_id} ({yaml_key}) is not a member of EntityId")
                continue
            if ent_id in exposed:
                failures.append(f"{filename}: {ent_id} is already exposed by {exposed[ent_id]}")
                continue
            exposed[ent_id] = filename
            if index_of[ent_id] < len(names):
                expected = names[index_of[ent_id]]
                check(
                    expected == yaml_key,
                    f"{filename}: YAML key {yaml_key!r} maps to {ent_id}, "
                    f"whose entity_name() is {expected!r} — the replay JSON and the "
                    f"entity would disagree",
                )

    for ent_id in ids:
        check(
            ent_id in exposed,
            f"{ent_id} exists in EntityId but no platform .py exposes it — "
            f"nothing can ever publish it",
        )

    for failure in failures:
        print(f"FAIL: {failure}")
    if failures:
        print(f"{len(failures)} failure(s)")
        return 1
    print(f"OK: {len(ids)} entity ids agree across catalog.h, catalog.cpp and {len(PLATFORM_FILES)} platform files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
