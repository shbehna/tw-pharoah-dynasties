"""Buildings."""

# Converting a religious building costs stone and wood instead of gold. Each rule is (regular expression
# matched against the whole resource cost key of the conversion, costs), the first matching rule wins.
# Costs are (stone, wood) for every level, or {level: (stone, wood)} with the level taken from the
# first group of the expression. Only conversions that cost gold in vanilla change; their gold cost
# becomes 0.
RELIGIOUS_CONVERSION_COSTS = [
    # Temples (vanilla 75 to 665 gold)
    (r"phar_(?:main|map)_religion_temple_\w+_(\d)_c?convert", {1: (75, 50), 2: (100, 75), 3: (125, 100)}),
    # Sea Peoples idols
    (r"phar_sea_religion_idol_\w+_(\d)_convert", {1: (125, 100), 2: (175, 125), 3: (225, 150)}),
    (r"troy_main_convert_religion_\w+_(\d)", {2: (125, 100), 3: (175, 125), 4: (225, 150)}),
    (r"troy_penthesilea_convert_religious_(\d)", {2: (175, 125), 3: (225, 175), 5: (275, 225)}),
    # Mesopotamian dwellings
    (r"phar_map_religion_dwelling_\w+_(\d)_convert", {1: (75, 35)}),
    # Shrines (outposts)
    (r"phar_main_convert_ers_shrine", (75, 75)),
]

# Production % of the three province resource chains, by level, and the unit
# upkeep reduction (province) added to their last level (vanilla none; 0: none).
GRANARY_PRODUCTION = [25, 40, 75]  # vanilla 5-10-20
GRANARY_FOOD_UPKEEP = 0
BRONZEWORKER_PRODUCTION = [10, 20, 35]  # vanilla 5-10-20
BRONZEWORKER_BRONZE_UPKEEP = -10
GOLDSMITH_PRODUCTION = [10, 15, 25]  # vanilla 5-10-20
GOLDSMITH_GOLD_UPKEEP = -5
SUMMER_FESTIVAL_FOOD_PRODUCTION = 40  # vanilla 10
SUMMER_FESTIVAL_HAPPINESS = 2  # vanilla 4
BEER_HALL_FOOD_PRODUCTION = 20  # vanilla 0
# Influence in the province of Amenmesse's Kushite Delegate School (vanilla -3, -2 at low and medium
# influence); the other influence values are scaled the same way.
DELEGATE_SCHOOL_INFLUENCE = 3
# Administration and management buildings, by level. Damaged values and the lower values at low and
# medium influence are scaled the same way.
# Tax Collector's Office, Tax Administration Centre, Royal Tax Administration (also in province
# capitals): % to all resources produced in the province (vanilla 5-10-20).
TAX_ADMINISTRATION_PRODUCTION = [10, 20, 35]
# Hall of Records, Palace of Correspondence, Wisdom Codices: % royal decree completion rate
# ("administration efficiency for royal decrees", for the whole faction; vanilla none). Every building
# adds to it. Outside province capitals the chain stops at Palace of Correspondence.
WISDOM_CODICES_DECREE_RATE = [1, 3, 5]
# Artisan's Workshop, Art School, Bazaar of the Arts: happiness in the province (vanilla 2-4-6).
BAZAAR_OF_THE_ARTS_HAPPINESS = [3, 5, 8]
# Midwife's House, Healing Hall, Surgeon's Practice: workforce growth in the province (vanilla 4-6-9).
SURGEONS_PRACTICE_WORKFORCE_GROWTH = [5, 8, 12]
# Mycenae's Kamaeu's Council, Damokoros' Residence, Lawagetas' Palace: happiness in the province
# (vanilla 0-1-2) and influence of the last level (vanilla 7; 4 at low and medium influence).
LAWAGETAS_PALACE_HAPPINESS = [1, 2, 4]
LAWAGETAS_PALACE_INFLUENCE = 8
# Road chains (Traveller's Inn, Caravanserai, Visitor's Quarters; Mycenae's Road Administration Office,
# Tarasiya Road Network, Damokoros' Road Infrastructure): % to all resources produced in adjacent own
# provinces (vanilla none).
ROADS_ADJACENT_PRODUCTION = [2, 5, 10]
# Workforce growth of the Management buildings built on a special resource (Olive Groves, Grand Bazaar,
# ...) that give workforce growth (vanilla 2).
RESOURCE_MANAGEMENT_WORKFORCE_GROWTH = 4
# Added to the campaign movement % of every building that gives own armies a movement bonus (land or
# sea): roads, Peleset and Sea Peoples buildings, landmarks. Outposts are set in their own section.
BUILDING_MOVEMENT_BONUS = 5
# Every other building's resource production % bonus is multiplied by this, if the bonus only
# applies to resources in OTHER_PRODUCTION_RESOURCES (troy_<resource> keys: food, bronze, gold,
# stones, wood). Bonuses to other resources keep their vanilla value.
OTHER_PRODUCTION_MULTIPLIER = 2
OTHER_PRODUCTION_RESOURCES = ["food"]
# Regular expressions of building keys whose production % bonuses are multiplied for every
# resource (landmarks, including the rebuilt ones and the unique wonders).
OTHER_PRODUCTION_ALL_RESOURCES = [r"_landmark_"]
# Regular expressions of building keys left out of the multiplier, e.g. r"_main_building_"
# to keep settlement buildings at their vanilla production bonus.
OTHER_PRODUCTION_EXCLUDE = []
# Effects set on whole building chains, by level: (regular expression matched against the whole chain key,
# effect, scope, values from the first level). A chain with fewer levels than values uses the first ones. An
# effect the level already has gets the new value (its other columns rescaled); a new one gives half when
# damaged, nothing when ruined and the full value at low and medium influence.
BUILDING_CHAIN_EFFECTS = [
    # Hanigalbat's War Stockpiles, War Treasury, War Council: food upkeep of units in the province (vanilla none)
    (r"phar_map_ash_military_administration_cost_mod", "phar_main_unit_upkeep_cost_percentage_multiplier_mod_food",
     "building_to_force_own_provincewide", [-6, -15, -25]),
    # Recruitment Hall, War Council, War Coffers: the same (vanilla none)
    (r"phar_main_all_military_administration_cost_mod", "phar_main_unit_upkeep_cost_percentage_multiplier_mod_food",
     "building_to_force_own_provincewide", [-5, -8, -15]),
    # Officer chains, upkeep of generals (bodyguard units) in the province (vanilla none): Hanigalbat's Officers'
    # School, Royal Officers' School, Palace of War; Officer Training Grounds, Officer School, Royal Officer
    # School; Ramesses' Military Office, Military School, Military Academy
    (r"phar_map_ash_military_administration_hero_training|phar_main_all_military_hero_training"
     r"|phar_main_ram_military_administration_hero_training",
     "phar_main_upkeep_mod_bodyguards", "building_to_force_own_provincewide", [-30, -50, -85]),
    # Hanigalbat's City Guard Station, Inner Army Headquarters, Defenders' Fortress: campaign movement of own
    # armies in the region (vanilla none)
    (r"phar_map_ash_military_garrison_type_a", "phar_main_mod_land_movement_campaign_basic", "region_to_force_own",
     [5, 10, 15]),
    # City Guard Station, City Guard Compound and their regional equivalents: the same (vanilla none)
    (r"phar_main_(?:canaan|hatti|kemet)_military_garrison_type_a|phar_(?:main|map)_military_garrison_type_a_\w+",
     "phar_main_mod_land_movement_campaign_basic", "region_to_force_own", [3, 6, 12]),
]

