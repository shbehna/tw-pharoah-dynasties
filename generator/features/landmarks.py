"""Landmarks: rebalanced effects, costs and garrisons (generator/data/landmarks)."""

from __future__ import annotations

from lib.data import GameData, Overlay

FEATURE = "landmarks"
DATA = "landmarks"


def apply(overlay: Overlay, settings) -> None:
    count = 0
    for tsv in overlay.data.data_tables(DATA):
        count += overlay.import_rows(tsv, FEATURE)
    texts = 0
    for loc in overlay.data.data_locs(DATA):
        for key, text, tooltip in loc.rows:
            overlay.put_loc(key, text, FEATURE, tooltip)
            texts += 1
    overlay.note(FEATURE, f"Landmarks rebalanced: {count} table rows and {texts} texts from generator/data/{DATA}.")


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
