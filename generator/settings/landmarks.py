"""Landmarks."""

# Effects of landmarks: building level -> {(effect, scope): value}. A value alone means: half (rounded
# toward zero) when damaged, nothing when ruined, the full value at low and medium influence; otherwise
# (value, damaged, ruined, low influence, medium influence). Effects not listed keep their vanilla values.
LANDMARK_EFFECTS = {
    "phar_map_all_landmark_unique_major_assuwa_wilusa_1": {  # Citadel of Troy
        ("phar_main_diplomatic_relations_all_factor_building", "building_to_faction_own"): (5, 0, 0, 5, 5),
    },
    "phar_map_all_landmark_unique_major_achaea_mycenae_1": {  # Cyclopean Walls
        ("phar_main_siege_attrition_mod_buildings", "region_to_force_own"): (-25, 0, 0, -25, -25),
    },
    "phar_map_all_landmark_gold_happiness_tushhan_2": {  # Decorated Pottery Workshop
        ("phar_main_base_amount_gold_province", "region_to_province_own_text_provincewide"): 30,
        ("phar_main_province_management_growth_added_slot",
         "region_to_province_own_text_provincewide"): (3, 3, 0, 3, 3),
        ("phar_main_province_management_happiness_building", "region_to_province_own_factionwide"): 4,
        ("phar_main_scripted_victory_points_buildings", "building_to_faction_own"): (1, 1, 0, 1, 1),
        ("phar_main_influence_province_management_buildings", "building_to_province_own_factionwide"): 4,
    },
    "phar_main_all_landmark_growth_happiness_ashkelon_1": {  # Deep Groundwater Supply
        ("phar_main_province_development_growth_added_building", "region_to_province_own_text_provincewide"): 6,
        ("phar_main_siege_attrition_mod_buildings", "region_to_force_own"): (-50, 0, 0, -50, -50),
        ("phar_main_siege_holdout_buildings", "region_to_region_own"): (2, 2, 0, 2, 2),
    },
    "phar_map_all_landmark_unique_major_achaea_ithaca_1": {  # Fortress of Ithaca
        ("phar_map_region_line_of_sight_basic", "building_to_region"): 80,
    },
    "phar_main_all_landmark_bronze_buhen_1": {  # Grand Copper Repository
        ("phar_main_armour_mod", "building_to_force_own_factionwide"): (5, 0, 0, 5, 5),
    },
    "phar_main_all_landmark_production_morale_boost_parha_2": {  # High Citadel of Parha
        ("phar_effect_economy_ers_trading_post_mod_all_resources", "region_to_province_own_text_provincewide"): 20,
        ("phar_main_diplomatic_relations_all_factor_building", "building_to_faction_own"): (5, 0, 0, 5, 5),
        ("phar_main_province_management_growth_added_slot",
         "region_to_province_own_text_provincewide"): (3, 3, 0, 3, 3),
        ("phar_main_province_development_growth_added_building", "region_to_province_own_text_provincewide"): 4,
        ("phar_main_province_management_happiness_building", "region_to_province_own_text_provincewide"): 4,
        ("phar_main_scripted_victory_points_buildings", "building_to_faction_own"): (1, 1, 1, 1, 1),
        ("phar_main_unit_stat_flat_bonus_morale_add_unit_sets_all_units",
         "region_to_province_own_text_own_armies"): (5, 0, 0, 5, 5),
    },
    "phar_map_all_landmark_unique_major_thrace_ismaros_1": {  # Hilltop Holdfast
        ("phar_main_siege_holdout_buildings", "region_to_region_own"): (1, 1, 0, 1, 1),
    },
    "phar_map_all_landmark_growth_movement_ur_1": {  # House of Ea-nasir
        ("phar_main_province_management_happiness_building",
         "region_to_province_own_text_provincewide"): (-5, -5, 0, -5, -5),
        ("phar_main_diplomatic_relations_all_factor_building", "building_to_faction_own"): (-5, -5, 0, -5, -5),
        ("phar_main_percentage_multiplier_mod_troy_bronze_buildings", "building_to_province_own_factionwide"): 5,
        ("phar_main_building_gold_base_amount_buildings", "region_to_region_own"): 20,
    },
    "phar_map_all_landmark_replenishment_influence_nineveh_2": {  # House of Exorcists
        ("phar_main_unit_stat_flat_bonus_morale_add_unit_sets_all_units",
         "region_to_province_own_text_own_armies"): (5, 0, 0, 5, 5),
        ("phar_main_province_management_happiness_building", "region_to_province_own_text_provincewide"): 4,
        ("phar_main_influence_province_management_buildings", "region_to_province_own_text_provincewide"): 4,
        ("phar_main_melee_attack_unit_sets_all_units", "building_to_province"): (5, 0, 0, 5, 5),
        ("phar_main_province_management_growth_added_slot",
         "region_to_province_own_text_provincewide"): (3, 3, 0, 3, 3),
        ("phar_main_scripted_victory_points_buildings", "building_to_faction_own"): (1, 1, 0, 1, 1),
    },
    "phar_map_all_landmark_food_happiness_terqa_1": {  # Ice House
        ("phar_main_province_management_happiness_building", "region_to_province_own_text_provincewide"): 2,
        ("phar_main_province_development_growth_added_building", "region_to_province_own_text_provincewide"): 4,
    },
    "phar_map_all_landmark_ranged_attack_chariot_speed_irridu_1": {  # Lion Hunting Grounds
        ("phar_main_scripted_effect_legitimacy_from_buildings", "building_to_faction_own"): 5,
        ("phar_map_unit_stat_flat_bonus_accuracy_mod", "region_to_province_own_text_own_armies"): (5, 0, 0, 5, 5),
        ("phar_map_unit_stat_flat_bonus_speed_add_unit_set_chariots",
         "region_to_province_own_text_own_armies"): (10, 0, 0, 10, 10),
    },
    "phar_map_all_landmark_unique_major_assuwa_telmessos_1": {  # Lycian Stables
        ("phar_main_unit_xp_mod_unit_sets_chariots_all", "building_to_force_own_provincewide"): (2, 0, 0, 2, 2),
    },
    "phar_main_all_landmark_food_boost_komombo_1": {  # Nilometer
        ("phar_main_influence_province_management_buildings",
         "region_to_province_own_text_provincewide"): (2, 1, 0, 1, 1),
        ("phar_main_province_development_growth_added_building", "region_to_province_own_text_provincewide"): 6,
        ("phar_main_scripted_effect_legitimacy_from_buildings", "building_to_faction_own"): 5,
    },
    "phar_map_all_landmark_happiness_general_rank_mari_1": {  # Palace Archive
        ("phar_main_hero_recruitment_level_mod_buildings", "region_to_province_own_text_provincewide"): 6,
        ("phar_main_province_management_happiness_building", "region_to_province_own_factionwide"): 2,
        ("phar_main_influence_province_management_buildings", "building_to_province_own_factionwide"): 2,
        ("phar_main_scripted_effect_legitimacy_from_buildings", "building_to_faction_own"): 5,
    },
    "phar_map_all_landmark_unique_major_achaea_knossos_1": {  # Palace of Minos
        ("phar_effect_economy_ers_trading_post_mod_all_resources", "building_to_province_own_factionwide"): 5,
        ("phar_main_province_management_happiness_building_faction", "building_to_province_own_factionwide"): 2,
    },
    "phar_main_all_landmark_production_boost_tarsus_1": {  # Pottery Markets
        ("phar_main_province_management_happiness_building", "region_to_province_own_text_provincewide"): 4,
        ("phar_main_province_management_happiness_building_adjacent", "province_to_adjacent_province_own"): 2,
        ("phar_main_province_management_influence_building_adjacent", "region_to_adjacent_province_own"): 2,
    },
    "phar_main_all_landmark_legitimacy_influence_megiddo_1": {  # Professional Scribal Complex
        ("phar_main_influence_province_management_buildings", "region_to_province_own_text_provincewide"): 6,
        ("phar_main_province_management_influence_building_adjacent",
         "region_to_adjacent_province_own"): (4, 2, 0, 2, 2),
        ("phar_main_scripted_effect_legitimacy_from_buildings", "building_to_faction_own"): 5,
    },
    "phar_main_all_landmark_happiness_influence_kawa_1": {  # Rock Art Site School
        ("phar_main_scripted_effect_legitimacy_from_buildings", "building_to_faction_own"): 2,
        ("phar_main_province_management_happiness_building", "region_to_province_own_text_provincewide"): 6,
        ("phar_main_province_management_happiness_building_adjacent", "province_to_adjacent_province_own"): 3,
        ("phar_main_province_management_influence_building_adjacent", "region_to_adjacent_province_own"): 3,
    },
    "phar_map_all_landmark_unique_major_achaea_pteleon_1": {  # Royal Asaminthos
        ("phar_map_unit_fatigue_resistance_mod_unit_sets_bodyguards",
         "building_to_force_own_factionwide"): (-2, 0, 0, -2, -2),
        ("phar_map_unit_fatigue_resistance_mod_unit_sets_high_tier_units",
         "building_to_force_own_factionwide"): (-2, 0, 0, -2, -2),
    },
    "phar_main_all_landmark_happiness_hattusa_2": {  # Royal Legal Complex
        ("phar_main_province_management_growth_added_slot",
         "region_to_province_own_text_provincewide"): (3, 3, 0, 3, 3),
        ("phar_main_province_management_happiness_building_faction", "building_to_province_own_factionwide"): 2,
        ("phar_main_influence_province_management_buildings", "building_to_province_own_factionwide"): 2,
        ("phar_main_scripted_effect_legitimacy_from_buildings", "building_to_faction_own"): 5,
        ("phar_main_scripted_victory_points_buildings", "building_to_faction_own"): (1, 1, 1, 1, 1),
        ("phar_main_pillars_of_civilization_points_added", "region_to_faction_own"): (15, 0, 0, 15, 15),
    },
    "phar_main_all_landmark_production_boost_thebes_1": {  # Royal Tax Collector's Office
        ("phar_main_scripted_effect_legitimacy_from_buildings", "building_to_faction_own"): 5,
    },
    "phar_main_all_landmark_hero_training_memphis_1": {  # Royal War Academy
        ("phar_main_hero_recruitment_level_mod_buildings", "region_to_province_own_text_provincewide"): 8,
        ("phar_main_scripted_effect_legitimacy_from_buildings", "building_to_faction_own"): 4,
    },
    "phar_main_all_landmark_food_zippalanda_1": {  # Sanctified Cattle Herds
        ("phar_main_province_management_happiness_building", "region_to_province_own_text_provincewide"): 2,
        ("phar_main_influence_province_management_buildings",
         "region_to_province_own_text_provincewide"): (2, 1, 0, 1, 1),
    },
    "phar_main_all_landmark_production_boost_emar_1": {  # Shipment Redistribution Hub
        ("phar_main_influence_province_management_buildings", "region_to_province_own_text_provincewide"): 4,
        ("phar_main_province_management_influence_building_adjacent", "region_to_adjacent_province_own"): 2,
    },
    "phar_main_all_landmark_legitimacy_influence_amarna_1": {  # The Great Archives
        ("phar_main_pillars_of_civilization_points_added", "region_to_faction_own"): (15, 0, 0, 15, 15),
    },
    "phar_main_all_landmark_food_bahariya_oasis_1": {  # The Northern Oasis Fields
        ("phar_main_building_food_base_amount", "region_to_region_own"): 250,
        ("phar_main_influence_province_management_buildings",
         "region_to_province_own_text_provincewide"): (2, 1, 0, 1, 1),
        ("phar_main_province_development_growth_added_building", "region_to_province_own_text_provincewide"): 6,
        ("phar_main_province_management_happiness_building", "region_to_province_own_text_provincewide"): 4,
    },
    "phar_map_all_landmark_unique_major_assuwa_ephesos_1": {  # The Sacred Way
        ("phar_main_all_gods_favour", "region_to_faction_own"): (100, 50, 10, 100, 100),
        ("phar_main_province_management_happiness_building", "region_to_province_own_text_provincewide"): 4,
        ("phar_main_influence_province_management_buildings", "region_to_province_own_text_provincewide"): 4,
    },
}

