"""Compatibility add-ons: one extra pack per mod listed in mod.json "compat_addons".

An add-on's rows reference the other mod's buildings, characters or units, so an add-on must only be
enabled together with its mod. Each add-on has a builder below (BUILDERS, by "name"):
- make_character_unique: the unique characters added by that mod can serve in any faction, as the main
  mod does for the game's own (generator/lib/characters.py): permitted in every faction, bodyguard units
  allowed for every unit group, bodyguards for every subculture
- cptt_recruitment_rework: rebalanced effects of that mod's buildings (CPTT_BUILDING_EFFECTS)

The other mod's tables are read from reference/addons/<name>/ (scripts/extract.ps1).
"""

from __future__ import annotations

import glob
import os

from lib.characters import BODYGUARDS, PERMITTED, UNIT_PERMISSIONS, any_faction_rows, unique_subtypes
from lib.data import GameData, fmt_float
from lib.output import clear_folder
from lib.tsv import TsvFile, read_tsv, write_tsv

BEJ = "building_effects_junction_tables"


def _mod_rows(mod_dir: str, table: str) -> list[dict]:
    rows = []
    for path in sorted(glob.glob(os.path.join(mod_dir, "db", table, "*.tsv"))):
        rows.extend(read_tsv(path).dicts())
    return rows


def _make_character_unique(mod_dir: str, data: GameData, settings, addon: dict) -> tuple[dict, str]:
    def combined(table: str) -> list[dict]:
        return list(data.table(table).dicts()) + _mod_rows(mod_dir, table)

    game_subtypes = {row["key"] for row in data.table("agent_subtypes_tables").dicts()}
    added = [row for row in _mod_rows(mod_dir, "agent_subtypes_tables") if row["key"] not in game_subtypes]
    subtypes = unique_subtypes(added, settings.UNIQUE_CHARACTER_KEY_PARTS)
    rows = any_faction_rows(subtypes, combined("factions_tables"), combined("agent_subtypes_tables"),
                            combined(PERMITTED), combined(UNIT_PERMISSIONS), combined(BODYGUARDS))
    # The main mod covers the game's unique characters for the game's factions; the factions this
    # mod adds need them too.
    game_factions = {row["key"] for row in data.table("factions_tables").dicts()}
    new_factions = [row for row in _mod_rows(mod_dir, "factions_tables") if row["key"] not in game_factions]
    # (Their bodyguard copies to every subculture are already in the main mod.)
    game_unique = unique_subtypes(list(data.table("agent_subtypes_tables").dicts()), settings.UNIQUE_CHARACTER_KEY_PARTS)
    extra = any_faction_rows(game_unique, new_factions, combined("agent_subtypes_tables"), combined(PERMITTED),
                             combined(UNIT_PERMISSIONS), list(data.table(BODYGUARDS).dicts()))
    rows.permitted += extra.permitted
    rows.unit_permissions += extra.unit_permissions
    tables = {PERMITTED: rows.permitted, UNIT_PERMISSIONS: rows.unit_permissions, BODYGUARDS: rows.bodyguards}
    summary = (f"{addon['title']} add-on ({addon['pack']}): {len(subtypes)} unique characters can serve "
               f"in any of the {rows.factions} factions: {len(rows.permitted)} permitted subtypes, "
               f"{len(rows.units)} bodyguard units allowed for {rows.groups} unit groups "
               f"({len(rows.unit_permissions)} rows), {len(rows.bodyguards)} bodyguards copied to every "
               f"subculture; the game's unique characters can also serve in the factions it adds "
               f"({len(new_factions)}). Characters: {', '.join(subtypes)}.")
    return tables, summary


def _cptt_recruitment_rework(mod_dir: str, data: GameData, settings, addon: dict) -> tuple[dict, str]:
    buildings = {row["level_name"] for row in _mod_rows(mod_dir, "building_levels_tables")}
    effects = {row["effect"] for row in data.table("effects_tables").dicts()}
    rows = []
    for building, building_effects in settings.CPTT_BUILDING_EFFECTS.items():
        if building not in buildings:
            raise ValueError(f"CPTT_BUILDING_EFFECTS: {addon['title']} has no building {building}")
        for (effect, scope), spec in building_effects.items():
            if effect not in effects:
                raise ValueError(f"CPTT_BUILDING_EFFECTS ({building}): unknown effect {effect}")
            if isinstance(spec, tuple):
                value, damaged, ruined, low, medium = spec
            else:
                value, damaged, ruined, low, medium = spec, 0, 0, spec, spec
            rows.append({"building": building, "effect": effect, "effect_scope": scope,
                         **{column: fmt_float(v) for column, v in (
                             ("value", value), ("value_damaged", damaged), ("value_ruined", ruined),
                             ("value_low_influence", low), ("value_medium_influence", medium))}})
    summary = (f"{addon['title']} add-on ({addon['pack']}): effects of {len(settings.CPTT_BUILDING_EFFECTS)} "
               f"buildings ({len(rows)} rows, CPTT_BUILDING_EFFECTS).")
    return {BEJ: rows}, summary


# mod.json "compat_addons" name -> (builder(mod_dir, data, settings, addon) -> ({table: rows}, summary),
# section of the change report).
BUILDERS = {
    "make_character_unique": (_make_character_unique, "characters"),
    "cptt_recruitment_rework": (_cptt_recruitment_rework, "buildings"),
}


def generate_addons(root: str, data: GameData, settings, mod: dict) -> list[tuple[str, str]]:
    """Write src_addons/<name>/ for each add-on; returns (report section, summary line) per add-on."""
    out_root = os.path.join(root, "src_addons")
    clear_folder(out_root)
    summaries = []
    for addon in mod.get("compat_addons", []):
        name = addon["name"]
        if name not in BUILDERS:
            raise ValueError(f"mod.json compat_addons: no builder for {name}")
        mod_dir = os.path.join(root, "reference", "addons", name)
        builder, section = BUILDERS[name]
        if not os.path.isdir(os.path.join(mod_dir, "db")):
            summaries.append((section, f"{addon['title']}: not generated, run scripts\\extract.ps1 first "
                             f"(needs the Workshop mod {addon['workshop_id']})."))
            continue
        tables, summary = builder(mod_dir, data, settings, addon)
        file_name = f"{mod['file_prefix']}compat_{name}"
        for table, table_rows in tables.items():
            if not table_rows:
                continue
            game = data.table(table)
            values = [[row.get(column, "") for column in game.columns] for row in table_rows]
            path = os.path.join(out_root, name, "db", table, file_name + ".tsv")
            write_tsv(path, TsvFile(game.columns, table, game.version, f"db/{table}/{file_name}", values))
        summaries.append((section, summary))
    return summaries
