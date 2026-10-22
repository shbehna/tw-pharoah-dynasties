# Dynasties Rebalance

A Total War: PHARAOH DYNASTIES mod that rebalances administrative burden, outposts, movement,
landmarks, buildings and garrisons, and gives the AI bonuses that grow during the campaign. What it changes is in [CHANGELOG.md](CHANGELOG.md); the
generator also writes a row-by-row list to `docs/CHANGES.md`.

The mod is installed as a local pack in the game's `data` folder. Nothing is uploaded to the Workshop.

## Install

You need Windows, Python 3.10 or later and an internet connection for the first step.
Run the scripts from a PowerShell window in this folder:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1     # downloads RPFM and the table schema into tools\
powershell -ExecutionPolicy Bypass -File scripts\extract.ps1   # extracts the game data into reference\
python generator\generate.py                                   # writes the mod source into src\
powershell -ExecutionPolicy Bypass -File scripts\install.ps1   # builds dist\dynasties_rebalance.pack and copies it to the game
```

Then, in the game launcher:

1. Enable **dynasties_rebalance**.
2. Check for enabled mods that change the same things (see [Other mods](#other-mods)).
3. Start a new campaign. The new administration tier thresholds also apply to existing saves, but the
   game stores each settlement's administration cost in the save and only updates it when a building
   there changes.

To remove the mod: `scripts\install.ps1 -Uninstall`.
The scripts find the game through Steam; if that fails, pass its folder: `scripts\install.ps1 -GamePath "D:\...\Total War PHARAOH DYNASTIES"`.

## Change a value

Every number is in [generator/settings/](generator/settings), one module per section of the changelog
(`admin.py`, `landmarks.py`, `experience.py`, ...). The rebuilt landmarks (new building levels, their names
and help pages) are TSV files in [generator/data/](generator/data). After editing either:

```powershell
python generator\generate.py                                   # rewrites src\ and docs\CHANGES.md
powershell -ExecutionPolicy Bypass -File scripts\install.ps1
powershell -ExecutionPolicy Bypass -File scripts\check.ps1     # optional: RPFM diagnostics (invalid references...)
```

After a game patch, run `scripts\extract.ps1` first. Update [CHANGELOG.md](CHANGELOG.md) when you change a value.

## Design notes

| Topic | What the mod does |
| --- | --- |
| Administration tier thresholds | A small script changes the thresholds in the game's `supply_points.lua` when the campaign loads, instead of replacing that file, so the game's later fixes to it are kept. The tier titles show the new ranges. |
| Province capitals | They cost 1 administration point more than other major settlements in vanilla and keep that +1 (`KEEP_PROVINCE_CAPITAL_EXTRA_ADMIN`). |
| Lookout posts | Two effects, one for the region and one for the province; in the lookout post's own region they add up. |
| Own army movement | Forts, Warriors' Refuges, Monuments, Lookout posts and Waystations use the campaign movement effect of roads (`phar_main_mod_land_movement_campaign_basic`), so they add up with each other and with roads. |
| Monuments | The five regular Monuments. The unique wonders (pyramids, ziggurats, ...) share the monument interaction but are left out. |
| Naval full speed | Sea movement is reduced for everyone and the Full Speed stance bonus is scaled down by the same proportion (`NAVAL_FULL_SPEED_BONUS_SCALE`), so full speed is as much slower as regular movement. |
| Granary, bronzeworker, goldsmith | The "%" is the main production effect; the extra +5% these buildings give at high influence is unchanged. Tausret's own versions of these chains are separate buildings and fall under the doubling rule (only her food chain is doubled). |
| Beer Hall | The same building is the Wine Hall or Performance Hall for other cultures; all of them get the food bonus. |
| Doubling other production % | Only bonuses (positive values) that apply to food alone (`OTHER_PRODUCTION_RESOURCES`); bonuses to several resources (e.g. +% to all resources) or to other resources keep their vanilla value. Landmarks get every production bonus doubled (`OTHER_PRODUCTION_ALL_RESOURCES`). Add patterns to `OTHER_PRODUCTION_EXCLUDE` to leave some buildings out. |
| Garrisons | Settlement main buildings keep their vanilla garrison (`SETTLEMENT_GARRISON_MULTIPLIER`); lookout posts have their own multiplier (`LOOKOUT_GARRISON_MULTIPLIER`); every other building's garrison units are multiplied (`GARRISON_MULTIPLIER`), landmark garrisons included. The garrison commander is never multiplied. |
| Rebuilt landmarks | Four landmarks are replaced by new building levels (`<landmark>_2`); burden reductions defined for the old level move to the new one. |
| Progressive difficulty | A script gives each AI faction (not players, not rebels) the effect bundle of the current tier: at the start of each player turn for every faction, and at the start of its own turn for a faction that appears later. Major factions are the ones the game flags as major (`faction:is_major()`). Turns and values: `PROGRESSIVE_DIFFICULTY_*`; a tier whose values are all 0 (tier 0, from turn 0) has no effect bundle. |
| Progressive difficulty log | Every bundle given or removed, one summary line per turn and the list of factions at each load go to `dynasties_rebalance.log` in the game folder (`PROGRESSIVE_DIFFICULTY_LOG_FILE`) and to the game's script log. |
| Campaign AI targets | Only where AI armies go: the distance penalty of army tasks (`cai_task_management_system_variable_group_junctions_tables`, `AI_DISTANCE_*`) and the priority of army tasks for the task generator groups of the game's AI personalities (`cai_task_management_system_task_generator_groups_generators_junctions_tables`, `AI_TASK_PRIORITY_*`). War declarations, aggressiveness and diplomacy are not changed. Tasks aimed at the human player keep their vanilla priority. |
| Unique characters | A script (`dyn_rebal_unique_characters.lua`) listens to `FactionDestroysOtherFaction` and `FactionDestroyed` and moves the unique characters of a destroyed AI faction to a human player (`cm:reassign_character_to_faction`). Unique: immortal, or subtype key containing `UNIQUE_CHARACTER_KEY_PARTS`, so characters of other mods are moved too. Unique generals of a human player that have never led an army for that player get one (`cm:create_force_with_existing_general` with `UNIQUE_CHARACTER_PLACEHOLDER_UNIT`, which is then removed). That is remembered per faction and character subtype, not per character: a disbanded unique general comes back as a new character (new cqi), which would otherwise get an army again. The game's own unique characters are permitted in every faction, with their bodyguards allowed everywhere; characters added by other mods rely on those mods for that. |

Units and buildings left over from Total War: TROY (`troy_` keys, not used in Pharaoh) are not changed.

## Other mods

`docs/CONFLICTS.md` compares this mod with the mods currently enabled in the launcher: mods that are
redundant with it (everything they change is also changed here), mods that change some of the same rows
and which one wins, and mods that replace game scripts. Refresh it after changing the mod list:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\extract.ps1 -ActiveMods
python generator\conflicts.py
```

