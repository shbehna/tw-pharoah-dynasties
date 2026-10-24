"""Generate the mod source (src/) from the game data and the mod's data files.

Usage:  python generator/generate.py

Needs the game data extracted by scripts/extract.ps1 and the schema downloaded by
scripts/setup.ps1. All tunable values are in generator/settings/ (one module per section);
the rebuilt landmarks (new building levels, texts) are in generator/data/.
"""

from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "generator"))

import settings  # noqa: E402
from addons import generate_addons  # noqa: E402
from features import (admin, ai, buildings, characters, difficulty, experience, garrisons, landmarks,  # noqa: E402
                      movement, outposts, religion)
from lib.data import GameData, Overlay  # noqa: E402
from lib.output import drop_unchanged, write_source  # noqa: E402
from lib.report import write_report  # noqa: E402
from lib.schema import Schema  # noqa: E402
from separate_mods import generate_separate_mods  # noqa: E402

# Order matters: later features see (and may change) the rows written by earlier ones.
# Landmarks run first so the production multiplier and garrison doubling include them.
FEATURES = [landmarks, admin, outposts, movement, buildings, religion, garrisons, experience, difficulty, ai, characters]
# Section order of CHANGELOG.md, used for the report.
REPORT_ORDER = ["admin", "outposts", "movement", "landmarks", "buildings", "religion", "garrisons", "experience",
                "difficulty", "ai", "characters", "confederations"]


def main() -> int:
    with open(os.path.join(ROOT, "mod.json"), encoding="utf-8") as handle:
        mod = json.load(handle)
    schema_path = os.path.join(ROOT, "tools", "schemas", "schema_ph_dyn.json")
    if not os.path.exists(schema_path):
        print("Schema missing: run scripts/setup.ps1 first.", file=sys.stderr)
        return 1

    data = GameData(os.path.join(ROOT, "reference"), os.path.join(ROOT, "generator", "data"), Schema(schema_path))
    overlay = Overlay(data)
    for feature in FEATURES:
        print(f"- {feature.FEATURE}")
        feature.apply(overlay, settings)

    dropped = drop_unchanged(overlay)
    written = write_source(overlay, os.path.join(ROOT, "src"), mod["file_prefix"])
    addons = generate_addons(ROOT, data, settings, mod)
    for section, summary in addons:
        overlay.note(section, summary)
    separate = generate_separate_mods(ROOT, data, settings, mod)
    for entry, notes in separate:
        overlay.note("confederations", f"Separate mod {entry['pack']} (src_mods/{entry['name']}/), "
                                       f"independent of the main pack:")
        for note in notes:
            overlay.note("confederations", note)
    write_report(overlay, os.path.join(ROOT, "docs", "CHANGES.md"), REPORT_ORDER, mod["file_prefix"])

    rows = sum(len(t.rows) for t in overlay.tables.values())
    print(f"Wrote {len(written)} files to src/ ({rows} table rows, {len(overlay.loc)} texts, "
          f"{len(overlay.scripts)} scripts; {dropped} rows identical to the game were left out).")
    for _section, summary in addons:
        print(f"Add-on: {summary[:160]}")
    for entry, _notes in separate:
        print(f"Separate mod: {entry['title']} ({entry['pack']}) in src_mods/{entry['name']}/")
    print("Change report: docs/CHANGES.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
