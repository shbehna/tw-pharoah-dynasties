"""Game data access (vanilla + the mod's data files) and the overlay that holds the mod's changes.

The overlay is the in-memory version of the mod: for every table it stores the
rows the mod adds or overrides, keyed by the table's key columns. Features read
the *effective* data (vanilla with the overlay applied on top) and write new
rows into the overlay, so later features see the result of earlier ones.
"""

from __future__ import annotations

import glob
import os
from dataclasses import dataclass, field

from .schema import Schema
from .tsv import TsvFile, read_tsv


def fmt_float(value: float) -> str:
    return f"{value:.4f}"


def _format_default(default: str, field_type: str) -> str:
    """Schema defaults written the way RPFM writes values (e.g. F32 "0" -> "0.0000")."""
    if field_type == "F32" and default not in ("", None):
        try:
            return fmt_float(float(default))
        except ValueError:
            return default
    return default


def fmt_value(value, field_type: str) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, bool):
        return "true" if value else "false"
    if field_type == "F32":
        return fmt_float(float(value))
    if field_type in ("I32", "I64", "OptionalI64"):
        return str(int(value))
    return str(value)


class GameData:
    """Read-only access to the game data extracted by scripts/extract.ps1 (reference/)
    and to the mod's own data files (generator/data/)."""

    def __init__(self, reference_dir: str, data_dir: str, schema: Schema):
        self.reference_dir = reference_dir
        self.data_dir = data_dir
        self.schema = schema
        self._tables: dict[str, TsvFile] = {}
        self._loc: dict[str, str] | None = None

    # -- vanilla -------------------------------------------------------------
    def table(self, name: str) -> TsvFile:
        if name not in self._tables:
            path = os.path.join(self.reference_dir, "vanilla", "db", name, "data__.tsv")
            if not os.path.exists(path):
                raise FileNotFoundError(f"Vanilla table not extracted: {path} (run scripts/extract.ps1)")
            self._tables[name] = read_tsv(path)
        return self._tables[name]

    def loc(self) -> dict[str, str]:
        """English localisation, key -> text."""
        if self._loc is None:
            self._loc = {}
            for path in glob.glob(os.path.join(self.reference_dir, "vanilla", "text", "db", "*.loc.tsv")):
                for row in read_tsv(path).rows:
                    self._loc[row[0]] = row[1]
        return self._loc

    # -- the mod's own data files ------------------------------------------------
    def data_tables(self, name: str) -> list[TsvFile]:
        """Tables in generator/data/<name>/db/<table>/*.tsv."""
        paths = sorted(glob.glob(os.path.join(self.data_dir, name, "db", "*", "*.tsv")))
        if not paths:
            raise FileNotFoundError(f"No tables in {os.path.join(self.data_dir, name, 'db')}")
        return [read_tsv(p) for p in paths]

    def data_locs(self, name: str) -> list[TsvFile]:
        """Texts in generator/data/<name>/text/db/*.loc.tsv."""
        return [read_tsv(p) for p in sorted(glob.glob(os.path.join(self.data_dir, name, "text", "db", "*.loc.tsv")))]


@dataclass
class OverlayRow:
    values: list[str]
    feature: str


@dataclass
class OverlayTable:
    name: str
    version: int
    columns: list[str]
    types: list[str]
    defaults: list[str]
    key_index: list[int]
    rows: dict[tuple, OverlayRow] = field(default_factory=dict)

    def key_of(self, values: list[str]) -> tuple:
        return tuple(values[i] for i in self.key_index)


@dataclass
class LocEntry:
    text: str
    feature: str
    tooltip: str = "false"


