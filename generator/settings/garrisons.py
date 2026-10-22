"""Buildings with garrisons."""

# Number of copies of every garrison unit (commanders excluded), compared to vanilla.
SETTLEMENT_GARRISON_MULTIPLIER = 1  # main buildings of major and minor settlements
LOOKOUT_GARRISON_MULTIPLIER = 2  # lookout posts
GARRISON_MULTIPLIER = 4  # every other building with a garrison (garrison buildings, other outposts, landmarks, ...)
# Ammunition % that garrison buildings give to own armies in their region (vanilla none), as (regular
# expression matched against the whole building level key, {"all": % ammunition, "siege": % ammunition
# when defending a siege}). The first matching pattern wins. Damaged and low or medium influence: full
# value; ruined: none.
GARRISON_AMMUNITION = [
    # Ashur's garrison chain
    (r"phar_map_ash_military_garrison_type_a_1", {"all": 15}),
    (r"phar_map_ash_military_garrison_type_a_2", {"all": 20}),
    (r"phar_map_ash_military_garrison_type_a_3", {"all": 25}),
    # Guard Tower of Canaan, Hatti and Egypt (Suppiluliuma's keeps the general values below)
    (r"phar_main_(?:canaan|hatti|kemet)_military_administration_garrison_type_b_1", {"all": 10, "siege": 10}),
    # City Guard Station, City Guard Compound and their equivalents
    (r"phar_\w+_military_(?:administration_)?garrison_type_a(?:_[a-z_]+)?_1", {"all": 10}),
    (r"phar_\w+_military_(?:administration_)?garrison_type_a(?:_[a-z_]+)?_2", {"all": 15}),
    # Guard Tower and its equivalents (Babylon's Royal Garrison included)
    (r"phar_\w+_military_(?:administration_)?garrison_type_b(?:_[a-z_]+)?_1", {"all": 10, "siege": 5}),
]