### Compatibility add-ons

Some mods get an add-on pack: mods that add unique characters (to let those characters serve in any faction,
as the main mod does for the game's own: permitted subtypes, bodyguard units allowed everywhere, bodyguards for
every culture), and mods whose buildings this mod rebalances. An add-on's rows refer to the other mod's
characters, units or buildings, so **enable an add-on only together with its mod**. Each add-on has a builder in
`generator/addons.py`.

| Add-on pack | For |
| --- | --- |
| `dynasties_rebalance_compat_make_character_unique.pack` | Make Character Unique (Workshop 3320741050), also its "Slot" variant (same characters) |
| `dynasties_rebalance_compat_cptt_recruitment_rework.pack` | CPTT Recruitment Rework (Workshop 3441336326): rebalanced Relocation Office and Deportation Hub (`CPTT_BUILDING_EFFECTS`) |

The add-ons are listed in `mod.json` (`compat_addons`). To add one for another mod, add an entry with its
Workshop ID, subscribe to it, then run `scripts\extract.ps1` (it extracts the mod's tables to
`referenceddons\`), `python generator\generate.py` (writes `src_addons\`) and `scripts\install.ps1`
(builds and installs every pack).

### Separate mods

Optional packs that do not depend on the main mod: enable each one or not, with or without
`dynasties_rebalance.pack`. They are listed in `mod.json` (`separate_mods`), generated to `src_mods\` and
built and installed with the main mod.

| Pack | What it does |
| --- | --- |
| `dynasties_start_confederations.pack` | When a new campaign starts, a faction played by a human confederates the AI factions that own some regions (`START_CONFEDERATIONS`): Hanigalbat gets the owner of Sangaritu. |

Start confederations: the script (`dynasties_start_confederations.lua`) runs on the first tick of a new
campaign only (`cm:add_first_tick_callback_new`, plus a saved flag). For each faction in
`START_CONFEDERATIONS` played by a human, it looks up the owner of each listed region and confederates it
(`cm:force_confederation`) unless it is a player or rebels. The owner is read in game, not from the start
position, so the setting names regions rather than factions.

## How it is built

- `generator/` reads the extracted game tables (`reference/vanilla`) and its own data files
  (`generator/data`) and settings (`generator/settings/`), and writes the mod source to `src/`: one TSV file per table and section, the
  texts, and four Lua scripts (administration tiers, outpost sacking, progressive difficulty, unique characters). It only writes rows that differ
  from the game.
- `scripts/build.ps1` packs `src/` with RPFM (Rusted PackFile Manager) 4.7.4, the last version with a
  command line tool, converting the TSV files to the game's binary tables.
- Every table and text file inside the pack starts with `!!!!!!!!!!!!!!!!_dynasties_rebalance_`. When two
  mods define the same row, the game keeps the one from the file whose name sorts first, so this mod wins
  over vanilla and over almost every other mod.

| Path | Contents |
| --- | --- |
| `CHANGELOG.md` | What the mod changes |
| `generator/settings/` | All the numbers, one module per section |
| `generator/data/` | Rebuilt landmarks: new building levels, names, help pages, fixes |
| `generator/features/` | One module per section |
| `generator/conflicts.py` | Comparison with the enabled mods |
| `scripts/` | `setup`, `extract`, `build`, `install`, `check` |
| `src/` | Generated mod source, packed as-is (not versioned) |
| `generator/addons.py`, `src_addons/` | Compatibility add-ons and their generated source (not versioned) |
| `generator/separate_mods.py`, `src_mods/` | Separate mods and their generated source (not versioned) |
| `docs/CHANGES.md`, `docs/CONFLICTS.md` | Generated reports (not versioned) |
| `tools/`, `reference/`, `dist/` | Downloaded or extracted (not versioned) |