# Wood per turn of the wood production chains, by level: chain -> values (vanilla in the comments). The chain's
# own wood effect changes (wood, or port wood for the ports), other columns rescaled; a chain must list every
# level (ruins excluded). Mycenae's extra wood at high influence is not changed.
WOOD_PRODUCTION = {
    # Mesopotamia: Logging Grounds, Logging Camp
    "phar_map_all_resource_production_wood_mesopotamia_type_a": [55, 110],  # vanilla 35, 50
    "phar_map_irsu_resource_production_wood_mesopotamia_type_a": [55],  # Irsu's (vanilla 30)
    # Canaan: Woodcutting Yard, Woodcutting Complex
    "phar_main_wood_production_canaan_type_a": [45, 80],  # vanilla 30, 40
    "phar_main_irsu_resource_production_wood_type_a": [55],  # Irsu's (vanilla 35)
    # Canaan: Cypress Timber Yard, Cedar Timber Yard (also +1/+3 influence)
    "phar_main_wood_production_canaan_type_b": [50, 90],  # vanilla 50, 60
    "phar_main_irsu_resource_production_wood_canaan_type_b": [90],  # Irsu's (vanilla 50)
    # Hatti: Pine Timber Yard, Oak Timber Yard
    "phar_main_wood_production_hatti": [55, 95],  # vanilla 45, 55
    # Achaea: Logger's Yard, Logger's Square
    "phar_map_wood_production_achaea": [40, 85],  # vanilla 30, 40
    "phar_map_irsu_wood_production_achaea": [65],  # Irsu's (vanilla 30)
    # Assuwa: Lumber Shacks, Oak Storage
    "phar_map_wood_production_assuwa": [40, 85],  # vanilla 30, 40
    "phar_map_irsu_wood_production_assuwa": [50],  # Irsu's (vanilla 30)
    # Thrace: Foresters' Huts, Foresters' Houses
    "phar_map_wood_production_thrace": [60, 125],  # vanilla 30, 40
    "phar_map_irsu_wood_production_thrace": [65],  # Irsu's (vanilla 30)
    # Mycenae: Woodworker Kerosiya, Woodworker Brigades (+45/+55 more at high influence)
    "phar_map_myc_resource_production_wood_minor": [35, 75],  # vanilla 25, 35
    # Oases: Woodcutter Encampment, Woodcutter Camp (also lower recruitment cost)
    "phar_main_wood_oasis": [30, 50],  # vanilla 20, 30
    "phar_main_irsu_resource_production_wood_oasis": [40],  # Irsu's (vanilla 20)
    # Nile: Nile Lumber Camp, Nile Lumber Yard (also more fish)
    "phar_main_all_resource_production_wood_nile": [25, 45],  # vanilla 15, 20
    # Ports: Lumber Depot, Lumber Reserve (Nile); Lumber Waterways, Lumber Storehouse (Tigris and Euphrates)
    "phar_main_port_nile": [45, 65],  # vanilla 45, 55
    "phar_main_irsu_resource_production_wood_port_nile": [45],  # Irsu's (vanilla 45)
    "phar_map_all_resource_production_wood_port_tigris_euphrates": [50, 75],  # vanilla 50, 60
}

