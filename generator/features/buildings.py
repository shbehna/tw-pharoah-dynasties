"""Buildings.

- religious building conversions cost stone and wood instead of gold (generator/data/buildings)
- granary, bronzeworker and goldsmith chains
- summer festival grounds and beer hall
- Kushite Delegate School influence
- campaign movement bonus of buildings (outposts excluded)
- every other building's resource production % multiplied, for bonuses that only apply to some resources (food)
  and for every bonus of landmarks
"""

from __future__ import annotations

import collections
import re

from lib.buildings import BEJ, VALUE_COLUMNS, building_levels, set_effect
from lib.data import Overlay, fmt_float

FEATURE = "buildings"

LEGACY_PREFIX = "troy_"
# Province resource chains: (chain, resource, production setting, upkeep setting)
CHAINS = [
    ("phar_main_all_resource_production_modifier_food", "food", "GRANARY_PRODUCTION", "GRANARY_FOOD_UPKEEP"),
    ("phar_main_all_resource_production_modifier_bronze", "bronze", "BRONZEWORKER_PRODUCTION", "BRONZEWORKER_BRONZE_UPKEEP"),
    ("phar_main_all_resource_production_modifier_gold", "gold", "GOLDSMITH_PRODUCTION", "GOLDSMITH_GOLD_UPKEEP"),
]
PROVINCE = "region_to_province_own_text_provincewide"
ARMIES_IN_PROVINCE = "building_to_force_own_provincewide"
SUMMER_FESTIVAL_GROUNDS = "phar_main_all_province_management_happiness_type_a_nile_1"
BEER_HALL = "phar_main_all_province_management_happiness_type_b_2"
FOOD_PRODUCTION = "phar_main_percentage_multiplier_mod_troy_food_buildings"
HAPPINESS = "phar_main_province_management_happiness_building"
TRADING_POST = "_ers_trading_post_"  # set in the outposts section
DELEGATE_SCHOOL = "phar_main_amenmesse_province_management_main_building_production_boost_growth_3"
INFLUENCE = "phar_main_influence_province_management_buildings"
# Own-army campaign movement effects (land, sea, both). Roads' extra bonus at high influence
# (..._influence_bonus) is left out so each building gets the bonus once.
MOVEMENT_EFFECTS = {
    "phar_main_mod_land_movement_campaign_basic",
    "phar_main_movement_sea_mod_buildings",
    "phar_main_mod_ship_movement_campaign_mod_land_movement_campaign_basic",
}
OUTPOST = "_ers_"  # outpost slots, including the unique wonders built in them


def apply(overlay: Overlay, settings) -> None:
    s = settings
    count = 0
    for tsv in overlay.data.data_tables("buildings"):
        count += overlay.import_rows(tsv, FEATURE)
    overlay.note(FEATURE, f"Religious building conversions cost stone and wood instead of gold "
                          f"({count} cost rows, generator/data/buildings).")

    mentioned = _chains(overlay, s)
    mentioned |= _happiness_buildings(overlay, s)
    _multiply_production(overlay, s, mentioned)
    _delegate_school(overlay, s)
    _movement_bonus(overlay, s)


def _delegate_school(overlay: Overlay, s) -> None:
    current = overlay.get(BEJ, (DELEGATE_SCHOOL, INFLUENCE))
    set_effect(overlay, DELEGATE_SCHOOL, INFLUENCE, current["effect_scope"], s.DELEGATE_SCHOOL_INFLUENCE, FEATURE)
    overlay.note(FEATURE, f"Kushite Delegate School: {s.DELEGATE_SCHOOL_INFLUENCE:+g} influence in the province "
                          f"(vanilla {float(current['value']):+g}).")


def _movement_bonus(overlay: Overlay, s) -> None:
    rows = [row for row in overlay.rows(BEJ)
            if row["effect"] in MOVEMENT_EFFECTS and float(row["value"]) > 0
            and not row["building"].startswith(LEGACY_PREFIX) and OUTPOST not in row["building"]]
    for row in rows:
        set_effect(overlay, row["building"], row["effect"], row["effect_scope"],
                   float(row["value"]) + s.BUILDING_MOVEMENT_BONUS, FEATURE)
    overlay.note(FEATURE, f"Campaign movement bonus of buildings +{s.BUILDING_MOVEMENT_BONUS}% "
                          f"({len(rows)} buildings: {', '.join(sorted(row['building'] for row in rows))}).")


