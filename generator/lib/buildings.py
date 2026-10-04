"""Helpers for building_effects_junction_tables rows."""

from __future__ import annotations

import math

from .data import Overlay, fmt_float

BEJ = "building_effects_junction_tables"
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
        out[column] = fmt_float(_round_like(original, original * factor))
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