class Overlay:
    def __init__(self, data: GameData):
        self.data = data
        self.tables: dict[str, OverlayTable] = {}
        self.loc: dict[str, LocEntry] = {}
        self.scripts: dict[str, tuple[str, str]] = {}  # pack path -> (content, feature)
        self.notes: list[tuple[str, str]] = []  # (feature, text) for the change report
        self._vanilla_by_key: dict[str, dict[tuple, list[str]]] = {}

    # -- tables ----------------------------------------------------------------
    def table(self, name: str) -> OverlayTable:
        if name not in self.tables:
            vanilla = self.data.table(name)
            # RPFM writes key columns first in its TSV files, so match schema fields by name.
            fields = {f.name: f for f in self.data.schema.fields(name, vanilla.version)}
            if set(fields) != set(vanilla.columns):
                raise ValueError(f"Schema columns for {name} v{vanilla.version} do not match the extracted table")
            ordered = [fields[c] for c in vanilla.columns]
            self.tables[name] = OverlayTable(
                name=name,
                version=vanilla.version,
                columns=vanilla.columns,
                types=[f.field_type for f in ordered],
                defaults=[_format_default(f.default, f.field_type) for f in ordered],
                key_index=[i for i, f in enumerate(ordered) if f.is_key],
            )
        return self.tables[name]

    def _vanilla_index(self, name: str) -> dict[tuple, list[str]]:
        if name not in self._vanilla_by_key:
            table = self.table(name)
            self._vanilla_by_key[name] = {table.key_of(row): row for row in self.data.table(name).rows}
        return self._vanilla_by_key[name]

    def to_values(self, name: str, row) -> list[str]:
        """Convert a dict (column -> value) or a full list into a list of formatted strings."""
        table = self.table(name)
        if isinstance(row, dict):
            unknown = set(row) - set(table.columns)
            if unknown:
                raise KeyError(f"{name}: unknown columns {sorted(unknown)}")
            return [
                fmt_value(row[c], t) if c in row else d
                for c, t, d in zip(table.columns, table.types, table.defaults)
            ]
        if len(row) != len(table.columns):
            raise ValueError(f"{name}: expected {len(table.columns)} values, got {len(row)}")
        return [fmt_value(v, t) for v, t in zip(row, table.types)]

    def put(self, name: str, row, feature: str) -> tuple:
        """Add or replace a row; `feature` decides which file of the mod it is written to."""
        table = self.table(name)
        values = self.to_values(name, row)
        key = table.key_of(values)
        table.rows[key] = OverlayRow(values=values, feature=feature)
        return key

    def get(self, name: str, key: tuple) -> dict | None:
        """Effective row for `key` (the mod's if it changed it, else the game's), as a copy."""
        table = self.table(name)
        if key in table.rows:
            return dict(zip(table.columns, table.rows[key].values))
        vanilla = self._vanilla_index(name).get(key)
        return dict(zip(table.columns, vanilla)) if vanilla is not None else None

    def vanilla(self, name: str, key: tuple) -> dict | None:
        table = self.table(name)
        row = self._vanilla_index(name).get(key)
        return dict(zip(table.columns, row)) if row is not None else None

    def rows(self, name: str):
        """Effective rows (vanilla with the overlay applied), as dicts."""
        table = self.table(name)
        vanilla = self._vanilla_index(name)
        for key, values in vanilla.items():
            override = table.rows.get(key)
            yield dict(zip(table.columns, override.values if override else values))
        for key, row in table.rows.items():
            if key not in vanilla:
                yield dict(zip(table.columns, row.values))

    def import_rows(self, tsv: TsvFile, feature: str, transform=None) -> int:
        """Copy the rows of a mod table into the overlay (columns are matched by name).

        `transform(row) -> row | None` can rewrite or skip rows on the way in.
        """
        table = self.table(tsv.table)
        if tsv.version != table.version:
            self.note(feature, f"{tsv.path}: table version {tsv.version} differs from the game's "
                               f"{table.version}; columns were matched by name")
        count = 0
        for row in tsv.dicts():
            if transform is not None:
                row = transform(row)
                if row is None:
                    continue
            self.put(tsv.table, {c: v for c, v in row.items() if c in table.columns}, feature)
            count += 1
        return count

    # -- localisation -----------------------------------------------------------
    def put_loc(self, key: str, text: str, feature: str, tooltip: str = "false") -> None:
        self.loc[key] = LocEntry(text=text, feature=feature, tooltip=tooltip)

    # -- scripts ----------------------------------------------------------------
    def put_script(self, pack_path: str, content: str, feature: str) -> None:
        self.scripts[pack_path] = (content, feature)

    def note(self, feature: str, text: str) -> None:
        self.notes.append((feature, text))
