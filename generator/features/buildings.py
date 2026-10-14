"""Buildings.

- religious building conversions cost stone and wood instead of gold (generator/data/buildings)
- granary, bronzeworker and goldsmith chains
- summer festival grounds and beer hall
- Kushite Delegate School influence
- campaign movement bonus of buildings (outposts excluded)
- every other building's resource production % multiplied, for bonuses that only apply to some resources (food)
  and for every bonus of landmarks
- per-turn upkeep of a share of the construction cost (administration, management and religious buildings)
"""

from __future__ import annotations

import collections
import math
import re

from lib.buildings import (BEJ, UPKEEP_FACTOR, VALUE_COLUMNS, bonus_value_ui, building_levels, building_sets, set_effect,
                           upkeep_ui_name)
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
UPKEEP_COST = "dyn_rebal_building_upkeep_"
UPKEEP_DISPLAY_GOLD = "phar_main_dummy_building_gold_upkeep"
RUIN_SUFFIXES = ("_ruin", "_ruins")


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
    _upkeep(overlay, s)


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


def _upkeep(overlay: Overlay, s) -> None:
    resource_of = {row["unique_id"]: row["resource"] for row in overlay.rows("pooled_resource_factor_junctions_tables")}
    upkeep_factor = {row["resource"]: row["unique_id"] for row in overlay.rows("pooled_resource_factor_junctions_tables")
                     if row["factor"] == UPKEEP_FACTOR}
    costs: dict[str, dict[str, float]] = collections.defaultdict(dict)
    for row in overlay.rows("resource_cost_pooled_resource_junctions_tables"):
        costs[row["resource_cost"]][row["pooled_resource_factor"]] = float(row["amount"])
    sets = building_sets(overlay)
    included, excluded = set(s.BUILDING_UPKEEP_SETS), set(s.BUILDING_UPKEEP_EXCLUDED_SETS)
    unknown = sorted((included | excluded) - set().union(*sets.values()))
    if unknown:
        raise ValueError(f"BUILDING_UPKEEP_SETS / BUILDING_UPKEEP_EXCLUDED_SETS: unknown building sets {unknown}")

    per_set = collections.Counter()
    for level in list(overlay.rows("building_levels_tables")):
        name = level["level_name"]
        level_sets = sets.get(name, set())
        if name.startswith(LEGACY_PREFIX) or not level_sets & included or level_sets & excluded:
            continue
        if name.endswith(RUIN_SUFFIXES):
            continue  # abandoned settlements and landmarks: a placeholder cost of 1 stone, no upkeep
        build: dict[str, float] = collections.Counter()
        for factor, amount in costs.get(level["create_resource_cost"], {}).items():
            if amount < 0:
                build[resource_of[factor]] -= amount
        upkeep = dict(costs.get(level["upkeep_resource_cost"], {}))
        has_upkeep = {resource_of[factor] for factor in upkeep}
        for resource, amount in build.items():
            value = math.ceil(amount * s.BUILDING_UPKEEP_PERCENT / (100 * s.BUILDING_UPKEEP_ROUNDING)) * s.BUILDING_UPKEEP_ROUNDING
            if resource not in has_upkeep and value > 0:
                upkeep[upkeep_factor[resource]] = -value
        if upkeep == costs.get(level["upkeep_resource_cost"], {}):
            continue
        # Levels with the same upkeep share one resource cost, named after the amounts.
        cost_id = UPKEEP_COST + "_".join(f"{resource_of[f].removeprefix('troy_')}{-a:g}" for f, a in sorted(upkeep.items()))
        overlay.put("resource_costs_tables", {"id": cost_id, "treasury_cost": 0,
                                              "expenditure_type": "CONSTRUCTION_OTHER", "income_type": "OTHER"}, FEATURE)
        for factor, amount in upkeep.items():
            overlay.put("resource_cost_pooled_resource_junctions_tables",
                        {"pooled_resource_factor": factor, "resource_cost": cost_id, "amount": amount}, FEATURE)
        overlay.put("building_levels_tables", dict(level, upkeep_resource_cost=cost_id), FEATURE)
        # The upkeep itself does not show on the building: like vanilla, a display-only effect shows it.
        for factor, amount in upkeep.items():
            effect = _upkeep_display_effect(overlay, resource_of[factor])
            if overlay.get(BEJ, (name, effect)) is None:
                overlay.put(BEJ, {"building": name, "effect": effect, "effect_scope": "region_to_region_own",
                                  **{column: fmt_float(amount) for column in VALUE_COLUMNS}}, FEATURE)
        per_set["+".join(sorted(level_sets & included))] += 1
    overlay.note(FEATURE, f"Building upkeep: {s.BUILDING_UPKEEP_PERCENT}% of the construction cost per turn, rounded "
                          f"up to {s.BUILDING_UPKEEP_ROUNDING}, existing upkeep kept per resource ("
                          + ", ".join(f"{count} levels of {name}" for name, count in sorted(per_set.items())) + ").")


def _upkeep_display_effect(overlay: Overlay, resource: str) -> str:
    """Display-only effect "Building <Resource> Upkeep: -N" of `resource` (troy_<resource>). Vanilla has
    one for gold, used by its few buildings with an upkeep; the others are new."""
    if resource == "troy_gold":
        return UPKEEP_DISPLAY_GOLD
    short = resource.removeprefix("troy_").removesuffix("s")
    effect = f"dyn_rebal_dummy_building_{short}_upkeep"
    overlay.put("effects_tables", dict(overlay.get("effects_tables", (UPKEEP_DISPLAY_GOLD,)), effect=effect,
                                       icon=f"fx_icon_{short}_income.png", icon_negative=f"fx_icon_{short}_upkeep.png"),
                FEATURE)
    overlay.put_loc(f"effects_description_{effect}", f"%+n to {short} income per turn due to building upkeep", FEATURE)
    bonus_value_ui(overlay, f"dyn_rebal_dummy_{short}_upkeep", effect, upkeep_ui_name(overlay, resource, FEATURE),
                   f"icon_effect_{short}_income.png", percent=False, positive_is_good=True, feature=FEATURE,
                   designator="bonus_value_condition_designator_resource")
    return effect
