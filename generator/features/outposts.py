"""Outposts (extra region slots, "ERS")."""

from __future__ import annotations

from lib.buildings import BEJ, effects_by_building, set_effect
from lib.data import Overlay

FEATURE = "outposts"

# Every outpost type has a "dummy_army_interact_<type>" effect; it identifies all culture variants.
INTERACT = "phar_main_dummy_army_interact_"
TRADING_POST_EFFECT = "phar_effect_economy_ers_trading_post_mod_all_resources_regionwide"
FORT_UPKEEP_DUMMY = "phar_main_dummy_ers_fort_upkeep"
FORT_UPKEEP_UI = "dummy_fort_ers_upkeep"
REFUGE_UPKEEP_DUMMY = "dyn_rebal_dummy_ers_refugee_upkeep"
HAPPINESS = "phar_main_province_management_happiness_building"
ENEMY_MOVEMENT_REGION = "phar_main_mod_land_movement_campaign_debuff"  # "...of enemy armies starting the turn here"
ENEMY_MOVEMENT_PROVINCE = "dyn_rebal_mod_land_movement_campaign_debuff_province"
OWN_MOVEMENT = "phar_main_mod_land_movement_campaign_basic"  # the effect of roads


def _outposts(overlay: Overlay, kind: str, key_part: str) -> list[str]:
    """Buildings of one outpost type. `key_part` keeps out e.g. unique wonders that share the monument interaction."""
    return sorted(
        building
        for building, effects in effects_by_building(overlay).items()
        if key_part in building and any(e["effect"] == INTERACT + kind for e in effects)
    )


def lookout_posts(overlay: Overlay) -> list[str]:
    return _outposts(overlay, "outpost", "_ers_outpost_")


def apply(overlay: Overlay, settings) -> None:
    s = settings
    _trading_posts(overlay, s)
    _forts_and_refuges(overlay, s)
    _waystations(overlay, s)
    _enemy_movement(overlay, s)
    _own_movement(overlay, s)


def _trading_posts(overlay: Overlay, s) -> None:
    buildings = _outposts(overlay, "trading_post", "_ers_trading_post_")
    for building in buildings:
        set_effect(overlay, building, TRADING_POST_EFFECT, "building_to_region",
                   s.TRADING_POST_RESOURCE_PRODUCTION, FEATURE, damaged=0)
    overlay.note(FEATURE, f"Trading posts ({len(buildings)}): +{s.TRADING_POST_RESOURCE_PRODUCTION}% to all "
                          f"resources produced in the region.")


def _forts_and_refuges(overlay: Overlay, s) -> None:
    for variable, value in (
        ("fort_garrison_max_units", s.FORT_MAX_UNITS),
        ("refugee_camp_garrison_max_units", s.WARRIORS_REFUGE_MAX_UNITS),
        ("fort_garrison_units_upkeep_modifier_percentage", -s.FORT_UPKEEP_REDUCTION),
        ("refugee_camp_garrison_units_upkeep_modifier_percentage", -s.WARRIORS_REFUGE_UPKEEP_REDUCTION),
    ):
        overlay.put("campaign_variables_tables", {"variable_key": variable, "value": value}, FEATURE)

    # Forts: the upkeep reduction itself is the campaign variable above; the
    # building effect only shows it in the UI.
    forts = _outposts(overlay, "fort", "_ers_fort")
    for building in forts:
        if overlay.get(BEJ, (building, FORT_UPKEEP_DUMMY)) is not None:
            set_effect(overlay, building, FORT_UPKEEP_DUMMY, "building_to_region_unseen",
                       -s.FORT_UPKEEP_REDUCTION, FEATURE, damaged=0)
    overlay.put_loc(f"effects_description_{FORT_UPKEEP_DUMMY}",
                    f"-{s.FORT_UPKEEP_REDUCTION}% to upkeep of army units stationed in the fort", FEATURE)
    overlay.put_loc(f"effect_bonus_value_ui_additions_value_override_{FORT_UPKEEP_DUMMY}{FORT_UPKEEP_UI}",
                    f"-{s.FORT_UPKEEP_REDUCTION}%", FEATURE)

    # Warriors' Refuges have no upkeep reduction in vanilla: add a UI effect like the fort's.
    overlay.put("effects_tables", dict(overlay.get("effects_tables", (FORT_UPKEEP_DUMMY,)), effect=REFUGE_UPKEEP_DUMMY), FEATURE)
    overlay.put("effect_bonus_value_ui_additions_tables", dict(
        overlay.get("effect_bonus_value_ui_additions_tables", (FORT_UPKEEP_UI, FORT_UPKEEP_DUMMY)),
        effect=REFUGE_UPKEEP_DUMMY), FEATURE)
    overlay.put_loc(f"effects_description_{REFUGE_UPKEEP_DUMMY}",
                    f"-{s.WARRIORS_REFUGE_UPKEEP_REDUCTION}% to upkeep of army units stationed in the refuge", FEATURE)
    overlay.put_loc(f"effect_bonus_value_ui_additions_value_override_{REFUGE_UPKEEP_DUMMY}{FORT_UPKEEP_UI}",
                    f"-{s.WARRIORS_REFUGE_UPKEEP_REDUCTION}%", FEATURE)
    refuges = _outposts(overlay, "refugee", "_ers_refugee_")
    for building in refuges:
        set_effect(overlay, building, REFUGE_UPKEEP_DUMMY, "building_to_region_unseen",
                   -s.WARRIORS_REFUGE_UPKEEP_REDUCTION, FEATURE, damaged=0)

    # Advice texts quote the vanilla capacities.
    overlay.put_loc("advice_info_texts_localised_text_phar_camp_info_ers_fort_03",
                    "In order to Garrison Armies at a Fort, an Army must physically visit its location. "
                    f"A Fort can hold up to {s.FORT_MAX_UNITS} units (a regular Army holds 20).", FEATURE)
    overlay.put_loc("advice_info_texts_localised_text_phar_sea_camp_info_refugee_camp_02",
                    f"This outpost provides a small garrison of units (up to {s.WARRIORS_REFUGE_MAX_UNITS}), which "
                    "reinforce all your battles in the region and require upkeep "
                    f"(reduced by {s.WARRIORS_REFUGE_UPKEEP_REDUCTION}%). Each turn there's a chance that a new unit "
                    "will be added to the garrison, but you can stop this when you wish.", FEATURE)
    overlay.note(FEATURE, f"Forts ({len(forts)}): hold {s.FORT_MAX_UNITS} units, -{s.FORT_UPKEEP_REDUCTION}% upkeep. "
                          f"Warriors' Refuges ({len(refuges)}): hold {s.WARRIORS_REFUGE_MAX_UNITS} units, "
                          f"-{s.WARRIORS_REFUGE_UPKEEP_REDUCTION}% upkeep.")


