"""Religion: food production bonuses of the local gods' shrines and dwellings.

- the effect bundles of each favour tier of a god's shrine or dwelling (phar_<...>_effect_bundle_<god>_
  shrine_t<tier>_effect_<n>, ..._dwelling_...): food production effects multiplied
  (RELIGION_FOOD_PRODUCTION_MULTIPLIER)
- the help page buildings of those shrines and dwellings (..._fake_help_pages) show the same values; they
  are set from their vanilla value, replacing the building multiplier of the buildings feature
"""

from __future__ import annotations

import re

from lib.buildings import BEJ, VALUE_COLUMNS
from lib.data import Overlay, fmt_float

FEATURE = "religion"

EBEJ = "effect_bundles_to_effects_junctions_tables"
# Food production: "% to food income" and "% food per turn from buildings" (Yamm).
FOOD_EFFECTS = {"phar_main_percentage_multiplier_mod_food", "phar_main_effect_economy_buildings_multi_food"}
TIER_BUNDLE = re.compile(r"phar_\w+_effect_bundle_(\w+?)_(shrine|dwelling)_t\d+(?:_effect_\d+)?")
HELP_PAGE = re.compile(r"phar_\w+_(?:ers_shrine_\w+|religion_dwelling_\w+)_fake_help_pages")


def apply(overlay: Overlay, settings) -> None:
    factor = settings.RELIGION_FOOD_PRODUCTION_MULTIPLIER
    gods = set()
    bundles = 0
    for row in overlay.rows(EBEJ):
        match = TIER_BUNDLE.fullmatch(row["effect_bundle_key"])
        if match is None or row["effect_key"] not in FOOD_EFFECTS:
            continue
        vanilla = overlay.vanilla(EBEJ, (row["effect_bundle_key"], row["effect_key"]))
        value = round(float((vanilla or row)["value"]) * factor)
        overlay.put(EBEJ, dict(row, value=value), FEATURE)
        gods.add(f"{match.group(1)} ({match.group(2)})")
        bundles += 1
    pages = 0
    for row in overlay.rows(BEJ):
        if not HELP_PAGE.fullmatch(row["building"]) or row["effect"] not in FOOD_EFFECTS:
            continue
        vanilla = overlay.vanilla(BEJ, (row["building"], row["effect"])) or row
        overlay.put(BEJ, dict(row, **{column: fmt_float(round(float(vanilla[column]) * factor))
                                      for column in VALUE_COLUMNS}), FEATURE)
        pages += 1
    overlay.note(FEATURE, f"Food production of the gods' shrines and dwellings x{factor:g}: {bundles} favour tier "
                          f"effects ({', '.join(sorted(gods))}) and {pages} help pages.")
