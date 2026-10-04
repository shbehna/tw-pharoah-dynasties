"""Write the overlay to the mod source folder (src/) in RPFM TSV format."""

from __future__ import annotations

import collections
import os
import shutil

from .data import Overlay
from .tsv import TsvFile, write_tsv


def drop_unchanged(overlay: Overlay) -> int:
    """Remove overlay rows that are identical to vanilla: they would only add conflicts."""
    dropped = 0
    for name, table in overlay.tables.items():
        for key in list(table.rows):
            vanilla = overlay.vanilla(name, key)
            if vanilla is not None and list(vanilla.values()) == table.rows[key].values:
                del table.rows[key]
                dropped += 1
    return dropped


def clear_folder(path: str) -> None:
    """Delete the folder's contents but keep the folder (it may be open in an editor or shell)."""
    os.makedirs(path, exist_ok=True)
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            shutil.rmtree(entry.path)
        else:
            os.remove(entry.path)


def write_source(overlay: Overlay, src_dir: str, prefix: str) -> list[str]:
    clear_folder(src_dir)
    written = []

    for name, table in sorted(overlay.tables.items()):
        by_feature: dict[str, list[list[str]]] = collections.defaultdict(list)
        for row in table.rows.values():
            by_feature[row.feature].append(row.values)
        for feature, rows in sorted(by_feature.items()):
            file_name = f"{prefix}{feature}"
            path = os.path.join(src_dir, "db", name, file_name + ".tsv")
            write_tsv(path, TsvFile(table.columns, name, table.version, f"db/{name}/{file_name}", rows))
            written.append(path)

    by_feature_loc: dict[str, list[list[str]]] = collections.defaultdict(list)
    for key, entry in overlay.loc.items():
        by_feature_loc[entry.feature].append([key, entry.text, entry.tooltip])
    for feature, rows in sorted(by_feature_loc.items()):
        file_name = f"{prefix}{feature}.loc"
        path = os.path.join(src_dir, "text", "db", file_name + ".tsv")
        write_tsv(path, TsvFile(["key", "text", "tooltip"], "Loc", 1, f"text/db/{file_name}", rows))
        written.append(path)

    for pack_path, (content, _feature) in sorted(overlay.scripts.items()):
        path = os.path.join(src_dir, *pack_path.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
        written.append(path)
    return written
