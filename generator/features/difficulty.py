"""Progressive difficulty.

- one effect bundle per tier and faction kind (major or other), with the AI bonuses; a tier
  without bonuses (e.g. tier 0 from turn 0) has no bundle
- a campaign script that gives AI factions the bundle of the current tier and logs what it does
"""

from __future__ import annotations

from features import admin
from lib.data import Overlay

FEATURE = "difficulty"

BUNDLES = "effect_bundles_tables"
EBEJ = "effect_bundles_to_effects_junctions_tables"
SCRIPT_PATH = "script/campaign/mod/dyn_rebal_progressive_difficulty.lua"
BUNDLE_PREFIX = "dyn_rebal_progressive_difficulty"
ICON = "fx_icon_army.png"
KINDS = {"major": "major factions", "other": "other factions"}
TIER_NAMES = ["0", "I", "II", "III", "IV", "V"]  # tier 0 is the first one in the settings

# Setting name -> (effects, scope, text for the report and the bundle description).
# The effects and scopes are the ones vanilla uses for the same faction-wide bonuses; building
# upkeep uses the mod's own effects (see admin.building_upkeep_effects), one per resource.
EFFECTS = {
    "army_upkeep": (["troy_effect_army_campaign_upkeep"], "faction_to_force_own_factionwide",
                    "{:+g}% upkeep cost of all units"),
    "recruitment_cost": (["phar_main_military_recruitment_cost_mod_all_units"], "faction_to_force_own_factionwide",
                         "{:+g}% recruitment cost of all units"),
    "income": (["troy_effect_economy_mod_all_resources"], "faction_to_region_own",
               "{:+g}% to all resources produced"),
    "recruitment_slots": (["troy_effect_faction_unit_recruitment_points"], "faction_to_province_own",
                          "{:+g} local recruitment capacity"),
    "construction_cost": (["phar_main_building_construction_cost_percentage_multiplier_mod_all"],
                          "faction_to_region_own", "{:+g}% construction cost of all buildings"),
    "building_upkeep": ([], "faction_to_region_own", "{:+g}% upkeep of all buildings"),
    "happiness": (["troy_effect_faction_happiness_in_all_own_territories"], "faction_to_province_own",
                  "{:+g} happiness in every province"),
}


def apply(overlay: Overlay, settings) -> None:
    s = settings
    turns = s.PROGRESSIVE_DIFFICULTY_TURNS
    if turns != sorted(turns) or len(set(turns)) != len(turns) or len(turns) > len(TIER_NAMES):
        raise ValueError(f"PROGRESSIVE_DIFFICULTY_TURNS must be increasing (at most {len(TIER_NAMES)} tiers)")
    values = {"major": s.PROGRESSIVE_DIFFICULTY_MAJOR, "other": s.PROGRESSIVE_DIFFICULTY_OTHER}
    for kind, table in values.items():
        unknown = set(table) - set(EFFECTS)
        if unknown:
            raise ValueError(f"Unknown progressive difficulty bonuses for {kind}: {sorted(unknown)}")
        for name, tier_values in table.items():
            if len(tier_values) != len(turns):
                raise ValueError(f"{name} ({kind}) needs one value per turn in PROGRESSIVE_DIFFICULTY_TURNS")

    effects = dict(EFFECTS)
    _, scope, _ = EFFECTS["building_upkeep"]
    resources = s.PROGRESSIVE_DIFFICULTY_BUILDING_UPKEEP_RESOURCES
    effects["building_upkeep"] = (admin.building_upkeep_effects(overlay, resources), scope,
                                  f"{{:+g}}% {'/'.join(resources)} upkeep of all buildings")

    tiers = []
    for tier, turn in enumerate(turns):
        bundles = {}
        for kind, table in values.items():
            if all(tier_values[tier] == 0 for tier_values in table.values()):
                overlay.note(FEATURE, f"Tier {TIER_NAMES[tier]} from turn {turn}, AI {KINDS[kind]}: no bonuses.")
                continue
            bundle = f"{BUNDLE_PREFIX}_{kind}_{tier}"
            bundles[kind] = bundle
            descriptions = _bundle(overlay, bundle, kind, tier, turn, table, effects)
            overlay.note(FEATURE, f"Tier {TIER_NAMES[tier]} from turn {turn}, AI {KINDS[kind]} ({bundle}): "
                                  f"{', '.join(descriptions)}.")
        tiers.append((turn, bundles))
    overlay.put_script(SCRIPT_PATH, _script(tiers, s.PROGRESSIVE_DIFFICULTY_LOG_FILE), FEATURE)
    log = (f"the game script log and {s.PROGRESSIVE_DIFFICULTY_LOG_FILE} in the game folder"
           if s.PROGRESSIVE_DIFFICULTY_LOG_FILE else "the game script log")
    overlay.note(FEATURE, f"The script {SCRIPT_PATH} applies the bundles to AI factions (players and rebels "
                          f"excluded) and logs every change to {log}.")


