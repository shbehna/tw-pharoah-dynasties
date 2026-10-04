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
MAJOR_SETTLEMENT_ADMIN_COST = [2, 3, 4, 8, 12]  # vanilla 2-3-4-5-6
MINOR_SETTLEMENT_ADMIN_COST = [2, 4, 6]  # vanilla 2-3-4
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
TRADING_POST_RESOURCE_PRODUCTION = 25  # % to all resources in the region (vanilla 10)
FORT_MAX_UNITS = 20  # vanilla 10
WARRIORS_REFUGE_MAX_UNITS = 15  # vanilla 6
FORT_UPKEEP_REDUCTION = 90  # % (vanilla 50)
WARRIORS_REFUGE_UPKEEP_REDUCTION = 30  # % (vanilla 0)
WAYSTATION_HAPPINESS = 3  # province happiness (vanilla 0)
MONUMENT_ENEMY_MOVEMENT_PROVINCE = -10  # % campaign movement of enemy armies in the province
LOOKOUT_ENEMY_MOVEMENT_REGION = -10  # % campaign movement of enemy armies in the region
LOOKOUT_ENEMY_MOVEMENT_PROVINCE = -2.5  # % campaign movement of enemy armies in the province

# ---------------------------------------------------------------------------
# Movement
# ---------------------------------------------------------------------------
LAND_MOVEMENT = -30  # % campaign movement on land, every faction (player and AI)
NAVAL_MOVEMENT = -30  # % campaign movement at sea, every faction
# Multiplier for the bonus of the naval "Full Speed" stance (vanilla +50%).
# 0.7 makes full speed 30% slower as well: (100 - 30 + 35) = 0.7 * (100 + 50).
NAVAL_FULL_SPEED_BONUS_SCALE = 0.7
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
GOLDSMITH_GOLD_UPKEEP = -10
SUMMER_FESTIVAL_FOOD_PRODUCTION = 40  # vanilla 10
SUMMER_FESTIVAL_HAPPINESS = 2  # vanilla 4
BEER_HALL_FOOD_PRODUCTION = 20  # vanilla 0
# Every other building with a resource production % bonus gets it multiplied by this.
# This includes main settlement buildings (+% to all resources in the region) and landmarks.
OTHER_PRODUCTION_MULTIPLIER = 2
# Regular expressions of building keys left out of the multiplier, e.g. r"_main_building_"
# to keep settlement buildings at their vanilla production bonus.
OTHER_PRODUCTION_EXCLUDE = []

# ---------------------------------------------------------------------------
# Buildings with garrisons
# ---------------------------------------------------------------------------
# Number of copies of every garrison unit (commanders excluded), compared to vanilla.
SETTLEMENT_GARRISON_MULTIPLIER = 1  # main buildings of major and minor settlements
GARRISON_MULTIPLIER = 4  # every other building with a garrison (garrison buildings, outposts, landmarks, ...)