def _waystations(overlay: Overlay, s) -> None:
    buildings = _outposts(overlay, "waystation", "_ers_waystation_")
    for building in buildings:
        set_effect(overlay, building, HAPPINESS, "region_to_province_own_text_provincewide",
                   s.WAYSTATION_HAPPINESS, FEATURE, damaged=0)
    overlay.note(FEATURE, f"Waystations ({len(buildings)}): +{s.WAYSTATION_HAPPINESS} happiness in the province.")


def _enemy_movement(overlay: Overlay, s) -> None:
    # A building can only have each effect once, so the province-wide part uses its own effect key
    # (same bonus value as the vanilla region debuff).
    overlay.put("effects_tables", dict(overlay.get("effects_tables", (ENEMY_MOVEMENT_REGION,)),
                                       effect=ENEMY_MOVEMENT_PROVINCE), FEATURE)
    overlay.put("effect_bonus_value_basic_junction_tables",
                {"effect": ENEMY_MOVEMENT_PROVINCE, "bonus_value_id": "mod_land_movement_campaign"}, FEATURE)
    overlay.put_loc(f"effects_description_{ENEMY_MOVEMENT_PROVINCE}",
                    "%+n% to campaign movement range of enemy armies starting the turn in this province", FEATURE)

    monuments = _outposts(overlay, "monument", "_ers_monument_")
    for building in monuments:
        set_effect(overlay, building, ENEMY_MOVEMENT_PROVINCE, "region_to_force_enemy_provincewide",
                   s.MONUMENT_ENEMY_MOVEMENT_PROVINCE, FEATURE, damaged=0)
    lookouts = lookout_posts(overlay)
    for building in lookouts:
        set_effect(overlay, building, ENEMY_MOVEMENT_REGION, "region_to_force_enemy",
                   s.LOOKOUT_ENEMY_MOVEMENT_REGION, FEATURE, damaged=0)
        set_effect(overlay, building, ENEMY_MOVEMENT_PROVINCE, "region_to_force_enemy_provincewide",
                   s.LOOKOUT_ENEMY_MOVEMENT_PROVINCE, FEATURE, damaged=0)
    overlay.note(FEATURE, f"Monuments ({len(monuments)}): {s.MONUMENT_ENEMY_MOVEMENT_PROVINCE:g}% movement for enemy "
                          f"armies in the province. Lookout posts ({len(lookouts)}): "
                          f"{s.LOOKOUT_ENEMY_MOVEMENT_REGION:g}% in the region and "
                          f"{s.LOOKOUT_ENEMY_MOVEMENT_PROVINCE:g}% in the province (they stack in the outpost's region).")


def _own_movement(overlay: Overlay, s) -> None:
    # Effects of different buildings add up, so several outposts in a region or province stack.
    notes = []
    for name, kind, key_part, scope, area, value in (
        ("Forts", "fort", "_ers_fort", "region_to_force_own", "region", s.FORT_OWN_MOVEMENT_REGION),
        ("Warriors' Refuges", "refugee", "_ers_refugee_", "region_to_force_own", "region",
         s.WARRIORS_REFUGE_OWN_MOVEMENT_REGION),
        ("Monuments", "monument", "_ers_monument_", "region_to_force_own", "region", s.MONUMENT_OWN_MOVEMENT_REGION),
        ("Lookout posts", "outpost", "_ers_outpost_", "region_to_force_own", "region", s.LOOKOUT_OWN_MOVEMENT_REGION),
        ("Waystations", "waystation", "_ers_waystation_", "region_to_force_own_provincewide", "province",
         s.WAYSTATION_OWN_MOVEMENT_PROVINCE),
    ):
        if not value:
            continue
        buildings = _outposts(overlay, kind, key_part)
        for building in buildings:
            set_effect(overlay, building, OWN_MOVEMENT, scope, value, FEATURE, damaged=0)
        notes.append(f"{name} ({len(buildings)}) {value:+g}% in the {area}")
    if notes:
        overlay.note(FEATURE, f"Campaign movement of own armies: {'; '.join(notes)} (bonuses of several outposts add up).")
