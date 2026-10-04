"""Buildings with garrisons.

- every garrison unit a building provides is multiplied (same unit types, commanders excluded)
- garrison buildings give ammunition bonuses to own armies in the region (generator/data/garrisons)
"""

from __future__ import annotations

import collections
import hashlib

from lib.data import Overlay

FEATURE = "garrisons"

LEGACY_PREFIX = "troy_"
GROUPS_BY_BUILDING = "building_level_campaign_group_armed_citizenry_junctions_tables"
UNITS_IN_GROUP = "armed_citizenry_units_to_unit_groups_junctions_tables"
INT32_MAX = 2**31 - 1  # vanilla ids are random positive 32-bit numbers; stay in that range


def apply(overlay: Overlay, settings) -> None:
    s = settings
    count = 0
    for tsv in overlay.data.data_tables("garrisons"):
        count += overlay.import_rows(tsv, FEATURE)
    overlay.note(FEATURE, f"Garrison buildings give ammunition bonuses to own armies in their region "
                          f"({count} building effects, generator/data/garrisons).")
    _multiply_garrisons(overlay, s.GARRISON_MULTIPLIER)


def _multiply_garrisons(overlay: Overlay, multiplier: int) -> None:
    if multiplier <= 1:
        return
    caste = {row["unit"]: row["caste"] for row in overlay.rows("main_units_tables")}
    groups = {
        row["unit_group"]
        for row in overlay.rows(GROUPS_BY_BUILDING)
        if not row["building_level"].startswith(LEGACY_PREFIX)
    }
    units = list(overlay.rows(UNITS_IN_GROUP))
    used_ids = {int(row["id"]) for row in units}

    added = collections.Counter()
    for row in sorted(units, key=lambda r: (r["unit_group"], int(r["priority"]), r["unit"], int(r["id"]))):
        group = row["unit_group"]
        # Garrison commanders (one bodyguard unit per culture) are lords: the garrison only gets one.
        if group not in groups or caste.get(row["unit"]) in ("lord", "hero"):
            continue
        for copy in range(1, multiplier):
            new_id = _new_id(f"{group}|{row['unit']}|{row['id']}|{copy}", used_ids)
            overlay.put(UNITS_IN_GROUP, dict(row, id=str(new_id)), FEATURE)
            added[group] += 1
    overlay.note(FEATURE, f"Garrisons x{multiplier}: {sum(added.values())} garrison units added to "
                          f"{len(added)} unit groups (commanders excluded). Large settlements can now exceed "
                          f"20 garrison units in total; the units' priority decides which ones the game keeps "
                          f"if it caps them.")


def _new_id(seed: str, used: set[int]) -> int:
    salt = 0
    while True:
        digest = hashlib.sha1(f"dyn_rebal|{seed}|{salt}".encode()).digest()
        candidate = int.from_bytes(digest[:4], "big") & INT32_MAX
        if candidate > 1_000_000 and candidate not in used:
            used.add(candidate)
            return candidate
        salt += 1
