"""Landmarks: rebalanced effects, costs and garrisons.

- effects, construction costs and garrisons: settings/landmarks.py
- the rebuilt landmarks (new building levels), their texts and fixes: generator/data/landmarks
"""

from __future__ import annotations

from lib.data import GameData, Overlay, stable_id

FEATURE = "landmarks"
DATA = "landmarks"

BEJ = "building_effects_junction_tables"
POOLED_COSTS = "resource_cost_pooled_resource_junctions_tables"
UNIT_GROUPS = "armed_citizenry_unit_groups_tables"
UNITS_IN_GROUP = "armed_citizenry_units_to_unit_groups_junctions_tables"
GROUPS_BY_BUILDING = "building_level_campaign_group_armed_citizenry_junctions_tables"
RESOURCES = {"gold": "troy_gold_buildings", "stones": "troy_stones_buildings", "wood": "troy_wood_buildings"}
GARRISON_UNIT_PRIORITY = 2


def apply(overlay: Overlay, settings) -> None:
    s = settings
    count = 0
    for tsv in overlay.data.data_tables(DATA):
        count += overlay.import_rows(tsv, FEATURE)
    texts = 0
    for loc in overlay.data.data_locs(DATA):
        for key, text, tooltip in loc.rows:
            overlay.put_loc(key, text, FEATURE, tooltip)
            texts += 1
    overlay.note(FEATURE, f"Rebuilt landmarks and fixes: {count} table rows and {texts} texts from "
                          f"generator/data/{DATA}.")
    _effects(overlay, s)
    _costs(overlay, s)
    _garrisons(overlay, s)


def _effects(overlay: Overlay, s) -> None:
    count = 0
    for building, effects in s.LANDMARK_EFFECTS.items():
        for (effect, scope), spec in effects.items():
            if isinstance(spec, tuple):
                value, damaged, ruined, low, medium = spec
            else:
                value, damaged, ruined, low, medium = spec, int(spec / 2), 0, spec, spec
            overlay.put(BEJ, {"building": building, "effect": effect, "effect_scope": scope, "value": value,
                              "value_damaged": damaged, "value_ruined": ruined, "value_low_influence": low,
                              "value_medium_influence": medium}, FEATURE)
            count += 1
    overlay.note(FEATURE, f"Effects of {len(s.LANDMARK_EFFECTS)} landmarks ({count} effects, LANDMARK_EFFECTS).")


def _costs(overlay: Overlay, s) -> None:
    for building, costs in s.LANDMARK_COSTS.items():
        unknown = set(costs) - set(RESOURCES)
        if unknown:
            raise ValueError(f"LANDMARK_COSTS ({building}): unknown resources {sorted(unknown)}")
        for resource, amount in costs.items():
            overlay.put(POOLED_COSTS, {"pooled_resource_factor": RESOURCES[resource], "resource_cost": building,
                                       "amount": -amount}, FEATURE)
    overlay.note(FEATURE, f"Construction costs of {len(s.LANDMARK_COSTS)} landmarks (LANDMARK_COSTS).")


def _garrisons(overlay: Overlay, s) -> None:
    # The campaign groups every culture's buildings use: one per subculture, one per Sea Peoples faction.
    campaign_groups = sorted({row["campaign_group"] for row in overlay.rows(GROUPS_BY_BUILDING)
                              if "_subculture_" in row["campaign_group"]
                              or row["campaign_group"].startswith("phar_sea_armed_citizenry_faction_")})
    used_ids = {int(row["id"]) for row in overlay.rows(UNITS_IN_GROUP)}
    for building, (group, units) in s.LANDMARK_GARRISONS.items():
        overlay.put(UNIT_GROUPS, {"unit_group": group}, FEATURE)
        for campaign_group in campaign_groups:
            overlay.put(GROUPS_BY_BUILDING, {"building_level": building, "campaign_group": campaign_group,
                                             "unit_group": group}, FEATURE)
        for unit, number in units.items():
            for copy in range(number):
                new_id = stable_id(f"landmark|{group}|{unit}|{copy}", used_ids)
                overlay.put(UNITS_IN_GROUP, {"id": new_id, "priority": GARRISON_UNIT_PRIORITY, "unit": unit,
                                             "unit_group": group}, FEATURE)
    overlay.note(FEATURE, f"Garrisons of {len(s.LANDMARK_GARRISONS)} landmarks, for {len(campaign_groups)} cultures "
                          f"(LANDMARK_GARRISONS).")


def remapped_levels(data: GameData) -> dict[str, str]:
    """Landmark building levels replaced by new ones: old `<landmark>_1` -> new `<landmark>_2`.

    Some vanilla `_1` levels are moved to a "Placeholder" chain and a `_2` level takes
    their place, so rows other features attach to `_1` must follow.
    """
    remap = {}
    for tsv in data.data_tables(DATA):
        if tsv.table != "building_levels_tables":
            continue
        rows = list(tsv.dicts())
        names = {r["level_name"] for r in rows}
        for row in rows:
            name = row["level_name"]
            if row["chain"] == "Placeholder" and name.endswith("_1") and name[:-2] + "_2" in names:
                remap[name] = name[:-2] + "_2"
    return remap
