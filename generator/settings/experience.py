"""Experience (half the values of the "XP Followers Traits And Buildings Buffed" mod, Workshop 3456700913,
rounded to the nearest 5)."""

# Unit experience per turn given by buildings (effect phar_main_unit_xp_mod_training_unit_sets_all), as
# (regular expression matched against the whole building level key, value) or (..., value, scope). The
# first matching pattern wins; None leaves the building alone. Without a scope, the building's vanilla
# rows of this effect change; with one, the row of that scope is set (added if the building has none) and
# other scopes keep their vanilla value. Damaged buildings and low or medium influence give half (rounded
# down), ruined buildings nothing.
EXPERIENCE_UNIT_BUILDINGS = [
    # Hanigalbat's own buildings: the value of the matching shared building + 20%, rounded to the nearest 5.
    # Champion's Hall (shared 170; vanilla 40)
    (r"phar_map_ash_military_administration_unit_training_type_b_1", 205),
    # City Guard Station, Inner Army Headquarters (shared 100, 150), Defenders' Fortress (150 + 50 = 200),
    # for own armies in their region (vanilla none)
    (r"phar_map_ash_military_garrison_type_a_1", 120, "building_to_forces_own_regionwide"),
    (r"phar_map_ash_military_garrison_type_a_2", 180, "building_to_forces_own_regionwide"),
    (r"phar_map_ash_military_garrison_type_a_3", 240, "building_to_forces_own_regionwide"),
    # Hanigalbat's Practice Halls, Training Compound, Arena of Trials (vanilla none)
    (r"phar_map_ash_military_administration_unit_training_type_a_1", 30, "building_to_force_own_provincewide"),
    (r"phar_map_ash_military_administration_unit_training_type_a_2", 60, "building_to_force_own_provincewide"),
    (r"phar_map_ash_military_administration_unit_training_type_a_3", 120, "building_to_force_own_provincewide"),
    # Proving Grounds, Training Grounds; Kuru's Mercenary Office, Mercenary Centre (vanilla none). These chains
    # have 2 levels.
    (r"phar_main_(?:all|kuru)_military_administration_unit_training_type_a_1", 20,
     "building_to_force_own_provincewide"),
    (r"phar_main_(?:all|kuru)_military_administration_unit_training_type_a_2", 50,
     "building_to_force_own_provincewide"),
    # Kuru's Mercenary Hunting Camp, Mercenary Hunting Village (vanilla 25, 50)
    (r"phar_main_kuru_military_administration_unit_training_type_b_1", 105),
    (r"phar_main_kuru_military_administration_unit_training_type_b_2", 210),
    # Champion's Hall, every culture (vanilla 40)
    (r"phar_\w+_military_administration_unit_training_type_b_1", 170),
    # Warriors' Refuge (vanilla 40)
    (r"phar_\w+_ers_refugee_\w+", 170),
    # Garrison buildings, for own armies in their region (vanilla none): City Guard Station, City Guard
    # Compound, Guard Tower and their equivalents.
    (r"phar_\w+_military_(?:administration_)?garrison_type_a(?:_[a-z_]+)?_1", 100, "building_to_forces_own_regionwide"),
    (r"phar_\w+_military_(?:administration_)?garrison_type_a(?:_[a-z_]+)?_2", 150, "building_to_forces_own_regionwide"),
    (r"phar_\w+_military_(?:administration_)?garrison_type_b(?:_[a-z_]+)?_1", 75, "building_to_forces_own_regionwide"),
    # Royal War Academy (vanilla 70)
    (r"phar_main_all_landmark_hero_training_memphis_1", 235),
    # Shrine of Amun, Shrine of Kumarbi (vanilla 15, 30)
    (r"phar_main_ers_shrine_amun_fake_help_pages", 65),
    (r"phar_main_ers_shrine_kumarbi_fake_help_pages", 125),
    # Sea Peoples' Trapping Sites, Hunters' Tents, Hunting Bivouac (vanilla 20, 50, 120)
    (r"phar_sea_horde_management_xp_per_turn_upkeep_1", 50),
    (r"phar_sea_horde_management_xp_per_turn_upkeep_2", 125),
    (r"phar_sea_horde_management_xp_per_turn_upkeep_3", 255),
    # Peleset Single Combat Arena, Fighting Games, Fighting Tournaments (vanilla 30, 40, 75)
    (r"phar_sea_peleset_special_xp_mod_1", 75),
    (r"phar_sea_peleset_special_xp_mod_2", 100),
    (r"phar_sea_peleset_special_xp_mod_3", 190),
    # Peleset Great Assembly, all armies (vanilla 50)
    (r"phar_sea_peleset_special_royal_council_1", 125),
    # Peleset Dueling Field, Battle Arena (vanilla 35, 70)
    (r"phar_sea_peleset_province_management_influence_xp_per_turn_native_settled_2", 145),
    (r"phar_sea_peleset_province_management_influence_xp_per_turn_native_settled_3", 235),
]

