"""Progressive difficulty."""

# Bonuses for AI factions only (not players, not rebels), applied by a campaign script.
# Tier 0 starts at the first turn below, tier 1 replaces it at the second one, and so on.
# A tier whose values are all 0 gives no bonuses (and has no effect bundle).
# Major factions are the ones the game flags as major; every other AI faction gets the
# "other" values. Each list holds one value per tier: tier 0, 1, 2, 3.
PROGRESSIVE_DIFFICULTY_TURNS = [0, 20, 50, 80]
PROGRESSIVE_DIFFICULTY_MAJOR = {
    "army_upkeep": [-10, -30, -80, -100],  # % upkeep cost of all units
    "recruitment_cost": [-20, -50, -80, -100],  # % recruitment cost of all units
    "income": [20, 60, 120, 180],  # % to all resources produced in every region
    "recruitment_slots": [2, 6, 12, 20],  # local recruitment capacity
    "construction_cost": [0, -20, -60, -100],  # % construction cost of all buildings
    "building_upkeep": [-80, -80, -80, -80],  # % building upkeep (resources: PROGRESSIVE_DIFFICULTY_BUILDING_UPKEEP_RESOURCES)
    "happiness": [0, 5, 8, 10],  # happiness in every province
}
PROGRESSIVE_DIFFICULTY_OTHER = {
    "army_upkeep": [0, -15, -40, -65],
    "recruitment_cost": [0, -25, -50, -75],
    "income": [0, 20, 30, 50],
    "recruitment_slots": [0, 2, 6, 10],
    "construction_cost": [0, -10, -20, -40],
    "building_upkeep": [-80, -80, -80, -80],
    "happiness": [0, 2, 4, 5],
}
# Resources of the "building_upkeep" bonus (food, bronze, gold, stones, wood).
PROGRESSIVE_DIFFICULTY_BUILDING_UPKEEP_RESOURCES = ["gold", "stones", "wood"]
# The script logs every bundle it applies or removes to the game's script log (when script
# logging is enabled) and to this file in the game folder. None: game script log only.
PROGRESSIVE_DIFFICULTY_LOG_FILE = "dynasties_rebalance.log"
