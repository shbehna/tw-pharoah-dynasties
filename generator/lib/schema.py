"""Access to RPFM's table schema (field names, types and key columns)."""

from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass(frozen=True)
class Field:
    name: str
    field_type: str
    is_key: bool
    default: str


class Schema:
    def __init__(self, json_path: str):
        with open(json_path, encoding="utf-8") as handle:
            self._definitions = json.load(handle)["definitions"]

    def fields(self, table: str, version: int) -> list[Field]:
        for definition in self._definitions.get(table, []):
            if definition["version"] == version:
                return [
                    Field(
                        name=f["name"],
                        field_type=f["field_type"] if isinstance(f["field_type"], str) else next(iter(f["field_type"])),
                        is_key=bool(f["is_key"]),
                        default="" if f.get("default_value") is None else str(f["default_value"]),
                    )
                    for f in definition["fields"]
                ]
        raise KeyError(f"No schema definition for {table} v{version}")

    def key_columns(self, table: str, version: int) -> list[str]:
        return [f.name for f in self.fields(table, version) if f.is_key]