# Construction time of whole building chains, in turns added (minimum 1 turn): (regular expression matched
# against the whole chain key, turns).
BUILDING_CONSTRUCTION_TIME = [
    # Wood derivative chains: Cedar Warehouse (vanilla 2 turns), Woodcutters' District (2), Lumber Mill (2) and
    # Lumber Mill Complex (3)
    (r"phar_map_all_resource_production_wood_mesopotamia_type_a_derivative"
     r"|phar_main_wood_production_canaan_derivative_type_a|phar_main_wood_production_hatti_derivative", -1),
]

# Buildings of the CPTT Recruitment Rework mod (Workshop 3441336326), in its compatibility add-on
# (dynasties_rebalance_compat_cptt_recruitment_rework.pack): building level -> {(effect, scope): value}. A value
# alone means: nothing when damaged or ruined, the full value at low and medium influence (as that mod does);
# otherwise (value, damaged, ruined, low influence, medium influence). The effects listed replace the mod's
# rows of the same effect; its other effects stay.
CPTT_BUILDING_EFFECTS = {
    # Relocation Office, Deportation Hub (Mesopotamian factions; the mod: workforce growth -10/-20 here and
    # +10/+20 in adjacent provinces, which share one row so only one applies; influence 0, +2/+4 at low and
    # medium influence; happiness -10/-15)
    "cptt_fac_mes_depo_1": {
        ("phar_main_province_development_growth_added_building", "region_to_province_own_text_provincewide"): -10,
        ("phar_sea_province_development_growth_added_building", "province_to_adjacent_province_own"): 4,
        ("phar_main_influence_province_management_buildings", "region_to_province_own_text_provincewide"): 2,
        ("phar_main_province_management_happiness_building", "region_to_province_own_text_provincewide"): -3,
        # Upkeep of native units in the province (all resources: the game has no food-only upkeep effect for a
        # set of units)
        ("phar_main_upkeep_cost_mod_unit_sets_all_native_units", "building_to_force_own_provincewide"): -5,
    },
    "cptt_fac_mes_depo_2": {
        ("phar_main_province_development_growth_added_building", "region_to_province_own_text_provincewide"): -20,
        ("phar_sea_province_development_growth_added_building", "province_to_adjacent_province_own"): 8,
        ("phar_main_influence_province_management_buildings", "region_to_province_own_text_provincewide"): 5,
        ("phar_main_province_management_happiness_building", "region_to_province_own_text_provincewide"): -6,
        ("phar_main_upkeep_cost_mod_unit_sets_all_native_units", "building_to_force_own_provincewide"): -10,
    },
    # Grand Archive chain (Mesopotamian factions): State Archive, Central Archive, Royal Archive, Imperial Archive,
    # Universal Archives. Factionwide upkeep of units, at high influence only (as the mod does; the mod: food and
    # gold -5/-10/-20/-35/-50%). 0 removes the mod's value.
    "cptt_fac_mes_grandadmin_1": {
        ("phar_main_unit_upkeep_cost_percentage_multiplier_mod_food",
         "building_to_force_own_factionwide"): (-5, 0, 0, 0, 0),
        ("phar_main_unit_upkeep_cost_percentage_multiplier_mod_gold",
         "building_to_force_own_factionwide"): (0, 0, 0, 0, 0),
    },
    "cptt_fac_mes_grandadmin_2": {
        ("phar_main_unit_upkeep_cost_percentage_multiplier_mod_food",
         "building_to_force_own_factionwide"): (-10, 0, 0, 0, 0),
        ("phar_main_unit_upkeep_cost_percentage_multiplier_mod_gold",
         "building_to_force_own_factionwide"): (0, 0, 0, 0, 0),
    },
    "cptt_fac_mes_grandadmin_3": {
        ("phar_main_unit_upkeep_cost_percentage_multiplier_mod_food",
         "building_to_force_own_factionwide"): (-15, 0, 0, 0, 0),
        ("phar_main_unit_upkeep_cost_percentage_multiplier_mod_gold",
         "building_to_force_own_factionwide"): (0, 0, 0, 0, 0),
    },
    "cptt_fac_mes_grandadmin_4": {
        ("phar_main_unit_upkeep_cost_percentage_multiplier_mod_food",
         "building_to_force_own_factionwide"): (-25, 0, 0, 0, 0),
        ("phar_main_unit_upkeep_cost_percentage_multiplier_mod_gold",
         "building_to_force_own_factionwide"): (-5, 0, 0, 0, 0),
    },
    "cptt_fac_mes_grandadmin_5": {
        ("phar_main_unit_upkeep_cost_percentage_multiplier_mod_food",
         "building_to_force_own_factionwide"): (-35, 0, 0, 0, 0),
        ("phar_main_unit_upkeep_cost_percentage_multiplier_mod_gold",
         "building_to_force_own_factionwide"): (-10, 0, 0, 0, 0),
    },
}

