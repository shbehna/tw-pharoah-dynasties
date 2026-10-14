"""Rows that let unique characters serve in any faction (main mod and compatibility add-ons).

Works on plain rows (dicts) so it can combine the game's tables with another mod's.
"""

from __future__ import annotations

from dataclasses import dataclass, field

LEGACY_PREFIX = "troy_"
PERMITTED = "faction_agent_permitted_subtypes_tables"
UNIT_PERMISSIONS = "units_to_groupings_military_permissions_tables"
BODYGUARDS = "equipped_ancillaries_to_commanded_unit_junctions_tables"
# Key columns of the bodyguard table (every column but the unit and the art set).
BODYGUARD_KEY = ("agent_subtypes", "campaign", "culture", "equipped_armor_type", "equipped_mount_type",
                 "equipped_shield_type", "equipped_weapon_type", "factions", "subculture",
                 "equipped_bodyguard_skin_type", "equipped_character_skin_type")


@dataclass
class AnyFactionRows:
    permitted: list[dict] = field(default_factory=list)
    unit_permissions: list[dict] = field(default_factory=list)
    bodyguards: list[dict] = field(default_factory=list)
    units: set[str] = field(default_factory=set)
    factions: int = 0
    groups: int = 0


def unique_subtypes(agent_subtypes: list[dict], key_parts: list[str]) -> list[str]:
    return sorted(row["key"] for row in agent_subtypes
                  if not row["key"].startswith(LEGACY_PREFIX) and any(part in row["key"] for part in key_parts))


def any_faction_rows(subtypes: list[str], factions: list[dict], agent_subtypes: list[dict],
                     permitted: list[dict], unit_permissions: list[dict], bodyguards: list[dict]) -> AnyFactionRows:
    """Rows to add so that `subtypes` can serve in every faction of `factions` (existing rows are skipped).

    - the subtype is permitted as a general in every faction
    - every bodyguard unit of the subtype is allowed for every unit group
    - bodyguards defined for one subculture only also apply to every other subculture
    """
    out = AnyFactionRows()
    # By key: a later row (another mod's) replaces an earlier one (the game's).
    factions = list({row["key"]: row for row in factions if not row["key"].startswith(LEGACY_PREFIX)}.values())
    groups = sorted({row["military_group"] for row in factions if row["military_group"]})
    out.factions, out.groups = len(factions), len(groups)
    subtype_set = set(subtypes)

    existing = {(row["agent"], row["faction"], row["subtype"]) for row in permitted}
    for subtype in subtypes:
        for faction in factions:
            if ("general", faction["key"], subtype) not in existing:
                out.permitted.append({"agent": "general", "faction": faction["key"], "subtype": subtype, "campaign": ""})

    own = [row for row in bodyguards if row["agent_subtypes"] in subtype_set]
    out.units = {row["commanded_unit"] for row in own if row["commanded_unit"]}
    out.units |= {row["associated_unit_override"] for row in agent_subtypes
                  if row["key"] in subtype_set and row.get("associated_unit_override")}
    allowed = {(row["unit"], row["military_group"]) for row in unit_permissions}
    for unit in sorted(out.units):
        for group in groups:
            if (unit, group) not in allowed:
                out.unit_permissions.append({"unit": unit, "military_group": group,
                                             "can_be_used_by_fort_colonel": "false"})

    keys = {tuple(row[c] for c in BODYGUARD_KEY) for row in own}
    for row in own:
        if not row["subculture"]:
            continue
        copy = dict(row, subculture="")
        key = tuple(copy[c] for c in BODYGUARD_KEY)
        if key not in keys:
            keys.add(key)
            out.bodyguards.append(copy)
    return out
