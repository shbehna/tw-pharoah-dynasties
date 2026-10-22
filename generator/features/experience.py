"""Experience: unit and character experience from buildings, followers and traits.

Values from the "XP Followers Traits And Buildings Buffed" mod (Workshop 3456700913), in
settings/experience.py:
- buildings: unit experience per turn (EXPERIENCE_UNIT_BUILDINGS), new for garrison buildings
- buildings: character experience per turn (EXPERIENCE_CHARACTER_BUILDINGS)
- followers and titles (EXPERIENCE_ANCILLARIES), traits (EXPERIENCE_TRAITS)
"""

from __future__ import annotations

import collections
import re

from lib.data import Overlay

FEATURE = "experience"

BEJ = "building_effects_junction_tables"
ANCILLARY_EFFECTS = "ancillary_to_effects_tables"
TRAIT_EFFECTS = "trait_level_effects_tables"
UNIT_XP = "phar_main_unit_xp_mod_training_unit_sets_all"
CHARACTER_XP = "phar_main_scripted_char_xp_per_turn"
TRAIT_UNIT_XP = "troy_effect_army_units_experience_per_turn"
# Unit experience effects of followers: phar_main_unit_xp_mod_training_..., phar_map_units_xp_mod_training_...
ANCILLARY_UNIT_XP = re.compile(r"phar_\w+_xp_mod_training_\w+")
LEGACY_PREFIX = "troy_"


def apply(overlay: Overlay, settings) -> None:
    s = settings
    effects_by_building = collections.defaultdict(list)
    for row in overlay.rows(BEJ):
        effects_by_building[row["building"]].append(row)
    _unit_buildings(overlay, s, effects_by_building)
    _character_buildings(overlay, s, effects_by_building)
    _value_rows(overlay, ANCILLARY_EFFECTS, "ancillary", lambda e: ANCILLARY_UNIT_XP.fullmatch(e),
                s.EXPERIENCE_ANCILLARIES, "followers and titles")
    _value_rows(overlay, TRAIT_EFFECTS, "trait_level", lambda e: e == TRAIT_UNIT_XP, s.EXPERIENCE_TRAITS, "traits")


def _unit_buildings(overlay: Overlay, s, effects_by_building) -> None:
    levels = [row["level_name"] for row in overlay.rows("building_levels_tables")
              if not row["level_name"].startswith(LEGACY_PREFIX)]
    count = 0
    for building in levels:
        rule = next((rule for rule in s.EXPERIENCE_UNIT_BUILDINGS if re.fullmatch(rule[0], building)), None)
        if rule is None or rule[1] is None:
            continue
        value, scope = rule[1], (rule[2] if len(rule) > 2 else None)
        half = value // 2
        values = {"value": value, "value_damaged": half, "value_ruined": 0,
                  "value_low_influence": half, "value_medium_influence": half}
        if scope is None:
            rows = [row for row in effects_by_building.get(building, []) if row["effect"] == UNIT_XP]
            if not rows:
                raise ValueError(f"EXPERIENCE_UNIT_BUILDINGS: {building} has no {UNIT_XP} effect; "
                                 f"give its rule a scope")
        else:
            rows = [{"building": building, "effect": UNIT_XP, "effect_scope": scope}]
        for row in rows:
            overlay.put(BEJ, dict(row, **values), FEATURE)
        count += 1
    overlay.note(FEATURE, f"Unit experience per turn from {count} buildings (EXPERIENCE_UNIT_BUILDINGS).")


def _character_buildings(overlay: Overlay, s, effects_by_building) -> None:
    for building, value in s.EXPERIENCE_CHARACTER_BUILDINGS.items():
        rows = [row for row in effects_by_building.get(building, []) if row["effect"] == CHARACTER_XP]
        if not rows:
            raise ValueError(f"EXPERIENCE_CHARACTER_BUILDINGS: {building} has no {CHARACTER_XP} effect")
        for row in rows:
            old = float(row["value"])
            scaled = {c: int(float(row[c]) * value / old) for c in
                      ("value_damaged", "value_ruined", "value_low_influence", "value_medium_influence")}
            overlay.put(BEJ, dict(row, value=value, **scaled), FEATURE)
    overlay.note(FEATURE, f"Character experience per turn from {len(s.EXPERIENCE_CHARACTER_BUILDINGS)} buildings "
                          f"(EXPERIENCE_CHARACTER_BUILDINGS).")


def _value_rows(overlay: Overlay, table: str, key_column: str, is_effect, values: dict, label: str) -> None:
    rows = collections.defaultdict(list)
    for row in overlay.rows(table):
        if row[key_column] in values and is_effect(row["effect"]):
            rows[row[key_column]].append(row)
    missing = sorted(set(values) - set(rows))
    if missing:
        raise ValueError(f"Experience settings for {label}: no unit experience effect for {missing}")
    for key, key_rows in rows.items():
        for row in key_rows:
            overlay.put(table, dict(row, value=values[key]), FEATURE)
    overlay.note(FEATURE, f"Unit experience from {len(values)} {label}.")
