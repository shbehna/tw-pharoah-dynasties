"""Separate mods: one extra pack per entry of mod.json "separate_mods".

Unlike the compatibility add-ons, these packs do not depend on any other mod (the main mod
included): each can be enabled on its own. Their source is written to src_mods/<name>/.
"""

from __future__ import annotations

import os

from features import confederations
from lib.data import GameData
from lib.output import clear_folder

# mod.json "separate_mods" name -> module with build(data, settings) -> (scripts, notes).
BUILDERS = {
    "start_confederations": confederations,
}


def generate_separate_mods(root: str, data: GameData, settings, mod: dict) -> list[tuple[dict, list[str]]]:
    """Write src_mods/<name>/ for each separate mod; returns (mod.json entry, notes) for each."""
    out_root = os.path.join(root, "src_mods")
    clear_folder(out_root)
    results = []
    for entry in mod.get("separate_mods", []):
        name = entry["name"]
        if name not in BUILDERS:
            raise ValueError(f"mod.json separate_mods: no builder for {name}")
        scripts, notes = BUILDERS[name].build(data, settings)
        for pack_path, content in sorted(scripts.items()):
            path = os.path.join(out_root, name, *pack_path.split("/"))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(content)
        results.append((entry, notes))
    return results