# Character experience per turn given by buildings (effect phar_main_scripted_char_xp_per_turn), by
# building level. The damaged and influence values keep their vanilla proportions.
EXPERIENCE_CHARACTER_BUILDINGS = {
    "phar_main_all_military_administration_hero_training_2": 25,  # Officer School (vanilla 20)
    "phar_main_all_military_administration_hero_training_3": 55,  # Royal Officer School (vanilla 50)
    # Hanigalbat: the value of the matching building above + 20%, rounded to the nearest 5
    "phar_map_ash_military_administration_hero_training_1": 30,  # Officers' School (25; vanilla 20)
    "phar_map_ash_military_administration_hero_training_2": 65,  # Royal Officers' School (55; vanilla 50)
    # Palace of War (vanilla 80 x 55/50 = 88; Hanigalbat only)
    "phar_map_ash_military_administration_hero_training_3": 105,
}

# Unit experience given to the army by followers and titles (their unit experience effects), by ancillary.
EXPERIENCE_ANCILLARIES = {
    "phar_main_common_general_11": 90,  # Veteran Soldier (vanilla 10)
    "phar_main_common_general_17": 90,  # Clay Tablet (vanilla 10)
    "phar_main_rare_3": 165,  # Mitanni Horse Trainer (vanilla 20)
    "phar_main_rare_4": 165,  # Kushite Guards (vanilla 20)
    "phar_main_rare_15": 165,  # Duellist (vanilla 20)
    "phar_main_rare_16": 165,  # Blind Veteran (vanilla 20)
    "phar_main_rare_17": 165,  # Strongman (vanilla 20)
    "phar_main_rare_18": 165,  # Wise Nobleman (vanilla 20)
    "phar_main_rare_50": 165,  # Obsidian Tools & Blades (vanilla 20)
    "phar_main_unique_26": 175,  # Ceremonial Sword of Adad-narari I (vanilla 25)
    "phar_map_hatshepsut_theban_veteran": 115,  # Theban Veteran (vanilla 20)
    "phar_map_hatshepsut_theban_veteran_unique": 175,  # Theban Veteran, unique (vanilla 20)
    "phar_main_prince_title_royal_steward": 90,  # Royal Steward (vanilla 50)
    "phar_main_prince_title_royal_steward_upgraded": 165,  # (vanilla 100)
    "phar_main_prince_title_man_of_the_people": 90,  # Man of the People (vanilla 50)
    "phar_main_prince_title_man_of_the_people_upgraded": 165,  # (vanilla 100)
    "phar_main_title_8": 125,  # Lionlike in Wrath (vanilla 75)
    "phar_main_title_23": 90,  # Overseer of Militia (vanilla 20)
}

# Unit experience per turn given by traits (effect troy_effect_army_units_experience_per_turn), by trait level.
EXPERIENCE_TRAITS = {
    "troy_trait_achilles_conf_grieving_1": 190,  # Grieving, Achilles (vanilla 100)
    "troy_trait_loyalty_mentor_1": 35,  # Mentor (vanilla 10)
}
