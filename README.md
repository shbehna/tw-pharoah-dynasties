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

Every number is in [generator/settings.py](generator/settings.py). Hand-made rows (landmarks, the
administrative buildings that reduce the burden, religious conversion costs, garrison ammunition)
are TSV files in [generator/data/](generator/data). After editing either:

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
| Monuments | The five regular Monuments. The unique wonders (pyramids, ziggurats, ...) share the monument interaction but are left out. |
| Naval full speed | Sea movement is reduced for everyone and the Full Speed stance bonus is scaled down by the same proportion (`NAVAL_FULL_SPEED_BONUS_SCALE`), so full speed is as much slower as regular movement. |
| Granary, bronzeworker, goldsmith | The "%" is the main production effect; the extra +5% these buildings give at high influence is unchanged. Tausret's own versions of these chains are separate buildings and fall under the doubling rule (only her food chain is doubled). |
| Beer Hall | The same building is the Wine Hall or Performance Hall for other cultures; all of them get the food bonus. |
| Doubling other production % | Only bonuses (positive values) that apply to food alone (`OTHER_PRODUCTION_RESOURCES`); bonuses to several resources (e.g. +% to all resources) or to other resources keep their vanilla value. Landmarks get every production bonus doubled (`OTHER_PRODUCTION_ALL_RESOURCES`). Add patterns to `OTHER_PRODUCTION_EXCLUDE` to leave some buildings out. |
| Garrisons | Settlement main buildings keep their vanilla garrison (`SETTLEMENT_GARRISON_MULTIPLIER`); lookout posts have their own multiplier (`LOOKOUT_GARRISON_MULTIPLIER`); every other building's garrison units are multiplied (`GARRISON_MULTIPLIER`), landmark garrisons included. The garrison commander is never multiplied. |
| Rebuilt landmarks | Four landmarks are replaced by new building levels (`<landmark>_2`); burden reductions defined for the old level move to the new one. |
| Progressive difficulty | A script gives each AI faction (not players, not rebels) the effect bundle of the current tier: at the start of each player turn for every faction, and at the start of its own turn for a faction that appears later. Major factions are the ones the game flags as major (`faction:is_major()`). Turns and values: `PROGRESSIVE_DIFFICULTY_*`. |
| Progressive difficulty log | Every bundle given or removed, one summary line per turn and the list of factions at each load go to `dynasties_rebalance.log` in the game folder (`PROGRESSIVE_DIFFICULTY_LOG_FILE`) and to the game's script log. |

Units and buildings left over from Total War: TROY (`troy_` keys, not used in Pharaoh) are not changed.

## Other mods

`docs/CONFLICTS.md` compares this mod with the mods currently enabled in the launcher: mods that are
redundant with it (everything they change is also changed here), mods that change some of the same rows
and which one wins, and mods that replace game scripts. Refresh it after changing the mod list:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\extract.ps1 -ActiveMods
python generator\conflicts.py
```

## How it is built

- `generator/` reads the extracted game tables (`reference/vanilla`) and its own data files
  (`generator/data`), and writes the mod source to `src/`: one TSV file per table and section, the
  texts, and three Lua scripts (administration tiers, outpost sacking, progressive difficulty). It only writes rows that differ
  from the game.
- `scripts/build.ps1` packs `src/` with RPFM (Rusted PackFile Manager) 4.7.4, the last version with a
  command line tool, converting the TSV files to the game's binary tables.
- Every table and text file inside the pack starts with `!!!!!!!!!!!!!!!!_dynasties_rebalance_`. When two
  mods define the same row, the game keeps the one from the file whose name sorts first, so this mod wins
  over vanilla and over almost every other mod.

| Path | Contents |
| --- | --- |
| `CHANGELOG.md` | What the mod changes |
| `generator/settings.py` | All the numbers |
| `generator/data/` | Hand-made rows (landmarks, burden reductions, conversion costs, garrison ammunition) |
| `generator/features/` | One module per section |
| `generator/conflicts.py` | Comparison with the enabled mods |
| `scripts/` | `setup`, `extract`, `build`, `install`, `check` |
| `src/` | Generated mod source, packed as-is (not versioned) |
| `docs/CHANGES.md`, `docs/CONFLICTS.md` | Generated reports (not versioned) |
| `tools/`, `reference/`, `dist/` | Downloaded or extracted (not versioned) |