# Construction costs of CPTT Recruitment Rework buildings: building level -> {resource: amount} (resources:
# gold, stones, wood). Each level gets its own cost; the mod's own costs are positive amounts, so its buildings
# cost nothing (Grand Archive: level 1 +3000 of each, levels 2-5 +2000 stone, +5000 wood and gold).
CPTT_BUILDING_COSTS = {
    "cptt_fac_mes_grandadmin_1": {"stones": 1000, "wood": 200, "gold": 100},  # State Archive
    "cptt_fac_mes_grandadmin_2": {"stones": 2000, "wood": 400, "gold": 200},  # Central Archive
    "cptt_fac_mes_grandadmin_3": {"stones": 3000, "wood": 600, "gold": 300},  # Royal Archive
    "cptt_fac_mes_grandadmin_4": {"stones": 4000, "wood": 800, "gold": 400},  # Imperial Archive
    "cptt_fac_mes_grandadmin_5": {"stones": 5000, "wood": 1000, "gold": 500},  # Universal Archives
}
# Building upkeep of CPTT Recruitment Rework buildings, for these resources of their cost in CPTT_BUILDING_COSTS,
# like the main mod's buildings: BUILDING_UPKEEP_PERCENT % of the cost per turn, rounded up to a multiple of
# BUILDING_UPKEEP_ROUNDING. (regular expression matched against the whole building level key, resources).
# The Grand Archive also keeps its fixed 50 gold upkeep and its wood upkeep (-20 to -320 wood production).
CPTT_BUILDING_UPKEEP_RESOURCES = [
    (r"cptt_fac_mes_grandadmin_\d", ["stones", "gold"]),
]

# Per-turn building upkeep (vanilla: a handful of buildings). Every level of the building sets in
# BUILDING_UPKEEP_SETS costs BUILDING_UPKEEP_PERCENT % of its construction cost per turn, for each
# resource of that cost, rounded up to a multiple of BUILDING_UPKEEP_ROUNDING. A resource the
# building already has an upkeep for keeps its vanilla upkeep. Levels also in a set of
# BUILDING_UPKEEP_EXCLUDED_SETS are left out.
# In-game categories: phar_main_municipal_complex (Administration), phar_main_province_management
# (Management), phar_main_religion (Religion), phar_main_military_administration (Military Support),
# phar_main_military_recruit (Recruitment), phar_main_resource_production (Resources),
# phar_main_production_management (Production). Other sets: phar_main_landmark, phar_main_port_plah,
# phar_main_military_ers / economic_ers / religious_ers / administrative_ers (outposts),
# phar_sea_horde_* (Sea Peoples hordes).
BUILDING_UPKEEP_PERCENT = 5
BUILDING_UPKEEP_ROUNDING = 5
BUILDING_UPKEEP_SETS = [
    "phar_main_municipal_complex",
    "phar_main_province_management",
    "phar_main_religion",
    "phar_main_landmark",
]
BUILDING_UPKEEP_EXCLUDED_SETS = [
    "phar_main_military_administration",
    "phar_main_military_recruit",
    "phar_main_resource_production",
    "phar_main_production_management",
]