def _bundle(overlay: Overlay, bundle: str, kind: str, tier: int, turn: int, table: dict, effects: dict) -> list[str]:
    descriptions = []
    for name, tier_values in table.items():
        value = tier_values[tier]
        if value == 0:
            continue
        keys, scope, text = effects[name]
        for effect in keys:
            overlay.put(EBEJ, {
                "effect_bundle_key": bundle,
                "effect_key": effect,
                "effect_scope": scope,
                "value": value,
                "advancement_stage": "start_turn_completed",
            }, FEATURE)
        descriptions.append(text.format(value))

    title = f"Progressive Difficulty {TIER_NAMES[tier]}"
    start = "from the start of the campaign" if turn <= 1 else f"from turn {turn}"
    description = (f"AI bonus for {KINDS[kind]} {start} (Dynasties Rebalance). "
                   f"Players never get it.")
    overlay.put(BUNDLES, {
        "key": bundle,
        "localised_description": description,
        "localised_title": title,
        "ui_icon": ICON,
        "bundle_target": "faction",
        "priority": 1,
    }, FEATURE)
    overlay.put_loc(f"effect_bundles_localised_title_{bundle}", title, FEATURE)
    overlay.put_loc(f"effect_bundles_localised_description_{bundle}", description, FEATURE)
    return descriptions


