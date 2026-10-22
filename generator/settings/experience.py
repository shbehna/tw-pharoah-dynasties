"""Experience (values from the "XP Followers Traits And Buildings Buffed" mod, Workshop 3456700913)."""

# Unit experience per turn given by buildings (effect phar_main_unit_xp_mod_training_unit_sets_all), as
# (regular expression matched against the whole building level key, value) or (..., value, scope). The
# first matching pattern wins; None leaves the building alone. Without a scope, the building's vanilla
# rows of this effect change; with one, the row of that scope is set (added if the building has none) and
# other scopes keep their vanilla value. Damaged buildings and low or medium influence give half (rounded
# down), ruined buildings nothing.
EXPERIENCE_UNIT_BUILDINGS = [
    # Kuru's Mercenary Hunting Camp, Mercenary Hunting Village (vanilla 25, 50)
    (r"phar_main_kuru_military_administration_unit_training_type_b_1", 205),
    (r"phar_main_kuru_military_administration_unit_training_type_b_2", 415),
    # Champion's Hall, every culture (vanilla 40)
    (r"phar_\w+_military_administration_unit_training_type_b_1", 335),
    # Warriors' Refuge (vanilla 40)
    (r"phar_\w+_ers_refugee_\w+", 335),
    # Garrison buildings, for own armies in their region (vanilla none): City Guard Station, City Guard
    # Compound, Guard Tower and their equivalents. Ashur's third garrison level is left out.
    (r"phar_map_ash_military_garrison_type_a_3", None),
    (r"phar_\w+_military_(?:administration_)?garrison_type_a(?:_[a-z_]+)?_1", 200, "building_to_forces_own_regionwide"),
    (r"phar_\w+_military_(?:administration_)?garrison_type_a(?:_[a-z_]+)?_2", 300, "building_to_forces_own_regionwide"),
    (r"phar_\w+_military_(?:administration_)?garrison_type_b(?:_[a-z_]+)?_1", 150, "building_to_forces_own_regionwide"),
    # Royal War Academy (vanilla 70)
    (r"phar_main_all_landmark_hero_training_memphis_1", 465),
    # Shrine of Amun, Shrine of Kumarbi (vanilla 15, 30)
    (r"phar_main_ers_shrine_amun_fake_help_pages", 125),
    (r"phar_main_ers_shrine_kumarbi_fake_help_pages", 250),
    # Sea Peoples' Trapping Sites, Hunters' Tents, Hunting Bivouac (vanilla 20, 50, 120)
    (r"phar_sea_horde_management_xp_per_turn_upkeep_1", 100),
    (r"phar_sea_horde_management_xp_per_turn_upkeep_2", 250),
    (r"phar_sea_horde_management_xp_per_turn_upkeep_3", 510),
    # Peleset Single Combat Arena, Fighting Games, Fighting Tournaments (vanilla 30, 40, 75)
    (r"phar_sea_peleset_special_xp_mod_1", 150),
    (r"phar_sea_peleset_special_xp_mod_2", 200),
    (r"phar_sea_peleset_special_xp_mod_3", 375),
    # Peleset Great Assembly, all armies (vanilla 50)
    (r"phar_sea_peleset_special_royal_council_1", 250),
    # Peleset Dueling Field, Battle Arena (vanilla 35, 70)
    (r"phar_sea_peleset_province_management_influence_xp_per_turn_native_settled_2", 290),
    (r"phar_sea_peleset_province_management_influence_xp_per_turn_native_settled_3", 465),
]

# Character experience per turn given by buildings (effect phar_main_scripted_char_xp_per_turn), by
# building level. The damaged and influence values keep their vanilla proportions.
EXPERIENCE_CHARACTER_BUILDINGS = {
    "phar_main_all_military_administration_hero_training_2": 45,  # Officer School (vanilla 20)
    "phar_main_all_military_administration_hero_training_3": 112,  # Royal Officer School (vanilla 50)
}

# Unit experience given to the army by followers and titles (their unit experience effects), by ancillary.
EXPERIENCE_ANCILLARIES = {
    "phar_main_common_general_11": 175,  # Veteran Soldier (vanilla 10)
    "phar_main_common_general_17": 175,  # Clay Tablet (vanilla 10)
    "phar_main_rare_3": 325,  # Mitanni Horse Trainer (vanilla 20)
    "phar_main_rare_4": 325,  # Kushite Guards (vanilla 20)
    "phar_main_rare_15": 325,  # Duellist (vanilla 20)
    "phar_main_rare_16": 325,  # Blind Veteran (vanilla 20)
    "phar_main_rare_17": 325,  # Strongman (vanilla 20)
    "phar_main_rare_18": 325,  # Wise Nobleman (vanilla 20)
    "phar_main_rare_50": 325,  # Obsidian Tools & Blades (vanilla 20)
    "phar_main_unique_26": 350,  # Ceremonial Sword of Adad-narari I (vanilla 25)
    "phar_map_hatshepsut_theban_veteran": 225,  # Theban Veteran (vanilla 20)
    "phar_map_hatshepsut_theban_veteran_unique": 350,  # Theban Veteran, unique (vanilla 20)
    "phar_main_prince_title_royal_steward": 175,  # Royal Steward (vanilla 50)
    "phar_main_prince_title_royal_steward_upgraded": 325,  # (vanilla 100)
    "phar_main_prince_title_man_of_the_people": 175,  # Man of the People (vanilla 50)
    "phar_main_prince_title_man_of_the_people_upgraded": 325,  # (vanilla 100)
    "phar_main_title_8": 250,  # Lionlike in Wrath (vanilla 75)
    "phar_main_title_23": 175,  # Overseer of Militia (vanilla 20)
}

# Unit experience per turn given by traits (effect troy_effect_army_units_experience_per_turn), by trait level.
EXPERIENCE_TRAITS = {
    "troy_trait_achilles_conf_grieving_1": 375,  # Grieving, Achilles (vanilla 100)
    "troy_trait_loyalty_mentor_1": 65,  # Mentor (vanilla 10)
}
