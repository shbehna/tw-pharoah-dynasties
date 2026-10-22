"""Unique characters."""

# A character is unique when it is immortal or its character subtype key contains one of these
# (the game's legendary characters, and the ones added by mods that follow the same naming, e.g.
# phar_mod_hero_... and phar_mcu_hero_...).
UNIQUE_CHARACTER_KEY_PARTS = ["_hero_"]
# When an AI faction is destroyed, its unique characters join a human player: the faction that
# destroyed it if it is a human player, else the first human player.
UNIQUE_CHARACTERS_JOIN_PLAYER = True
# A unique general of a human player that is not on the map (no army) and is not wounded, and has
# never led an army for that player, appears next to the faction's capital, alone: the army is
# created with this unit, which is removed right away. Once per character: a general whose army
# is disbanded afterwards does not come back.
UNIQUE_CHARACTER_PLACEHOLDER_UNIT = "phar_main_nat_low_lower_egyptian_militia"
