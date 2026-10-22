"""Movement."""

LAND_MOVEMENT = -30  # % campaign movement on land, every faction (player and AI)
NAVAL_MOVEMENT = -50  # % campaign movement at sea, every faction
# Multiplier for the bonus of the naval "Full Speed" stance (vanilla +50%).
# 0.7 makes full speed 30% slower as well: (100 - 30 + 35) = 0.7 * (100 + 50).
NAVAL_FULL_SPEED_BONUS_SCALE = 0.5
FORCED_MARCH_MIN_MOVEMENT = 25  # % of movement left required to enter forced march
MOVEMENT_LEFT_AFTER_RAZING_OUTPOST = 0.1  # fraction of max movement
MOVEMENT_LEFT_AFTER_SACKING_OUTPOST = 0.2
