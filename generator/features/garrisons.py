"""Buildings with garrisons.

- garrison units multiplied (same unit types, commanders excluded), with one multiplier for the
  main buildings of settlements, one for lookout posts and one for every other building
- garrison buildings give ammunition bonuses to own armies in the region (generator/data/garrisons)
"""

from __future__ import annotations

import collections
import hashlib

from features.admin import settlement_class
from features.outposts import lookout_posts
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
    _multiply_garrisons(overlay, s)


def _group_multipliers(overlay: Overlay, s) -> dict[str, int]:
    """Unit group -> multiplier, from the kind of building that provides it."""
    # In priority order: a unit group used by several kinds of buildings gets the first one's multiplier.
    by_kind = {
        "settlement": s.SETTLEMENT_GARRISON_MULTIPLIER,
        "lookout post": s.LOOKOUT_GARRISON_MULTIPLIER,
        "other": s.GARRISON_MULTIPLIER,
    }
    lookouts = set(lookout_posts(overlay))
    kinds: dict[str, set[str]] = collections.defaultdict(set)
    for row in overlay.rows(GROUPS_BY_BUILDING):
        building = row["building_level"]
        if building.startswith(LEGACY_PREFIX):
            continue
        if settlement_class(building):
            kinds[row["unit_group"]].add("settlement")
        elif building in lookouts:
            kinds[row["unit_group"]].add("lookout post")
        else:
            kinds[row["unit_group"]].add("other")
    multipliers = {}
    for group, used_by in kinds.items():
        kind = next(k for k in by_kind if k in used_by)
        if len(used_by) > 1:
            overlay.note(FEATURE, f"Unit group {group} is used by {' and '.join(sorted(used_by))} buildings; "
                                  f"it gets the {kind} multiplier.")
        multipliers[group] = by_kind[kind]
    return multipliers


def _multiply_garrisons(overlay: Overlay, s) -> None:
    caste = {row["unit"]: row["caste"] for row in overlay.rows("main_units_tables")}
    multipliers = _group_multipliers(overlay, s)
    units = list(overlay.rows(UNITS_IN_GROUP))
    used_ids = {int(row["id"]) for row in units}

    added = collections.Counter()
    for row in sorted(units, key=lambda r: (r["unit_group"], int(r["priority"]), r["unit"], int(r["id"]))):
        group = row["unit_group"]
        # Garrison commanders (one bodyguard unit per culture) are lords: the garrison only gets one.
        if multipliers.get(group, 1) <= 1 or caste.get(row["unit"]) in ("lord", "hero"):
            continue
        for copy in range(1, multipliers[group]):
            new_id = _new_id(f"{group}|{row['unit']}|{row['id']}|{copy}", used_ids)
            overlay.put(UNITS_IN_GROUP, dict(row, id=str(new_id)), FEATURE)
            added[group] += 1
    overlay.note(FEATURE, f"Garrisons of settlement main buildings x{s.SETTLEMENT_GARRISON_MULTIPLIER}, of lookout "
                          f"posts x{s.LOOKOUT_GARRISON_MULTIPLIER}, of every other building x{s.GARRISON_MULTIPLIER}: "
                          f"{sum(added.values())} garrison units added to "
                          f"{len(added)} unit groups (commanders excluded).")


def _new_id(seed: str, used: set[int]) -> int:
    salt = 0
    while True:
        digest = hashlib.sha1(f"dyn_rebal|{seed}|{salt}".encode()).digest()
        candidate = int.from_bytes(digest[:4], "big") & INT32_MAX
        if candidate > 1_000_000 and candidate not in used:
            used.add(candidate)
            return candidate
        salt += 1
