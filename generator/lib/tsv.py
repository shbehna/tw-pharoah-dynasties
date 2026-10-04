"""Read and write tables in the TSV format used by RPFM (Rusted PackFile Manager).

Layout of an RPFM TSV file:

    line 1   column names, tab separated
    line 2   "#<table_name>;<version>;<path inside the pack>" (padded with tabs)
    line 3+  one row per line, tab separated

Strings are stored verbatim. Embedded tabs/newlines are already escaped by RPFM
as the two-character sequences "\\t" / "\\n", so a plain split on real tab
characters is a lossless round trip.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass
class TsvFile:
    columns: list[str]
    table: str  # e.g. "building_effects_junction_tables" or "Loc"
    version: int
    path: str  # path inside the pack, e.g. "db/building_effects_junction_tables/data__"
    rows: list[list[str]] = field(default_factory=list)

    def index(self, column: str) -> int:
        return self.columns.index(column)

    def dicts(self):
        for row in self.rows:
            yield dict(zip(self.columns, row))


def read_tsv(file_path: str) -> TsvFile:
    with open(file_path, encoding="utf-8", newline="") as handle:
        lines = handle.read().split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    lines = [line[:-1] if line.endswith("\r") else line for line in lines]
    columns = lines[0].split("\t")
    meta = lines[1].split("\t")[0]
    if not meta.startswith("#"):
        raise ValueError(f"{file_path}: second line is not RPFM metadata: {meta!r}")
    table, version, path = meta[1:].split(";", 2)
    rows = []
    for line in lines[2:]:
        if line == "":
            continue
        values = line.split("\t")
        if len(values) < len(columns):
            values += [""] * (len(columns) - len(values))
        rows.append(values[: len(columns)])
    return TsvFile(columns=columns, table=table, version=int(version), path=path, rows=rows)


def write_tsv(file_path: str, tsv: TsvFile) -> None:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    width = len(tsv.columns)
    out = ["\t".join(tsv.columns), f"#{tsv.table};{tsv.version};{tsv.path}" + "\t" * (width - 1)]
    for row in tsv.rows:
        if len(row) != width:
            raise ValueError(f"{file_path}: row has {len(row)} values, expected {width}: {row}")
        out.append("\t".join(row))
    with open(file_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(out) + "\n")
