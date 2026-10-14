"""Compatibility add-ons: one extra pack per mod listed in mod.json "compat_addons".

Each add-on lets the unique characters added by that mod serve in any faction, as the main mod does
for the game's own (generator/lib/characters.py): permitted in every faction, bodyguard units allowed
for every unit group, bodyguards for every subculture. Its rows reference the other mod's characters
and units, so an add-on must only be enabled together with its mod.

The other mod's tables are read from reference/addons/<name>/ (scripts/extract.ps1).
"""

from __future__ import annotations

import glob
import os

from lib.characters import BODYGUARDS, PERMITTED, UNIT_PERMISSIONS, any_faction_rows, unique_subtypes
from lib.data import GameData
from lib.output import clear_folder
from lib.tsv import TsvFile, read_tsv, write_tsv


def _mod_rows(mod_dir: str, table: str) -> list[dict]:
    rows = []
    for path in sorted(glob.glob(os.path.join(mod_dir, "db", table, "*.tsv"))):
        rows.extend(read_tsv(path).dicts())
    return rows


def generate_addons(root: str, data: GameData, settings, mod: dict) -> list[str]:
    """Write src_addons/<name>/ for each add-on; returns one summary line per add-on."""
    out_root = os.path.join(root, "src_addons")
    clear_folder(out_root)
    summaries = []
    for addon in mod.get("compat_addons", []):
        name = addon["name"]
        mod_dir = os.path.join(root, "reference", "addons", name)
        if not os.path.isdir(os.path.join(mod_dir, "db")):
            summaries.append(f"{addon['title']}: not generated, run scripts\\extract.ps1 first "
                             f"(needs the Workshop mod {addon['workshop_id']}).")
            continue

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

        file_name = f"{mod['file_prefix']}compat_{name}"
        for table, table_rows in ((PERMITTED, rows.permitted), (UNIT_PERMISSIONS, rows.unit_permissions),
                                  (BODYGUARDS, rows.bodyguards)):
            if not table_rows:
                continue
            game = data.table(table)
            values = [[row.get(column, "") for column in game.columns] for row in table_rows]
            path = os.path.join(out_root, name, "db", table, file_name + ".tsv")
            write_tsv(path, TsvFile(game.columns, table, game.version, f"db/{table}/{file_name}", values))
        summaries.append(f"{addon['title']} add-on ({addon['pack']}): {len(subtypes)} unique characters can serve "
                         f"in any of the {rows.factions} factions: {len(rows.permitted)} permitted subtypes, "
                         f"{len(rows.units)} bodyguard units allowed for {rows.groups} unit groups "
                         f"({len(rows.unit_permissions)} rows), {len(rows.bodyguards)} bodyguards copied to every "
                         f"subculture; the game's unique characters can also serve in the factions it adds "
                         f"({len(new_factions)}). Characters: {', '.join(subtypes)}.")
    return summaries
