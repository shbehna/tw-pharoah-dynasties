"""Helpers for building_effects_junction_tables rows."""

from __future__ import annotations

import math

from .data import Overlay, fmt_float

BEJ = "building_effects_junction_tables"
# Pooled resource factor of building upkeep: troy_<resource>_building_upkeep.
UPKEEP_FACTOR = "buildings_upkeep"
VALUE_COLUMNS = ["value", "value_damaged", "value_ruined", "value_low_influence", "value_medium_influence"]


def _round_like(reference: float, value: float) -> float:
    """Whole numbers stay whole (rounded half away from zero), others keep 2 decimals."""
    if float(reference).is_integer():
        return math.copysign(math.floor(abs(value) + 0.5), value)
    return round(value, 2)


def scaled_values(row: dict, new_value: float) -> dict:
    """Value columns of `row` rescaled proportionally so that `value` becomes `new_value`."""
    old = float(row["value"])
    if old == 0:
        return new_values(new_value)
    factor = new_value / old
    out = {"value": fmt_float(new_value)}
    for column in VALUE_COLUMNS[1:]:
        original = float(row[column])
        out[column] = fmt_float(_round_like(original, original * factor) + 0.0)  # + 0.0: no "-0" when the sign flips
    return out


def new_values(value: float, damaged: float | None = None) -> dict:
    """Value columns for a new effect row (vanilla convention: half the value when damaged)."""
    if damaged is None:
        damaged = _round_like(value, value / 2)
    return {
        "value": fmt_float(value),
        "value_damaged": fmt_float(damaged),
        "value_ruined": fmt_float(0),
        "value_low_influence": fmt_float(value),
        "value_medium_influence": fmt_float(value),
    }


def set_effect(
    overlay: Overlay,
    building: str,
    effect: str,
    scope: str,
    value: float,
    feature: str,
    damaged: float | None = None,
) -> bool:
    """Set `effect` on `building` to `value`: rescale an existing row or add a new one.

    Returns True when the overlay changed.
    """
    current = overlay.get(BEJ, (building, effect))
    if current is not None:
        if float(current["value"]) == value and current["effect_scope"] == scope:
            return False
        current.update(scaled_values(current, value))
        current["effect_scope"] = scope
        overlay.put(BEJ, current, feature)
        return True
    row = {"building": building, "effect": effect, "effect_scope": scope}
    row.update(new_values(value, damaged))
    overlay.put(BEJ, row, feature)
    return True


def building_levels(overlay: Overlay) -> dict[str, dict]:
    return {row["level_name"]: row for row in overlay.rows("building_levels_tables")}


def effects_by_building(overlay: Overlay) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for row in overlay.rows(BEJ):
        out.setdefault(row["building"], []).append(row)
    return out


def building_sets(overlay: Overlay) -> dict[str, set[str]]:
    """Building level -> building sets it belongs to (e.g. phar_main_religion).

    A set lists whole chains or single levels; rows marked `exclude` take a chain's level back out.
    """
    by_chain: dict[str, list[str]] = {}
    for row in overlay.rows("building_levels_tables"):
        by_chain.setdefault(row["chain"], []).append(row["level_name"])
    included: dict[str, set[str]] = {}
    excluded: dict[str, set[str]] = {}
    for row in overlay.rows("building_set_to_building_junctions_tables"):
        levels = [row["building_level"]] if row["building_level"] else by_chain.get(row["building_chain"], [])
        target = excluded if row["exclude"] == "true" else included
        for level in levels:
            target.setdefault(level, set()).add(row["building_set"])
    return {level: sets - excluded.get(level, set()) for level, sets in included.items()}


RESOURCE_NAMES = {"troy_food": "Food", "troy_bronze": "Bronze", "troy_gold": "Gold", "troy_stones": "Stone", "troy_wood": "Wood"}


def upkeep_ui_name(overlay: Overlay, resource: str, feature: str) -> str:
    """Tooltip name "Building <Resource> Upkeep" (a bonus value name) of `resource` (troy_<resource>)."""
    name = f"dyn_rebal_building_upkeep_{resource.removeprefix('troy_')}"
    overlay.put("bonus_value_names_tables", {"key": name}, feature)
    overlay.put_loc(f"bonus_value_names_screen_name_{name}", f"Building {RESOURCE_NAMES[resource]} Upkeep", feature)
    return name


def bonus_value_ui(overlay: Overlay, key: str, effect: str, name_id: str, icon: str, percent: bool,
                   positive_is_good: bool, feature: str, designator: str = "") -> None:
    """Tooltip line of `effect`. Without one, the game names an effect on a resource factor after
    the factor (for building upkeep: "Building profit")."""
    overlay.put("bonus_value_uis_tables", {
        "key": key,
        "name_id": name_id,
        "priority": 110 if percent else 100,
        "ui_category_id": "bonus_value_ui_settlements",
        "value_formatting": "bonus_value_formatting_percent" if percent else "bonus_value_formatting_flat",
        "icon": icon,
        "is_positive_value_good": "true" if positive_is_good else "false",
        "show_value": "true",
        "designator_override": "",
        "show_parameters_tooltip": "false",
    }, feature)
    overlay.put("effect_bonus_value_ui_additions_tables", {
        "bonus_value_ui": key,
        "effect": effect,
        "is_positive_override": "true",
        "condition": "",
        "condition_designator": designator,
        "is_description": "false",
    }, feature)