def _chains(overlay: Overlay, s) -> set[str]:
    levels = building_levels(overlay)
    done = set()
    for chain, resource, production_setting, upkeep_setting in CHAINS:
        buildings = sorted((b for b, row in levels.items() if row["chain"] == chain), key=lambda b: int(levels[b]["level"]))
        production = getattr(s, production_setting)
        if len(buildings) != len(production):
            raise RuntimeError(f"{chain}: expected {len(production)} levels, found {buildings}")
        effect = f"phar_main_percentage_multiplier_mod_troy_{resource}_buildings"
        for building, value in zip(buildings, production):
            set_effect(overlay, building, effect, PROVINCE, value, FEATURE)
        upkeep = getattr(s, upkeep_setting)
        set_effect(overlay, buildings[-1], f"phar_main_unit_upkeep_cost_percentage_multiplier_mod_{resource}",
                   ARMIES_IN_PROVINCE, upkeep, FEATURE)
        done.update(buildings)
        overlay.note(FEATURE, f"{chain}: +{'/'.join(map(str, production))}% {resource} production; last level also "
                              f"{upkeep:g}% {resource} upkeep for armies in the province.")
    return done


def _happiness_buildings(overlay: Overlay, s) -> set[str]:
    festival_food = overlay.get(BEJ, (SUMMER_FESTIVAL_GROUNDS, FOOD_PRODUCTION))
    set_effect(overlay, SUMMER_FESTIVAL_GROUNDS, FOOD_PRODUCTION, festival_food["effect_scope"],
               s.SUMMER_FESTIVAL_FOOD_PRODUCTION, FEATURE)
    set_effect(overlay, SUMMER_FESTIVAL_GROUNDS, HAPPINESS, PROVINCE, s.SUMMER_FESTIVAL_HAPPINESS, FEATURE)
    set_effect(overlay, BEER_HALL, FOOD_PRODUCTION, festival_food["effect_scope"], s.BEER_HALL_FOOD_PRODUCTION, FEATURE)
    overlay.note(FEATURE, f"Summer Festival Grounds: +{s.SUMMER_FESTIVAL_FOOD_PRODUCTION}% food production, "
                          f"+{s.SUMMER_FESTIVAL_HAPPINESS} happiness. Beer Hall (also Wine/Performance Hall for other "
                          f"cultures): +{s.BEER_HALL_FOOD_PRODUCTION}% food production.")
    return {SUMMER_FESTIVAL_GROUNDS, BEER_HALL}


def production_effects(overlay: Overlay) -> dict[str, set[str]]:
    """Effects that change resource production by a percentage -> resources they apply to (troy_food, ...)."""
    resource_of_factor = {row["unique_id"]: row["resource"] for row in overlay.rows("pooled_resource_factor_junctions_tables")}
    effects: dict[str, set[str]] = collections.defaultdict(set)
    for row in overlay.rows("effect_bonus_value_pooled_resource_factor_junctions_tables"):
        if row["bonus_value_id"] == "percentage_multiplier_mod":
            effects[row["effect"]].add(resource_of_factor.get(row["resource_factor"], row["resource_factor"]))
    return effects


def _multiply_production(overlay: Overlay, s, mentioned: set[str]) -> None:
    factor = s.OTHER_PRODUCTION_MULTIPLIER
    excluded = [re.compile(p) for p in s.OTHER_PRODUCTION_EXCLUDE]
    all_resources = [re.compile(p) for p in s.OTHER_PRODUCTION_ALL_RESOURCES]
    resources = {f"troy_{resource}" for resource in s.OTHER_PRODUCTION_RESOURCES}
    all_effects = production_effects(overlay)
    effects = {effect for effect, applies_to in all_effects.items() if applies_to <= resources}
    per_effect = collections.Counter()
    for row in list(overlay.rows(BEJ)):
        building = row["building"]
        doubled = all_effects if any(p.search(building) for p in all_resources) else effects
        if (
            row["effect"] not in doubled
            or building.startswith(LEGACY_PREFIX)
            or building in mentioned
            or TRADING_POST in building
            or any(p.search(building) for p in excluded)
            or float(row["value"]) <= 0
        ):
            continue
        for column in VALUE_COLUMNS:
            row[column] = fmt_float(float(row[column]) * factor)
        overlay.put(BEJ, row, FEATURE)
        per_effect[row["effect"]] += 1
    total = sum(per_effect.values())
    detail = ", ".join(f"{effect} ({count})" for effect, count in sorted(per_effect.items()))
    overlay.note(FEATURE, f"Production % multiplied by {factor:g} on {total} building effects (bonuses that only "
                          f"apply to {', '.join(s.OTHER_PRODUCTION_RESOURCES)}, and every bonus of buildings matching "
                          f"{', '.join(s.OTHER_PRODUCTION_ALL_RESOURCES)}): {detail}.")
