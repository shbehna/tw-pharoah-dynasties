"""Compare the mod (src/) with the mods enabled in the launcher and write docs/CONFLICTS.md.

Usage:  scripts/extract.ps1 -ActiveMods   (once, to extract the enabled mods)
        python generator/conflicts.py

How the game resolves overlaps: when two table files define a row with the same key,
the row from the file whose name sorts first wins. That is why mods prefix their table
files with "!" or "@". This mod's files start with 16 "!" so they win almost always.
"""

from __future__ import annotations

import collections
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "generator"))

from lib.schema import Schema  # noqa: E402
from lib.tsv import read_tsv  # noqa: E402

EXAMPLES = 5
RELEVANT_SCRIPTS = {
    "script/campaign/supply_points.lua": "computes the administrative burden and its tiers. This mod sets the "
    "tier thresholds when the campaign loads, so its values apply on top of a replaced copy too; but an "
    "outdated copy still undoes the game's later fixes to the rest of that script.",
}


def key_columns(schema: Schema, table: str, version: int) -> list[str]:
    try:
        return schema.key_columns(table, version)
    except KeyError:
        return []


def load_mod_rows(schema: Schema, src_dir: str):
    """Our rows: table -> key -> (file name, row dict)."""
    rows = collections.defaultdict(dict)
    for path in glob.glob(os.path.join(src_dir, "db", "*", "*.tsv")):
        tsv = read_tsv(path)
        keys = key_columns(schema, tsv.table, tsv.version)
        name = os.path.basename(path)[:-4]
        for row in tsv.dicts():
            rows[tsv.table][tuple(row[k] for k in keys)] = (name, row)
    return rows


def load_loc_keys(folder: str) -> set[str]:
    keys = set()
    for path in glob.glob(os.path.join(folder, "text", "**", "*.loc.tsv"), recursive=True):
        keys |= {row[0] for row in read_tsv(path).rows}
    return keys


def main() -> int:
    with open(os.path.join(ROOT, "mod.json"), encoding="utf-8") as handle:
        mod = json.load(handle)
    schema = Schema(os.path.join(ROOT, "tools", "schemas", "schema_ph_dyn.json"))
    active_dir = os.path.join(ROOT, "reference", "active_mods")
    order_file = os.path.join(active_dir, "load_order.txt")
    if not os.path.exists(order_file):
        print("Run scripts/extract.ps1 -ActiveMods first.", file=sys.stderr)
        return 1
    with open(order_file, encoding="utf-8-sig") as handle:
        enabled = [line.strip() for line in handle if line.strip()]

    ours = load_mod_rows(schema, os.path.join(ROOT, "src"))
    our_texts = load_loc_keys(os.path.join(ROOT, "src"))
    script_list = os.path.join(ROOT, "reference", "vanilla", "script_files.txt")
    game_scripts = set()
    if os.path.exists(script_list):
        with open(script_list, encoding="utf-8-sig") as handle:
            game_scripts = {line.strip() for line in handle if line.strip()}

    redundant, overlaps, undecoded, replaced_scripts = [], [], [], []
    for label in enabled:
        folder = os.path.join(active_dir, label)
        scripts = [p for p in glob.glob(os.path.join(folder, "script", "**", "*"), recursive=True) if os.path.isfile(p)]
        for path in scripts:
            relative = os.path.relpath(path, folder).replace(os.sep, "/")
            if relative in game_scripts:
                replaced_scripts.append((label, relative))

        per_table = collections.defaultdict(lambda: {"theirs_win": 0, "ours_win": 0, "same": 0, "examples": []})
        rows_total = rows_covered = 0
        has_binary = False
        for path in sorted(glob.glob(os.path.join(folder, "db", "*", "*"))):
            if not path.endswith(".tsv"):
                undecoded.append(os.path.relpath(path, active_dir))
                has_binary = True
                continue
            tsv = read_tsv(path)
            rows_total += len(tsv.rows)
            keys = key_columns(schema, tsv.table, tsv.version)
            if tsv.table not in ours or not keys:
                continue
            their_file = os.path.basename(path)[:-4]
            for row in tsv.dicts():
                key = tuple(row.get(k, "") for k in keys)
                if key not in ours[tsv.table]:
                    continue
                rows_covered += 1
                our_file, our_row = ours[tsv.table][key]
                stats = per_table[tsv.table]
                differing = {c: (row[c], our_row[c]) for c in our_row if c in row and row[c] != our_row[c]}
                if not differing:
                    stats["same"] += 1
                    continue
                stats["ours_win" if our_file < their_file else "theirs_win"] += 1
                if len(stats["examples"]) < EXAMPLES:
                    detail = ", ".join(f"{c}: theirs {t} / ours {o}" for c, (t, o) in differing.items())
                    stats["examples"].append(f"`{' / '.join(key)}` — {detail}")

        texts = load_loc_keys(folder)
        fully_covered = rows_covered == rows_total and texts <= our_texts
        if (rows_total or texts) and fully_covered and not scripts and not has_binary:
            redundant.append(label)
            continue
        for table, stats in per_table.items():
            if stats["ours_win"] or stats["theirs_win"]:
                overlaps.append((label, table, stats))

    lines = [
        "# Conflicts with the enabled mods",
        "",
        "Generated by `generator/conflicts.py` from the mods enabled in the launcher; do not edit by hand.",
        "When two mods define the same row, the table file whose name sorts first wins "
        f"(this mod's files start with `{mod['file_prefix']}`).",
        "",
        "## Redundant: disable them",
        "",
        "Every row and text these mods define is also defined by this mod, so they have no effect while it is enabled.",
        "",
    ]
    lines += [f"- {label}" for label in redundant] or ["- none"]
    lines += ["", "## Mods changing some of the same rows", "",
              "The rest of these mods still applies.", ""]
    if not overlaps:
        lines.append("None.")
    for label, table, stats in sorted(overlaps):
        lines.append(f"### {label} — `{table}`")
        lines.append("")
        lines.append(f"{stats['ours_win'] + stats['theirs_win']} rows with different values "
                     f"(this mod wins {stats['ours_win']}, the other mod wins {stats['theirs_win']}); "
                     f"{stats['same']} identical rows.")
        lines.append("")
        lines += [f"- {e}" for e in stats["examples"]]
        lines.append("")
    lines += ["## Mods replacing game scripts", "",
              "These mods ship their own copy of a game script, which replaces the game's version.", ""]
    relevant = [(l, s) for l, s in sorted(replaced_scripts) if s in RELEVANT_SCRIPTS]
    other = [(l, s) for l, s in sorted(replaced_scripts) if s not in RELEVANT_SCRIPTS]
    if relevant:
        lines += ["Related to this mod:", ""]
        lines += [f"- **{label}**: `{script}` — {RELEVANT_SCRIPTS[script]}" for label, script in relevant]
        lines.append("")
    if other:
        lines += ["Not related to this mod: " + "; ".join(f"{label} (`{script}`)" for label, script in other), ""]
    if not replaced_scripts:
        lines += ["- none", ""]
    if undecoded:
        lines += ["## Tables that could not be checked", "", "The schema could not decode these files:", ""]
        lines += [f"- `{p}`" for p in undecoded]
    path = os.path.join(ROOT, "docs", "CONFLICTS.md")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines).rstrip() + "\n")
    print(f"Wrote {os.path.relpath(path, ROOT)}: {len(redundant)} redundant mods, "
          f"{len(overlaps)} overlapping mod/table pairs, {len(replaced_scripts)} replaced game scripts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