# Construction costs of landmarks: building level -> {resource: amount}. Resources not listed keep their
# vanilla cost.
LANDMARK_COSTS = {
    "phar_main_all_landmark_food_ugarit_1": {"stones": 800, "wood": 400},  # The White Harbour
    "phar_map_all_landmark_unique_major_assuwa_wilusa_1": {"stones": 1400, "wood": 200},  # Citadel of Troy
    # Cyclopean Walls
    "phar_map_all_landmark_unique_major_achaea_mycenae_1": {"gold": 100, "stones": 1400, "wood": 300},
    # Decorated Pottery Workshop
    "phar_map_all_landmark_gold_happiness_tushhan_2": {"gold": 300, "stones": 1000, "wood": 300},
    # Deep Groundwater Supply
    "phar_main_all_landmark_growth_happiness_ashkelon_1": {"gold": 100, "stones": 800, "wood": 250},
    # Fortress of Ithaca
    "phar_map_all_landmark_unique_major_achaea_ithaca_1": {"gold": 100, "stones": 1000, "wood": 450},
    "phar_main_all_landmark_bronze_buhen_1": {"gold": 500, "stones": 500, "wood": 500},  # Grand Copper Repository
    # High Citadel of Parha
    "phar_main_all_landmark_production_morale_boost_parha_2": {"gold": 250, "stones": 1250, "wood": 250},
    "phar_map_all_landmark_unique_major_thrace_ismaros_1": {"stones": 800, "wood": 400},  # Hilltop Holdfast
    "phar_map_all_landmark_growth_movement_ur_1": {"stones": 600, "wood": 300},  # House of Ea-nasir
    # House of Exorcists
    "phar_map_all_landmark_replenishment_influence_nineveh_2": {"gold": 400, "stones": 800, "wood": 250},
    "phar_map_all_landmark_food_happiness_terqa_1": {"gold": 100, "stones": 1000, "wood": 300},  # Ice House
    # Lion Hunting Grounds
    "phar_map_all_landmark_ranged_attack_chariot_speed_irridu_1": {"gold": 400, "stones": 200, "wood": 400},
    # Lycian Stables
    "phar_map_all_landmark_unique_major_assuwa_telmessos_1": {"gold": 300, "stones": 600, "wood": 400},
    "phar_main_all_landmark_food_boost_komombo_1": {"stones": 1000, "wood": 200},  # Nilometer
    "phar_map_all_landmark_happiness_general_rank_mari_1": {"gold": 300, "stones": 1000, "wood": 200},  # Palace Archive
    # Palace of Minos
    "phar_map_all_landmark_unique_major_achaea_knossos_1": {"gold": 450, "stones": 1000, "wood": 150},
    "phar_main_all_landmark_production_boost_tarsus_1": {"gold": 250, "stones": 850, "wood": 450},  # Pottery Markets
    # Professional Scribal Complex
    "phar_main_all_landmark_legitimacy_influence_megiddo_1": {"gold": 250, "stones": 1000, "wood": 250},
    "phar_main_all_landmark_happiness_influence_kawa_1": {"stones": 800, "wood": 100},  # Rock Art Site School
    # Royal Asaminthos
    "phar_map_all_landmark_unique_major_achaea_pteleon_1": {"gold": 250, "stones": 850, "wood": 250},
    "phar_main_all_landmark_happiness_hattusa_2": {"gold": 200, "stones": 1200, "wood": 200},  # Royal Legal Complex
    # Royal Tax Collector's Office
    "phar_main_all_landmark_production_boost_thebes_1": {"gold": 400, "stones": 1000, "wood": 200},
    "phar_main_all_landmark_hero_training_memphis_1": {"gold": 400, "stones": 1000, "wood": 200},  # Royal War Academy
    "phar_main_all_landmark_food_zippalanda_1": {"gold": 450, "stones": 200},  # Sanctified Cattle Herds
    # Shipment Redistribution Hub
    "phar_main_all_landmark_production_boost_emar_1": {"gold": 400, "stones": 400, "wood": 400},
    "phar_main_all_landmark_legitimacy_influence_amarna_1": {"stones": 1400, "wood": 300},  # The Great Archives
    # The Northern Oasis Fields
    "phar_main_all_landmark_food_bahariya_oasis_1": {"gold": 300, "stones": 300, "wood": 300},
    "phar_map_all_landmark_unique_major_assuwa_ephesos_1": {"stones": 1200, "wood": 100},  # The Sacred Way
}

