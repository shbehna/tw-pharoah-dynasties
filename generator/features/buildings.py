"""Buildings.

- religious building conversions cost stone and wood instead of gold (RELIGIOUS_CONVERSION_COSTS)
- granary, bronzeworker and goldsmith chains
- summer festival grounds and beer hall
- Kushite Delegate School influence
- administration and management buildings: tax administration, Wisdom Codices, Bazaar of the Arts, Surgeon's
  Practice, Lawagetas' Palace, roads, management buildings built on a special resource
- campaign movement bonus of buildings (outposts excluded)
- every other building's resource production % multiplied, for bonuses that only apply to some resources (food)
  and for every bonus of landmarks
- per-turn upkeep of a share of the construction cost (administration, management and religious buildings,
  landmarks)
"""

from __future__ import annotations

import collections
import math
import re

from lib.buildings import (BEJ, UPKEEP_FACTOR, VALUE_COLUMNS, bonus_value_ui, building_levels, building_sets,
                           effects_by_building, new_values, set_effect, upkeep_ui_name)
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
# Administration and management chains
TAX_CHAINS = ["phar_main_major_main_building_production_boost_overall",
              "phar_main_major_main_building_poc_production_boost_overall"]
TAX_PRODUCTION = "phar_effect_economy_ers_trading_post_mod_all_resources"  # all resources in the province
WISDOM_CODICES_CHAINS = ["phar_main_major_main_building_legitimacy_influence_boost",  # 2 levels
                         "phar_main_major_poc_main_building_legitimacy_influence_boost"]
DECREE_RATE = "phar_main_research_rate_mod_buildings"  # unused in vanilla
BAZAAR_CHAIN = "phar_main_happiness_type_c"
SURGEON_CHAIN = "phar_main_growth_type_a"
LAWAGETAS_CHAIN = "phar_map_myc_province_management_eqeta"
ROAD_CHAINS = ["phar_main_roads", "phar_map_myc_province_management_roads"]
WORKFORCE_GROWTH = "phar_main_province_development_growth_added_building"
ADJACENT_PRODUCTION = "phar_effect_resource_mod_all_buildings_adjacent"  # as Bay's Chief Scribe's Headquarters
ADJACENT_PROVINCES = "province_to_adjacent_province_own"
MANAGEMENT_SET = "phar_main_province_management"
RESOURCE_DERIVATIVE = "_derivative"  # buildings unlocked by a special resource of the region
# Own-army campaign movement effects (land, sea, both). Roads' extra bonus at high influence
# (..._influence_bonus) is left out so each building gets the bonus once.
MOVEMENT_EFFECTS = {
    "phar_main_mod_land_movement_campaign_basic",
    "phar_main_movement_sea_mod_buildings",
    "phar_main_mod_ship_movement_campaign_mod_land_movement_campaign_basic",
}
OUTPOST = "_ers_"  # outpost slots, including the unique wonders built in them
UPKEEP_EFFECT = "troy_effect_economy_building_upkeep_add_"  # + resource: flat building upkeep (negative values)
RUIN_SUFFIXES = ("_ruin", "_ruins")
POOLED_COSTS = "resource_cost_pooled_resource_junctions_tables"
# Wood per turn of a building: base wood, or port wood (WOOD_PRODUCTION).
WOOD_EFFECTS = {"phar_main_building_wood_base_amount", "phar_main_base_amount_troy_wood_phar_main_ports"}
GOLD_COST, STONE_COST, WOOD_COST = "troy_gold_buildings", "troy_stones_buildings", "troy_wood_buildings"


def apply(overlay: Overlay, settings) -> None:
    s = settings
    _conversion_costs(overlay, s)

    mentioned = _chains(overlay, s)
    mentioned |= _happiness_buildings(overlay, s)
    mentioned |= _management_buildings(overlay, s)
    _multiply_production(overlay, s, mentioned)
    _delegate_school(overlay, s)
    _movement_bonus(overlay, s)
    # After the movement bonus, so the chain values are not raised by it.
    _chain_effects(overlay, s)
    _wood_production(overlay, s)
    _construction_time(overlay, s)
    _upkeep(overlay, s)


