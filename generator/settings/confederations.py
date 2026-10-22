"""Confederations at the start of a campaign (separate mod: dynasties_start_confederations.pack)."""

# When a new campaign starts, a faction played by a human confederates the AI factions that own these
# regions (campaign script; players and rebels are left alone). Faction key -> region keys.
START_CONFEDERATIONS = {
    "phar_map_ninurta": ["phar_map_hanigalbat_sangaritu"],  # Hanigalbat: the owner of Sangaritu
}
# File in the game folder the script logs to (None: game script log only).
START_CONFEDERATIONS_LOG_FILE = "dynasties_rebalance.log"
