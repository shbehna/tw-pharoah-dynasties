"""Administrative burden."""

# Administration points at which each of the 12 administration tiers starts
# (vanilla: 0, 55, 110, 160, 215, 270, 330, 390, 455, 520, 590, 660).
ADMIN_TIER_THRESHOLDS = [0, 250, 450, 650, 850, 1050, 1250, 1500, 1750, 2050, 2350, 2700]
# Length of the administration bar in the UI, in points (vanilla: 730).
ADMIN_BAR_MAX = 2800
# Administration cost of the main settlement building, by building level (1-based).
MAJOR_SETTLEMENT_ADMIN_COST = [3, 6, 10, 16, 24]  # vanilla 2-3-4-5-6
MINOR_SETTLEMENT_ADMIN_COST = [3, 6, 12]  # vanilla 2-3-4
# Province capitals ("poc" major settlements) cost 1 more than other major
# settlements in vanilla (3-4-5-6-7). True keeps that +1 on top of the values above.
KEEP_PROVINCE_CAPITAL_EXTRA_ADMIN = True
# Construction cost penalty added to each administration tier (12 tiers per culture).
# The penalty starts at ADMIN_BUILDING_COST_FIRST_TIER with ADMIN_BUILDING_COST_START %
# and grows by ADMIN_BUILDING_COST_STEP % per tier (with 0 and 10: 0% at tier 1 ... 110% at tier 12).
# ADMIN_BUILDING_COST_MAX caps it, e.g. 100.
ADMIN_BUILDING_COST_FIRST_TIER = 1
ADMIN_BUILDING_COST_START = 0
ADMIN_BUILDING_COST_STEP = 10
ADMIN_BUILDING_COST_MAX = None  # % cap, or None
# Building upkeep % of each administration tier (1-12; see BUILDING_UPKEEP_PERCENT), for the
# resources in ADMIN_BUILDING_UPKEEP_RESOURCES (food, bronze, gold, stones, wood). 0: no effect.
ADMIN_BUILDING_UPKEEP = [-50, -25, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
ADMIN_BUILDING_UPKEEP_RESOURCES = ["gold", "stones"]
# Make the bronze and gold upkeep penalty/bonus of each administration tier equal to the food one
# (vanilla tiers have no gold upkeep effect).
ADMIN_BRONZE_GOLD_UPKEEP_EQUALS_FOOD = True
# Vanilla tiers 3-12 raise the recruitment cost of one resource, by culture: food (Egypt), bronze
# (Hittites) or gold (Mesopotamia). True raises the food, bronze and gold recruitment cost of these
# tiers by that same %. Aegean, Canaanite and Sea Peoples tiers already raise every recruitment cost.
ADMIN_RECRUITMENT_COST_ALL_RESOURCES = True
# Recruitment cost % of each administration tier (1-12), for every culture, or None for the vanilla
# values. Only tiers that have a recruitment cost effect in vanilla (3-12) can change.
# Vanilla: 0, 0, 10, 20, 30, 40, 50, 60, 80, 100, 120, 140 (Egypt, Hittites, Mesopotamia);
# 0, 0, 5, 10, 15, 20, 25, 30, 40, 50, 60, 80 (Aegea: native units; Canaan; Sea Peoples: horde units).
ADMIN_RECRUITMENT_COST = [0, 0, 10, 20, 30, 40, 50, 60, 80, 100, 120, 140]
# Buildings that reduce the administration burden (vanilla: none), in administration points:
# building level -> (reduction at high influence, reduction at low and medium influence).
# A damaged building gives no reduction. Rows of rebuilt landmarks move to their new level.
ADMIN_BURDEN_REDUCTIONS = {
    # Newscrier's Stand, Public Square, Hall of Messengers
    "phar_main_all_province_management_influence_type_a_1": (-5, -2),
    "phar_main_all_province_management_influence_type_a_2": (-10, -4),
    "phar_main_all_province_management_influence_type_a_3": (-14, -6),
    # Newscrier's Stand, Public Square (second chain)
    "phar_main_all_province_management_influence_type_b_1": (-4, -2),
    "phar_main_all_province_management_influence_type_b_2": (-7, -3),
    # Hall of Records, Palace of Correspondence (Wisdom Codices: province capitals)
    "phar_main_all_province_management_main_building_legitimacy_influence_boost_1": (-6, -3),
    "phar_main_all_province_management_main_building_legitimacy_influence_boost_2": (-10, -5),
    "phar_main_all_province_management_main_building_poc_legitimacy_influence_boost_1": (-5, -2),
    "phar_main_all_province_management_main_building_poc_legitimacy_influence_boost_2": (-10, -4),
    "phar_main_all_province_management_main_building_poc_legitimacy_influence_boost_3": (-14, -6),
    # Seti's Office of Relations, Seti's Royal Palace
    "phar_main_seti_province_management_main_building_legitimacy_influence_boost_1": (-8, -4),
    "phar_main_seti_province_management_main_building_legitimacy_influence_boost_2": (-12, -6),
    # Tax Collector's Office, Tax Administration Centre, Royal Tax Administration
    "phar_main_all_province_management_main_building_production_boost_overall_1": (-2, 0),
    "phar_main_all_province_management_main_building_production_boost_overall_2": (-4, -2),
    "phar_main_all_province_management_main_building_production_boost_overall_3": (-6, -3),
    "phar_main_all_province_management_main_building_poc_production_boost_overall_1": (-2, 0),
    "phar_main_all_province_management_main_building_poc_production_boost_overall_2": (-4, -2),
    "phar_main_all_province_management_main_building_poc_production_boost_overall_3": (-6, -3),
    # Seti's Tax Administration Centre, Tax Administration Palace
    "phar_main_seti_province_management_main_building_production_boost_overall_1": (-2, 0),
    "phar_main_seti_province_management_main_building_production_boost_overall_2": (-5, -2),
    # Recruitment Hall, War Council, War Coffers
    "phar_main_all_military_administration_cost_mod_1": (-3, -1),
    "phar_main_all_military_administration_cost_mod_2": (-6, -3),
    "phar_main_all_military_administration_cost_mod_3": (-10, -5),
    # Seti's Military Office, Recruitment Office, Recruitment Administration Centre; Mustering Office
    "phar_main_seti_military_administration_cost_mod_recruit_slot_type_a_1": (-3, -1),
    "phar_main_seti_military_administration_cost_mod_recruit_slot_type_a_2": (-6, -3),
    "phar_main_seti_military_administration_cost_mod_recruit_slot_type_a_3": (-10, -5),
    "phar_main_seti_military_administration_cost_mod_recruit_slot_type_b_1": (-3, -1),
    # Ashur's War Stockpiles, War Treasury, War Council
    "phar_map_ash_military_administration_cost_mod_1": (-5, -1),
    "phar_map_ash_military_administration_cost_mod_2": (-8, -3),
    "phar_map_ash_military_administration_cost_mod_3": (-14, -5),
    # Traveller's Inn, Caravanserai, Visitor's Quarters
    "phar_main_all_province_management_roads_1": (-2, 0),
    "phar_main_all_province_management_roads_2": (-4, -2),
    "phar_main_all_province_management_roads_3": (-7, -4),
    # Mycenae's Road Administration Office, Tarasiya Road Network, Damokoros' Road Infrastructure
    "phar_map_myc_province_management_roads_1": (-2, 0),
    "phar_map_myc_province_management_roads_2": (-4, -2),
    "phar_map_myc_province_management_roads_3": (-7, -4),
    # Babylon's City Trade Records, Merchants' Guild, Royal Scribal Archives (all settlements)
    "phar_map_bab_province_management_main_building_production_influence_1": (-7, -4),
    "phar_map_bab_province_management_main_building_production_influence_2": (-10, -5),
    "phar_map_bab_province_management_main_building_production_influence_3": (-14, -6),
    "phar_map_bab_province_management_main_building_poc_production_influence_1": (-6, -3),
    "phar_map_bab_province_management_main_building_poc_production_influence_2": (-10, -5),
    "phar_map_bab_province_management_main_building_poc_production_influence_3": (-14, -6),
    # Babylon's Royal Garrison
    "phar_map_bab_military_garrison_type_b_1": (-3, 0),
    # Translators' Quarters
    "phar_main_all_province_management_main_building_poc_happiness_boost_1": (-3, -1),
    # Amenmesse's Foreign Visitors' Entertainments, Foreigners' Residential Quarters, Kushite Delegate School
    "phar_main_amenmesse_province_management_main_building_production_boost_growth_1": (-1, 0),
    "phar_main_amenmesse_province_management_main_building_production_boost_growth_2": (-3, -1),
    "phar_main_amenmesse_province_management_main_building_production_boost_growth_3": (-5, -3),
    # Bay's Chief Scribe's Headquarters; Trading Fairground, Regional Fair
    "phar_main_bay_province_management_main_building_diplomatic_relations_1": (-3, -1),
    "phar_main_bay_province_management_production_boost_overall_1": (-1, 0),
    "phar_main_bay_province_management_production_boost_overall_2": (-3, -1),
    # Ramesses' Medjay Office, Medjay Barracks, Medjay Headquarters
    "phar_main_ramesses_military_infantry_type_a_1": (-1, 0),
    "phar_main_ramesses_military_infantry_type_a_2": (-3, -1),
    "phar_main_ramesses_military_infantry_type_a_3": (-5, -3),
    # Suppiluliuma's Militia Gathering Post, Army Supply Centre
    "phar_main_suppi_military_administration_army_buff_1": (-2, -1),
    "phar_main_suppi_military_administration_army_buff_2": (-4, -2),
    # Peleset Ox Pastures, Oxen Caravan, Oxen Cart Assembly
    "phar_sea_peleset_province_management_movement_production_boost_1": (-1, 0),
    "phar_sea_peleset_province_management_movement_production_boost_2": (-3, -1),
    "phar_sea_peleset_province_management_movement_production_boost_3": (-5, -3),
    # Sea Peoples' Highborn Gathering, Tribal Convocation (high influence only)
    "phar_sea_administration_commandment_modifier_1": (-4, 0),
    "phar_sea_administration_commandment_modifier_2": (-10, 0),
    # Landmarks: Royal Legal Complex, Royal War Academy, The Great Archives, Professional Scribal Complex,
    # Royal Tax Collector's Office, Palace Archive
    "phar_main_all_landmark_happiness_hattusa_1": (-10, -5),
    "phar_main_all_landmark_hero_training_memphis_1": (-8, -4),
    "phar_main_all_landmark_legitimacy_influence_amarna_1": (-10, -4),
    "phar_main_all_landmark_legitimacy_influence_megiddo_1": (-7, -3),
    "phar_main_all_landmark_production_boost_thebes_1": (-12, -6),
    "phar_map_all_landmark_happiness_general_rank_mari_1": (-10, -4),
}