def _conversion_costs(overlay: Overlay, s) -> None:
    """Religious building conversions cost stone and wood instead of gold (RELIGIOUS_CONVERSION_COSTS)."""
    costs = collections.defaultdict(set)
    for row in overlay.rows(POOLED_COSTS):
        costs[row["resource_cost"]].add(row["pooled_resource_factor"])
    count = 0
    for cost, factors in sorted(costs.items()):
        if GOLD_COST not in factors:
            continue
        for pattern, spec in s.RELIGIOUS_CONVERSION_COSTS:
            match = re.fullmatch(pattern, cost)
            if not match:
                continue
            if isinstance(spec, dict):
                level = int(match.group(1))
                if level not in spec:
                    raise ValueError(f"RELIGIOUS_CONVERSION_COSTS: no level {level} in {pattern} for {cost}")
                spec = spec[level]
            stone, wood = spec
            for factor, amount in ((GOLD_COST, 0), (STONE_COST, -stone), (WOOD_COST, -wood)):
                overlay.put(POOLED_COSTS, {"pooled_resource_factor": factor, "resource_cost": cost,
                                           "amount": amount}, FEATURE)
            count += 1
            break
    overlay.note(FEATURE, f"Religious building conversions cost stone and wood instead of gold "
                          f"({count} conversions, RELIGIOUS_CONVERSION_COSTS).")


def _delegate_school(overlay: Overlay, s) -> None:
    current = overlay.get(BEJ, (DELEGATE_SCHOOL, INFLUENCE))
    set_effect(overlay, DELEGATE_SCHOOL, INFLUENCE, current["effect_scope"], s.DELEGATE_SCHOOL_INFLUENCE, FEATURE)
    overlay.note(FEATURE, f"Kushite Delegate School: {s.DELEGATE_SCHOOL_INFLUENCE:+g} influence in the province "
                          f"(vanilla {float(current['value']):+g}).")


def _chain_levels(levels: dict[str, dict], chain: str, count: int) -> list[str]:
    buildings = sorted((b for b, row in levels.items() if row["chain"] == chain), key=lambda b: int(levels[b]["level"]))
    if len(buildings) != count:
        raise RuntimeError(f"{chain}: expected {count} levels, found {buildings}")
    return buildings


def _set_chain(overlay: Overlay, levels: dict[str, dict], chain: str, effect: str, values: list[float],
               scope: str | None = None) -> list[str]:
    """Set `effect` on each level of `chain`; without `scope`, levels that lack the effect take the scope of
    the chain's existing rows."""
    buildings = _chain_levels(levels, chain, len(values))
    existing = [row for b in buildings if (row := overlay.get(BEJ, (b, effect))) is not None]
    for building, value in zip(buildings, values):
        current = overlay.get(BEJ, (building, effect))
        row_scope = scope or (current or existing[0])["effect_scope"]
        set_effect(overlay, building, effect, row_scope, value, FEATURE)
    return buildings


def _management_buildings(overlay: Overlay, s) -> set[str]:
    levels = building_levels(overlay)
    tax = []
    for chain in TAX_CHAINS:
        tax += _set_chain(overlay, levels, chain, TAX_PRODUCTION, s.TAX_ADMINISTRATION_PRODUCTION)
    overlay.note(FEATURE, f"Tax administration chains: +{'/'.join(map(str, s.TAX_ADMINISTRATION_PRODUCTION))}% "
                          f"to all resources produced in the province.")

    rates = s.WISDOM_CODICES_DECREE_RATE
    _set_chain(overlay, levels, WISDOM_CODICES_CHAINS[0], DECREE_RATE, rates[:2], "building_to_faction_own")
    _set_chain(overlay, levels, WISDOM_CODICES_CHAINS[1], DECREE_RATE, rates, "building_to_faction_own")
    overlay.note(FEATURE, f"Wisdom Codices chains: +{'/'.join(f'{v:g}' for v in rates)}% royal decree completion rate.")

    _set_chain(overlay, levels, BAZAAR_CHAIN, HAPPINESS, s.BAZAAR_OF_THE_ARTS_HAPPINESS)
    _set_chain(overlay, levels, SURGEON_CHAIN, WORKFORCE_GROWTH, s.SURGEONS_PRACTICE_WORKFORCE_GROWTH)
    lawagetas = _set_chain(overlay, levels, LAWAGETAS_CHAIN, HAPPINESS, s.LAWAGETAS_PALACE_HAPPINESS)
    set_effect(overlay, lawagetas[-1], INFLUENCE, overlay.get(BEJ, (lawagetas[-1], INFLUENCE))["effect_scope"],
               s.LAWAGETAS_PALACE_INFLUENCE, FEATURE)
    overlay.note(FEATURE, f"Bazaar of the Arts chain: +{'/'.join(map(str, s.BAZAAR_OF_THE_ARTS_HAPPINESS))} happiness. "
                          f"Surgeon's Practice chain: +{'/'.join(map(str, s.SURGEONS_PRACTICE_WORKFORCE_GROWTH))} workforce "
                          f"growth. Lawagetas' Palace chain: +{'/'.join(map(str, s.LAWAGETAS_PALACE_HAPPINESS))} happiness, "
                          f"last level +{s.LAWAGETAS_PALACE_INFLUENCE} influence.")

    for chain in ROAD_CHAINS:
        _set_chain(overlay, levels, chain, ADJACENT_PRODUCTION, s.ROADS_ADJACENT_PRODUCTION, ADJACENT_PROVINCES)
    overlay.note(FEATURE, f"Road chains: +{'/'.join(map(str, s.ROADS_ADJACENT_PRODUCTION))}% to all resources produced "
                          f"in adjacent provinces.")

    sets = building_sets(overlay)
    growth = sorted(row["building"] for row in overlay.rows(BEJ)
                    if row["effect"] == WORKFORCE_GROWTH and RESOURCE_DERIVATIVE in row["building"]
                    and MANAGEMENT_SET in sets.get(row["building"], set()) and float(row["value"]) > 0
                    and not row["building"].startswith(LEGACY_PREFIX))
    for building in growth:
        # New values rather than rescaled ones: the Assuwa and Thrace Olive Groves have inconsistent
        # vanilla values (growth when ruined; none when damaged or at low and medium influence).
        row = overlay.get(BEJ, (building, WORKFORCE_GROWTH))
        row.update(new_values(s.RESOURCE_MANAGEMENT_WORKFORCE_GROWTH))
        overlay.put(BEJ, row, FEATURE)
    overlay.note(FEATURE, f"Management buildings on a special resource: +{s.RESOURCE_MANAGEMENT_WORKFORCE_GROWTH} "
                          f"workforce growth ({', '.join(growth)}).")
    return set(tax)