def _lua_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _script(tiers: list[tuple[int, dict[str, str]]], log_file: str | None) -> str:
    # A kind of faction without bonuses in a tier has no bundle: its field is left out (nil in Lua).
    tier_lines = "\n".join(
        "\t{ " + ", ".join([f"turn = {turn}"] + [f"{kind} = {_lua_string(bundles[kind])}"
                                                 for kind in KINDS if kind in bundles]) + " },"
        for turn, bundles in tiers
    )
    bundle_lines = "\n".join(f"\t{_lua_string(bundle)}," for _, bundles in tiers for bundle in bundles.values())
    log_file_value = _lua_string(log_file) if log_file else "nil"
    return f"""-- Dynasties Rebalance: progressive difficulty.
-- AI factions (not players, not rebels) get the effect bundle of the current tier: major factions
-- the "major" one, every other AI faction the "other" one. A new tier replaces the previous one.
-- A tier without a bundle for a kind of faction gives it no bonuses.
-- Generated by generator/features/difficulty.py - edit generator/settings.py instead.

local TIERS = {{
{tier_lines}
}}
-- Every bundle of every tier.
local BUNDLES = {{
{bundle_lines}
}}
-- Every change is logged to the game's script log (when script logging is enabled) and to this
-- file in the game folder (nil: script log only).
local LOG_FILE = {log_file_value}

local function log(message)
\tout("[Dynasties Rebalance] progressive difficulty: " .. message)
\tif not LOG_FILE then
\t\treturn
\tend
\tlocal file = io.open(LOG_FILE, "a")
\tif file then
\t\tfile:write(os.date("%Y-%m-%d %H:%M:%S") .. "  progressive difficulty: " .. message .. "\\n")
\t\tfile:close()
\tend
end

local function faction_label(faction)
\tlocal key = faction:name()
\tlocal ok, screen_name = pcall(function()
\t\treturn common.get_localised_string("factions_screen_name_" .. key)
\tend)
\tif ok and type(screen_name) == "string" and screen_name ~= "" then
\t\treturn screen_name .. " (" .. key .. ")"
\tend
\treturn key
end

local function current_tier(turn)
\tlocal current = nil
\tfor _, tier in ipairs(TIERS) do
\t\tif turn >= tier.turn then
\t\t\tcurrent = tier
\t\tend
\tend
\treturn current
end

local function wanted_bundle(faction, turn)
\tif faction:is_human() or faction:is_rebel() then
\t\treturn nil
\tend
\tlocal tier = current_tier(turn)
\tif not tier then
\t\treturn nil
\tend
\tif faction:is_major() then
\t\treturn tier.major
\tend
\treturn tier.other
end

-- Gives the faction the bundle it should have this turn and removes the others.
local function update_faction(faction, turn)
\tlocal faction_key = faction:name()
\tlocal wanted = wanted_bundle(faction, turn)
\tfor _, bundle in ipairs(BUNDLES) do
\t\tif bundle ~= wanted and faction:has_effect_bundle(bundle) then
\t\t\tcm:remove_effect_bundle(bundle, faction_key)
\t\t\tlog("turn " .. turn .. ": removed " .. bundle .. " from " .. faction_label(faction))
\t\tend
\tend
\tif wanted and not faction:has_effect_bundle(wanted) then
\t\tcm:apply_effect_bundle(wanted, faction_key, 0)
\t\tlog("turn " .. turn .. ": applied " .. wanted .. " to " .. faction_label(faction))
\tend
end

-- Factions that have each bundle; with `with_names`, also lists them.
local function log_summary(turn, with_names)
\tlocal tier = current_tier(turn)
\tif not tier then
\t\tlog("turn " .. turn .. ": no bonuses before turn " .. TIERS[1].turn)
\t\treturn
\tend
\tlocal tier_bundles = {{}}
\tif tier.major then
\t\ttable.insert(tier_bundles, tier.major)
\tend
\tif tier.other then
\t\ttable.insert(tier_bundles, tier.other)
\tend
\tif #tier_bundles == 0 then
\t\tlog("turn " .. turn .. ": no bonuses in the current tier")
\t\treturn
\tend
\tlocal holders = {{}}
\tfor _, bundle in ipairs(tier_bundles) do
\t\tholders[bundle] = {{}}
\tend
\tlocal faction_list = cm:model():world():faction_list()
\tfor i = 0, faction_list:num_items() - 1 do
\t\tlocal faction = faction_list:item_at(i)
\t\tif not faction:is_dead() then
\t\t\tfor bundle, names in pairs(holders) do
\t\t\t\tif faction:has_effect_bundle(bundle) then
\t\t\t\t\ttable.insert(names, faction_label(faction))
\t\t\t\tend
\t\t\tend
\t\tend
\tend
\tfor _, bundle in ipairs(tier_bundles) do
\t\tlocal names = holders[bundle]
\t\tlocal line = "turn " .. turn .. ": " .. #names .. " AI factions have " .. bundle
\t\tif with_names and #names > 0 then
\t\t\ttable.sort(names)
\t\t\tline = line .. ": " .. table.concat(names, ", ")
\t\tend
\t\tlog(line)
\tend
end

-- Gives every living faction the bundle it should have this turn.
local function update_all_factions(turn)
	local faction_list = cm:model():world():faction_list()
	for i = 0, faction_list:num_items() - 1 do
		local faction = faction_list:item_at(i)
		if not faction:is_dead() then
			update_faction(faction, turn)
		end
	end
end

log("script loaded")

-- The players' turn comes first in each round: update every faction then, so a new tier applies to
-- all AI factions at once and the summary is up to date. Factions that appear later in the round
-- get their bundle at the start of their own turn.
core:add_listener(
	"dyn_rebal_progressive_difficulty_faction_turn_start",
	"FactionTurnStart",
	true,
	function(context)
		local faction = context:faction()
		local turn = cm:turn_number()
		if faction:is_human() then
			update_all_factions(turn)
			-- One summary line per turn shows in the log that the script is running.
			log_summary(turn, false)
		else
			update_faction(faction, turn)
		end
	end,
	true
)

-- Run by the game's mod loader on the first tick (function named after the file): brings every
-- faction up to date, e.g. in a save made before the mod was installed, and lists the factions.
function dyn_rebal_progressive_difficulty()
	local turn = cm:turn_number()
	log("campaign loaded at turn " .. turn)
	update_all_factions(turn)
	log_summary(turn, true)
end
"""
