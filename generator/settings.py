"""Every tunable number of the mod, grouped like the sections of CHANGELOG.md.

Change a value here, then run `python generator/generate.py` and
`scripts/install.ps1` to rebuild and install the mod.
"""

# ---------------------------------------------------------------------------
# Administrative burden
# ---------------------------------------------------------------------------
# Administration points at which each of the 12 administration tiers starts
# (vanilla: 0, 55, 110, 160, 215, 270, 330, 390, 455, 520, 590, 660).
ADMIN_TIER_THRESHOLDS = [0, 150, 250, 400, 600, 750, 950, 1150, 1350, 1600, 1900, 2250]
# Length of the administration bar in the UI, in points (vanilla: 730).
ADMIN_BAR_MAX = 2300
# Administration cost of the main settlement building, by building level (1-based).
MAJOR_SETTLEMENT_ADMIN_COST = [2, 5, 8, 12, 16]  # vanilla 2-3-4-5-6
MINOR_SETTLEMENT_ADMIN_COST = [2, 5, 8]  # vanilla 2-3-4
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
# Make the bronze upkeep penalty/bonus of each administration tier equal to the food one.
ADMIN_BRONZE_UPKEEP_EQUALS_FOOD = True

# ---------------------------------------------------------------------------
# Outposts
# ---------------------------------------------------------------------------
TRADING_POST_RESOURCE_PRODUCTION = 15  # % to all resources in the region (vanilla 10)
FORT_MAX_UNITS = 20  # vanilla 10
WARRIORS_REFUGE_MAX_UNITS = 15  # vanilla 6
FORT_UPKEEP_REDUCTION = 90  # % (vanilla 50)
WARRIORS_REFUGE_UPKEEP_REDUCTION = 30  # % (vanilla 0)
WAYSTATION_HAPPINESS = 3  # province happiness (vanilla 0)
MONUMENT_ENEMY_MOVEMENT_PROVINCE = -10  # % campaign movement of enemy armies in the province
LOOKOUT_ENEMY_MOVEMENT_REGION = -10  # % campaign movement of enemy armies in the region
LOOKOUT_ENEMY_MOVEMENT_PROVINCE = -2.5  # % campaign movement of enemy armies in the province
# % campaign movement of your own armies (vanilla 0); the bonuses of several outposts add up.
FORT_OWN_MOVEMENT_REGION = 15
WARRIORS_REFUGE_OWN_MOVEMENT_REGION = 15
MONUMENT_OWN_MOVEMENT_REGION = 5
LOOKOUT_OWN_MOVEMENT_REGION = 5
WAYSTATION_OWN_MOVEMENT_PROVINCE = 10

# ---------------------------------------------------------------------------
# Movement
# ---------------------------------------------------------------------------
LAND_MOVEMENT = -30  # % campaign movement on land, every faction (player and AI)
NAVAL_MOVEMENT = -50  # % campaign movement at sea, every faction
# Multiplier for the bonus of the naval "Full Speed" stance (vanilla +50%).
# 0.7 makes full speed 30% slower as well: (100 - 30 + 35) = 0.7 * (100 + 50).
NAVAL_FULL_SPEED_BONUS_SCALE = 0.5
FORCED_MARCH_MIN_MOVEMENT = 25  # % of movement left required to enter forced march
MOVEMENT_LEFT_AFTER_RAZING_OUTPOST = 0.1  # fraction of max movement
MOVEMENT_LEFT_AFTER_SACKING_OUTPOST = 0.2

# ---------------------------------------------------------------------------
# Buildings
# ---------------------------------------------------------------------------
# Production % of the three province resource chains, by level, and the unit
# upkeep reduction (province) added to their last level.
GRANARY_PRODUCTION = [20, 30, 65]  # vanilla 5-10-20
GRANARY_FOOD_UPKEEP = -15
BRONZEWORKER_PRODUCTION = [10, 20, 35]  # vanilla 5-10-20
BRONZEWORKER_BRONZE_UPKEEP = -10
GOLDSMITH_PRODUCTION = [10, 15, 25]  # vanilla 5-10-20
GOLDSMITH_GOLD_UPKEEP = -5
SUMMER_FESTIVAL_FOOD_PRODUCTION = 40  # vanilla 10
SUMMER_FESTIVAL_HAPPINESS = 2  # vanilla 4
BEER_HALL_FOOD_PRODUCTION = 20  # vanilla 0
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

# ---------------------------------------------------------------------------
# Buildings with garrisons
# ---------------------------------------------------------------------------
# Number of copies of every garrison unit (commanders excluded), compared to vanilla.
SETTLEMENT_GARRISON_MULTIPLIER = 1  # main buildings of major and minor settlements
LOOKOUT_GARRISON_MULTIPLIER = 2  # lookout posts
GARRISON_MULTIPLIER = 4  # every other building with a garrison (garrison buildings, other outposts, landmarks, ...)

# ---------------------------------------------------------------------------
# Progressive difficulty
# ---------------------------------------------------------------------------
# Bonuses for AI factions only (not players, not rebels), applied by a campaign script.
# Tier 0 starts at the first turn below, tier 1 replaces it at the second one, and so on.
# A tier whose values are all 0 gives no bonuses (and has no effect bundle).
# Major factions are the ones the game flags as major; every other AI faction gets the
# "other" values. Each list holds one value per tier: tier 0, 1, 2, 3.
PROGRESSIVE_DIFFICULTY_TURNS = [0, 20, 50, 80]
PROGRESSIVE_DIFFICULTY_MAJOR = {
    "army_upkeep": [-10, -30, -60, -80],  # % upkeep cost of all units
    "recruitment_cost": [-20, -50, -75, -100],  # % recruitment cost of all units
    "income": [20, 60, 90, 150],  # % to all resources produced in every region
    "recruitment_slots": [2, 4, 6, 8],  # local recruitment capacity
    "construction_cost": [0, -20, -40, -60],  # % construction cost of all buildings
    "happiness": [0, 5, 8, 10],  # happiness in every province
}
PROGRESSIVE_DIFFICULTY_OTHER = {
    "army_upkeep": [0, -15, -30, -45],
    "recruitment_cost": [0, -25, -38, -50],
    "income": [0, 20, 30, 40],
    "recruitment_slots": [0, 2, 3, 4],
    "construction_cost": [0, -10, -15, -20],
    "happiness": [0, 2, 4, 5],
}
# The script logs every bundle it applies or removes to the game's script log (when script
# logging is enabled) and to this file in the game folder. None: game script log only.
PROGRESSIVE_DIFFICULTY_LOG_FILE = "dynasties_rebalance.log"