def _movement_bonus(overlay: Overlay, s) -> None:
    rows = [row for row in overlay.rows(BEJ)
            if row["effect"] in MOVEMENT_EFFECTS and float(row["value"]) > 0
            and not row["building"].startswith(LEGACY_PREFIX) and OUTPOST not in row["building"]]
    for row in rows:
        set_effect(overlay, row["building"], row["effect"], row["effect_scope"],
                   float(row["value"]) + s.BUILDING_MOVEMENT_BONUS, FEATURE)
    overlay.note(FEATURE, f"Campaign movement bonus of buildings +{s.BUILDING_MOVEMENT_BONUS}% "
                          f"({len(rows)} buildings: {', '.join(sorted(row['building'] for row in rows))}).")


def _matching_chains(levels: dict[str, dict], pattern: str, setting: str) -> dict[str, list[str]]:
    """Chains whose key matches `pattern` -> their levels in order (ruins left out)."""
    chains: dict[str, list[str]] = collections.defaultdict(list)
    for building, row in levels.items():
        if re.fullmatch(pattern, row["chain"]) and not building.endswith(RUIN_SUFFIXES):
            chains[row["chain"]].append(building)
    if not chains:
        raise ValueError(f"{setting}: no building chain matches {pattern}")
    return {chain: sorted(buildings, key=lambda b: int(levels[b]["level"])) for chain, buildings in chains.items()}


def _chain_effects(overlay: Overlay, s) -> None:
    levels = building_levels(overlay)
    for pattern, effect, scope, values in s.BUILDING_CHAIN_EFFECTS:
        chains = _matching_chains(levels, pattern, "BUILDING_CHAIN_EFFECTS")
        for buildings in chains.values():
            for building, value in zip(buildings, values):
                set_effect(overlay, building, effect, scope, value, FEATURE)
        overlay.note(FEATURE, f"{effect} ({scope}) {'/'.join(f'{v:+g}' for v in values)} by level on "
                              f"{len(chains)} chains: {', '.join(sorted(chains))}.")


def _wood_production(overlay: Overlay, s) -> None:
    levels = building_levels(overlay)
    effects = effects_by_building(overlay)
    changed = 0
    for chain, values in s.WOOD_PRODUCTION.items():
        buildings = _matching_chains(levels, re.escape(chain), "WOOD_PRODUCTION")[chain]
        if len(buildings) != len(values):
            raise ValueError(f"WOOD_PRODUCTION: {chain} has {len(buildings)} levels ({', '.join(buildings)}), "
                             f"not {len(values)}")
        for building, value in zip(buildings, values):
            rows = [row for row in effects.get(building, []) if row["effect"] in WOOD_EFFECTS]
            if len(rows) != 1:
                raise ValueError(f"WOOD_PRODUCTION: {building} needs exactly one of {sorted(WOOD_EFFECTS)}")
            changed += set_effect(overlay, building, rows[0]["effect"], rows[0]["effect_scope"], value, FEATURE)
    overlay.note(FEATURE, f"Wood per turn of {len(s.WOOD_PRODUCTION)} wood chains (WOOD_PRODUCTION): "
                          f"{changed} building levels changed.")