# Garrisons of landmarks (vanilla none): building level -> (unit group, {unit: number of units}). The
# garrison is the same for every culture, and GARRISON_MULTIPLIER (settings/garrisons.py) multiplies it.
LANDMARK_GARRISONS = {
    # Citadel of Troy: Troy's Chosen
    "phar_map_all_landmark_unique_major_assuwa_wilusa_1": ("phar_map_garrison_modded_troy",
                                                           {"phar_map_land_wil_wilusas_chosen": 2}),
    # Cyclopean Walls: Palace Guards
    "phar_map_all_landmark_unique_major_achaea_mycenae_1": ("phar_map_garrison_modded_cyclopean",
                                                            {"phar_map_land_ach_mycenaen_temple_guards": 2}),
    # Fortress of Ithaca: Exemplary Ambushers
    "phar_map_all_landmark_unique_major_achaea_ithaca_1": ("phar_map_garrison_modded_ithaca",
                                                           {"phar_map_land_ach_elite_ambushers": 2}),
    # Hilltop Holdfast: Mad Mares of Thrace
    "phar_map_all_landmark_unique_major_thrace_ismaros_1": ("phar_map_garrison_modded_thrace",
                                                            {"phar_map_land_thr_mares_of_diomedes": 1}),
    # Lycian Stables: Lycian Winged Chariots
    "phar_map_all_landmark_unique_major_assuwa_telmessos_1": ("phar_map_garrison_modded_lycian",
                                                              {"phar_map_land_wil_lycian_light_chariots": 1}),
}