def _construction_time(overlay: Overlay, s) -> None:
    levels = building_levels(overlay)
    for pattern, turns in s.BUILDING_CONSTRUCTION_TIME:
        chains = _matching_chains(levels, pattern, "BUILDING_CONSTRUCTION_TIME")
        for buildings in chains.values():
            for building in buildings:
                row = dict(levels[building])
                row["create_time"] = max(1, int(row["create_time"]) + turns)
                overlay.put("building_levels_tables", row, FEATURE)
        overlay.note(FEATURE, f"Construction time {turns:+d} turns on {len(chains)} chains: {', '.join(sorted(chains))}.")


def _chains(overlay: Overlay, s) -> set[str]:
    levels = building_levels(overlay)
    done = set()
    for chain, resource, production_setting, upkeep_setting in CHAINS:
        production = getattr(s, production_setting)
        buildings = _chain_levels(levels, chain, len(production))
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
    """Building upkeep as effects that add to the resource's building upkeep factor, like the effects that add
    to building production. A % effect on the factor (administration tiers, AI difficulty) scales effects
    only: a fixed upkeep cost (building_levels upkeep_resource_cost) would not change."""
    factors = list(overlay.rows("pooled_resource_factor_junctions_tables"))
    resource_of = {row["unique_id"]: row["resource"] for row in factors}
    upkeep_factors = {row["unique_id"] for row in factors if row["factor"] == UPKEEP_FACTOR}
    # Effects adding a flat amount to a building upkeep factor -> resource (troy_<resource>).
    upkeep_effects = {row["effect"]: resource_of[row["resource_factor"]]
                      for row in overlay.rows("effect_bonus_value_pooled_resource_factor_junctions_tables")
                      if row["bonus_value_id"] == "base_amount" and row["resource_factor"] in upkeep_factors}
    effect_of = {resource: effect for effect, resource in upkeep_effects.items() if effect.startswith(UPKEEP_EFFECT)}
    costs: dict[str, dict[str, float]] = collections.defaultdict(dict)
    for row in overlay.rows("resource_cost_pooled_resource_junctions_tables"):
        costs[row["resource_cost"]][row["pooled_resource_factor"]] = float(row["amount"])
    effects = effects_by_building(overlay)
    sets = building_sets(overlay)
    included, excluded = set(s.BUILDING_UPKEEP_SETS), set(s.BUILDING_UPKEEP_EXCLUDED_SETS)
    unknown = sorted((included | excluded) - set().union(*sets.values()))
    if unknown:
        raise ValueError(f"BUILDING_UPKEEP_SETS / BUILDING_UPKEEP_EXCLUDED_SETS: unknown building sets {unknown}")

    per_set = collections.Counter()
    used = set()
    for level in overlay.rows("building_levels_tables"):
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
        # Vanilla upkeep, as a fixed cost or an effect, is kept for its resource.
        has_upkeep = {resource_of[factor] for factor in costs.get(level["upkeep_resource_cost"], {})}
        has_upkeep |= {upkeep_effects[e["effect"]] for e in effects.get(name, []) if e["effect"] in upkeep_effects}
        added = False
        for resource, amount in sorted(build.items()):
            value = math.ceil(amount * s.BUILDING_UPKEEP_PERCENT / (100 * s.BUILDING_UPKEEP_ROUNDING)) * s.BUILDING_UPKEEP_ROUNDING
            if resource in has_upkeep or value <= 0:
                continue
            # Negative: the factor counts income. Damaged buildings pay in full, ruined ones nothing.
            row = {"building": name, "effect": effect_of[resource], "effect_scope": "region_to_region_own"}
            row.update(new_values(-value, damaged=-value))
            overlay.put(BEJ, row, FEATURE)
            used.add(resource)
            added = True
        if added:
            per_set["+".join(sorted(level_sets & included))] += 1
    for resource in sorted(used):
        short = resource.removeprefix("troy_").removesuffix("s")
        bonus_value_ui(overlay, f"dyn_rebal_building_upkeep_add_{short}", effect_of[resource],
                       upkeep_ui_name(overlay, resource, FEATURE), f"icon_effect_{short}_income.png",
                       percent=False, positive_is_good=True, feature=FEATURE,
                       designator="bonus_value_condition_designator_resource")
    overlay.note(FEATURE, f"Building upkeep: {s.BUILDING_UPKEEP_PERCENT}% of the construction cost per turn, rounded "
                          f"up to {s.BUILDING_UPKEEP_ROUNDING}, as {UPKEEP_EFFECT}<resource> effects; existing upkeep "
                          f"kept per resource ("
                          + ", ".join(f"{count} levels of {name}" for name, count in sorted(per_set.items())) + ").")
