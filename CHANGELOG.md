# Changelog

## 1.0.0 — 2026-10-04

Values are the ones you see in game; "vanilla" is the unmodded game.

### Administrative burden

- Administration tiers start at 0, 150, 250, 400, 600, 750, 950, 1150, 1350, 1600, 1900 and 2250 points
  (vanilla 0, 55, 110, 160, 215, 270, 330, 390, 455, 520, 590 and 660). The tier titles show the new ranges.
- Each administration tier adds to building construction costs: +0% at tier 1, then +10% per tier, up to +110% at tier 12.
- Administration tiers change the gold and stone upkeep of buildings: -50% at tier 1, -25% at tier 2, none at tier 3,
  then +10% at tier 4 and +10% more per tier, up to +90% at tier 12.
- Bronze and gold upkeep of every administration tier are the same as its food upkeep (for example +140% bronze and
  gold at tier 12; vanilla +120% bronze, no gold).
- Administration tiers that raise the recruitment cost of one resource (food for Egypt, bronze for the Hittites, gold
  for Mesopotamia) raise the other two by the same amount (for example +140% food, bronze and gold at tier 12).
- Recruitment cost of the administration tiers is the same for every culture: +10%, +20%, +30%, +40%, +50%, +60%,
  +80%, +100%, +120% and +140% from tier 3 to tier 12. Aegea (native units), Canaan and the Sea Peoples (horde units)
  had half of that in vanilla (+5% to +80%).
- Main buildings of major settlements cost 3, 6, 10, 16 and 24 administration points by level (vanilla 2, 3, 4, 5, 6).
  Province capitals keep their vanilla extra point: 4, 7, 11, 17 and 25.
- Main buildings of minor settlements cost 3, 6 and 12 administration points by level (vanilla 2, 3, 4).
- Administrative buildings reduce the administration burden (full value at high influence, less at lower influence):
  - Newscrier's Stand, Public Square, Hall of Messengers: -4, -8, -12 (the second Newscrier's Stand chain: -2, -5)
  - Hall of Records, Palace of Correspondence, Wisdom Codices: -4, -8, -12 (Seti's Office of Relations and Royal Palace: -4, -8)
  - Tax Collector's Office, Tax Administration Centre, Royal Tax Administration: -1, -3, -5 (Seti's versions: -1, -3)
  - Recruitment Hall, War Council, War Coffers: -3, -6, -10 (also Seti's Military Office chain and Mustering Office, and Ashur's War Stockpiles chain)
  - Traveller's Inn, Caravanserai, Visitor's Quarters: -1, -2, -5 (also the Mycenaean road chain)
  - Babylon's City Trade Records, Merchants' Guild, Royal Scribal Archives: -4, -8, -12; Royal Garrison: -1
  - Translators' Quarters: -3
  - Faction buildings: Amenmesse's Foreign Visitors' Entertainments chain -1, -3, -5; Bay's Chief Scribe's Headquarters -3 and Trading Fairground chain -1, -3;
    Ramesses' Medjay chain -1, -3, -5; Suppiluliuma's Militia Gathering Post and Army Supply Centre -2, -4;
    Peleset Oxen chain -1, -3, -5; Sea Peoples' Highborn Gathering and Tribal Convocation -4, -10
  - Landmarks: Royal Legal Complex, Royal War Academy, The Great Archives, Professional Scribal Complex,
    Royal Tax Collector's Office and Palace Archive: -5 each

### Outposts

- Trading posts: +15% to all resources produced in the region (vanilla +10%).
- Forts hold up to 20 units (vanilla 10) and reduce the upkeep of units stationed in them by 90% (vanilla 50%).
- Warriors' Refuges hold up to 15 units (vanilla 6) and reduce the upkeep of units stationed in them by 30% (vanilla none).
- Monuments: +3 happiness in the province.
- Lookout posts: -10% campaign movement for enemy armies in the region and -2.5% in the province (-12.5% in the lookout post's own region).
- Campaign movement of your own armies: Forts and Warriors' Refuges +15% in the region, Lookout posts +5% in the region,
  Monuments +5% and Waystations +10% in the province (vanilla none). The bonuses of several outposts add up.

### Movement

- Campaign movement -30% on land and -50% at sea, for every faction (player and AI) on every difficulty.
- The naval Full Speed stance gives +25% movement (vanilla +50%), so full speed is also 50% slower: 75% of vanilla base speed (vanilla 150%).
- Entering forced march requires at least 25% movement left.
- After razing an outpost an army keeps 10% of its movement; after sacking one, 20%.

### Landmarks

- Rebalanced effects:
  - Citadel of Troy: +5 diplomatic relations with all factions (vanilla +3)
  - Cyclopean Walls: -25% attrition when under siege
  - Deep Groundwater Supply: +6 workforce growth (vanilla +12), +2 turns of siege holdout
  - Fortress of Ithaca: line of sight 80 (vanilla 70)
  - High Citadel of Parha: +40% to all resources produced in the province, +5 diplomatic relations, +4 happiness, +4 workforce growth, +3 workforce from occupied slots, +5 morale on recruitment, +1 victory point
  - Hilltop Holdfast: +1 turn of siege holdout
  - House of Ea-nasir: +10% bronze income in your provinces, +20 gold per turn, -5 happiness, -5 diplomatic relations (vanilla +3)
  - House of Exorcists: +4 happiness, +4 influence, +5 morale and +5 melee attack on recruitment, +3 workforce from occupied slots, +1 victory point
  - Decorated Pottery Workshop: +30 gold per turn, +4 happiness, +4 influence, +3 workforce from occupied slots, +1 victory point
  - Ice House: +2 happiness (vanilla +3), +4 workforce growth
  - Lion Hunting Grounds: +5 legitimacy
  - Lycian Stables: +2 recruit rank for chariots
  - Nilometer: +2 influence (vanilla +3), +6 workforce growth (vanilla +7), +5 legitimacy
  - Palace Archive: +6 hero recruit rank (vanilla +7), +2 happiness (vanilla +4), +2 influence, +5 legitimacy (vanilla +4)
  - Palace of Minos: +10% to all resources produced in your provinces, +2 happiness in your provinces
  - Pottery Markets: +4 happiness (vanilla +2), +2 happiness and +2 influence in adjacent provinces
  - Professional Scribal Complex: +6 influence (vanilla +7), +4 influence in adjacent provinces (vanilla +5), +5 legitimacy (vanilla +4)
  - Rock Art Site School: +2 legitimacy (vanilla +4), +6 happiness (vanilla +7), +3 happiness (vanilla +4) and +3 influence in adjacent provinces
  - Royal Asaminthos: -2% fatigue for bodyguard and high tier units
  - Royal Legal Complex: +2 happiness and +2 influence in your provinces, +5 legitimacy, +15 civilization points, +3 workforce from occupied slots, +1 victory point
  - Royal Tax Collector's Office: +5 legitimacy (vanilla +3)
  - Royal War Academy: +8 hero recruit rank (vanilla +7), +4 legitimacy (vanilla +3), +235 experience per turn for units (vanilla +70; see Experience)
  - Sanctified Cattle Herds: +2 happiness (vanilla +3), +2 influence
  - Shipment Redistribution Hub: +4 influence (vanilla +5), +2 influence in adjacent provinces
  - The Northern Oasis Fields: +250 food per turn (vanilla +215), +2 influence (vanilla +3), +6 workforce growth (vanilla +7), +4 happiness (vanilla +5)
  - The Sacred Way: +100 favour with all your gods (vanilla +30), +4 happiness, +4 influence
- Royal Legal Complex, High Citadel of Parha, Decorated Pottery Workshop and House of Exorcists are rebuilt as new buildings with the effects above.
- Landmark garrisons: Cyclopean Walls 8 Palace Guards, Citadel of Troy 8 Troy's Chosen, Fortress of Ithaca 8 Exemplary Ambushers,
  Lycian Stables 4 Lycian Winged Chariots, Hilltop Holdfast 4 Mad Mares of Thrace.
- Construction costs:

  | Landmark | Gold | Stone | Wood |
  | --- | --- | --- | --- |
  | Citadel of Troy | 200 | 1400 (was 1070) | 200 (was 125) |
  | Cyclopean Walls | 100 (was 200) | 1400 (was 1050) | 300 (was 350) |
  | Decorated Pottery Workshop | 300 | 1000 | 300 |
  | Deep Groundwater Supply | 100 (was 200) | 800 (was 730) | 250 (was 95) |
  | Fortress of Ithaca | 100 (was 200) | 1000 (was 1060) | 450 (was 420) |
  | Grand Copper Repository | 500 (was 200) | 500 (was 1050) | 500 (was 135) |
  | High Citadel of Parha | 250 | 1250 | 250 |
  | Hilltop Holdfast | 200 | 800 (was 1070) | 400 (was 140) |
  | House of Ea-nasir | 200 | 600 (was 1110) | 300 (was 120) |
  | House of Exorcists | 400 | 800 | 250 |
  | Ice House | 100 (was 200) | 1000 (was 1100) | 300 (was 140) |
  | Lion Hunting Grounds | 400 (was 200) | 200 (was 1110) | 400 (was 125) |
  | Lycian Stables | 300 (was 200) | 600 (was 1030) | 400 (was 185) |
  | Nilometer | 200 | 1000 (was 730) | 200 (was 175) |
  | Palace Archive | 300 (was 200) | 1000 (was 1040) | 200 (was 115) |
  | Palace of Minos | 450 (was 200) | 1000 (was 1080) | 150 (was 120) |
  | Pottery Markets | 250 (was 200) | 850 (was 1200) | 450 (was 150) |
  | Professional Scribal Complex | 250 (was 200) | 1000 (was 1120) | 250 (was 145) |
  | Rock Art Site School | 200 | 800 (was 910) | 100 (was 120) |
  | Royal Asaminthos | 250 (was 200) | 850 (was 1020) | 250 (was 150) |
  | Royal Legal Complex | 200 | 1200 | 200 |
  | Royal Tax Collector's Office | 400 (was 200) | 1000 (was 1050) | 200 (was 135) |
  | Royal War Academy | 400 (was 200) | 1000 (was 1040) | 200 (was 135) |
  | Sanctified Cattle Herds | 450 (was 200) | 200 (was 550) | 200 |
  | Shipment Redistribution Hub | 400 (was 200) | 400 (was 1000) | 400 (was 120) |
  | The Great Archives | 200 | 1400 (was 1300) | 300 (was 180) |
  | The Northern Oasis Fields | 300 (was 200) | 300 (was 650) | 300 (was 190) |
  | The Sacred Way | 200 | 1200 (was 1070) | 100 (was 140) |
  | The White Harbour | 200 | 800 (was 820) | 400 (was 150) |

- Fixes: the construction costs of Cyclopean Walls and Palace of Minos were swapped; several landmarks had the wrong icon or description.

### Buildings

- Converting a religious building no longer costs gold; it costs stone and wood instead:
  75 stone and 50 wood for a level 1 temple, 100 and 75 for level 2, 125 and 100 for level 3;
  75 stone and 35 wood for Mesopotamian dwellings; 125/100, 175/125 and 225/150 for Sea Peoples idols; 75 and 75 for shrines.
- Granary chain: +25%, +40%, +75% food production in the province (vanilla +5%, +10%, +20%); the Granary also gives -15% food upkeep for armies in the province.
- War Council chains, food upkeep of units in the province (vanilla none): Hanigalbat's War Stockpiles, War Treasury,
  War Council -5%, -10%, -15%; Recruitment Hall, War Council, War Coffers -2%, -5%, -10%.
- Officer chains, upkeep of generals' bodyguard units in the province (vanilla none): -30%, -50%, -85% (Hanigalbat's
  Officers' School, Royal Officers' School, Palace of War; Officer Training Grounds, Officer School, Royal Officer
  School; Ramesses' Military Office, Military School, Military Academy).
- Garrison chains, campaign movement of own armies in the region (vanilla none): Hanigalbat's City Guard Station,
  Inner Army Headquarters, Defenders' Fortress +5%, +10%, +15%; City Guard Station and City Guard Compound (and their
  regional equivalents) +3%, +6%.
- Main wood chains: 45 and 100 wood per turn (Logging Grounds and Logging Camp, vanilla 35 and 50; Woodcutting Yard and
  Woodcutting Complex, vanilla 30 and 40; Pine and Oak Timber Yard, vanilla 45 and 55; Irsu's versions included).
- Wood derivative chains build 1 turn faster: Cedar Warehouse, Woodcutters' District and Lumber Mill 1 turn (vanilla 2),
  Lumber Mill Complex 2 turns (vanilla 3).
- Compatibility add-on for CPTT Recruitment Rework (`dynasties_rebalance_compat_cptt_recruitment_rework.pack`; enable it
  only together with that mod): Relocation Office and Deportation Hub -10/-20 workforce growth in the province, +4/+8
  in adjacent provinces, +2/+5 influence, -3/-6 happiness and -5%/-10% upkeep of native units in the province (all
  resources: the game has no food-only upkeep effect for a set of units). Fixes the mod's two workforce growth rows,
  which share one key so only one of them applied.
- Bronzeworker chain: +10%, +20%, +35% bronze production (vanilla +5%, +10%, +20%); the Royal Bronzeworker also gives -10% bronze upkeep for armies in the province.
- Goldsmith chain: +10%, +15%, +25% gold production (vanilla +5%, +10%, +20%); the Royal Goldsmith also gives -5% gold upkeep for armies in the province.
- Summer Festival Grounds: +40% food production (vanilla +10%) and +2 happiness (vanilla +4).
- Beer Hall (Wine Hall and Performance Hall for other cultures): +20% food production.
- Kushite Delegate School (Amenmesse): +3 influence in the province (vanilla -3).
- Tax Collector's Office, Tax Administration Centre, Royal Tax Administration: +10%, +20%, +35% to all resources produced
  in the province (vanilla +5%, +10%, +20%).
- Hall of Records, Palace of Correspondence, Wisdom Codices: +2%, +5%, +8% royal decree completion rate
  ("administration efficiency for royal decrees"; vanilla none). Every building adds to it.
- Artisan's Workshop, Art School, Bazaar of the Arts: +3, +5, +8 happiness (vanilla +2, +4, +6).
- Midwife's House, Healing Hall, Surgeon's Practice: +5, +8, +12 workforce growth (vanilla +4, +6, +9).
- Mycenae's Kamaeu's Council, Damokoros' Residence, Lawagetas' Palace: +1, +2, +4 happiness (vanilla none, +1, +2);
  Lawagetas' Palace +8 influence (vanilla +7; +5 at low and medium influence, vanilla +4).
- Roads (Traveller's Inn, Caravanserai, Visitor's Quarters, and Mycenae's Road Administration Office chain): +2%, +5%, +10%
  to all resources produced in adjacent provinces (vanilla none).
- Olive Groves, Fruit Gardens, Grape Orchards, Apple Orchard, Bakery and Grand Bazaar: +4 workforce growth (vanilla +2).
  Fixes: Fruit Gardens no longer gives workforce growth when ruined; Grape Orchards gives it when damaged and at low and medium influence.
- Every building that gives your armies a campaign movement bonus gets +5% more: roads (all cultures, e.g. +10%, +15%, +25%,
  vanilla +5%, +10%, +20%; the extra bonus at high influence is unchanged), the Peleset movement chain and mounted buildings,
  Sea Peoples horde buildings (land and sea movement), Telmessos (+55%) and Ugarit (+30% at sea). Outposts are not included.
- Every other building's food production bonus is doubled, including fisheries and Tausret's food chain.
- Landmarks: every resource production bonus is doubled.
- Other resource production bonuses of buildings (main settlement buildings, temples, ports, wood buildings, ...) are unchanged. Production penalties are unchanged.
- Administration, Management and Religion buildings (main settlement buildings, temples, Grand Temples, ...) and landmarks
  have an upkeep each turn of 5% of their construction cost, for each resource of that cost, rounded up to a multiple of 5
  (vanilla: no upkeep). For example, a major settlement costs 5 stone and 5 wood per turn at level 1, 45 stone, 10 wood and
  10 gold at level 5; a Grand Temple 60 stone, 10 wood and 15 gold; the Royal Legal Complex (Hattusa) 60 stone, 10 wood and 10 gold.
  The Bay's happiness chain, which costs food to build, has a food upkeep (50 and 100).
  Buildings that already have an upkeep keep it and only get the other resources: the Victory Points landmark keeps its
  50 gold and adds 250 stone and 65 wood. Military Support, Recruitment, Resources and Production buildings, outposts,
  wonders, Sea Peoples horde buildings and ruins have no added upkeep.

### Buildings with garrisons

- Buildings with a garrison, other than the main buildings of settlements and lookout posts, provide 4 times as many garrison units
  (same unit types; the garrison commander is not multiplied). Lookout posts provide 2 times as many.
  Settlement main buildings keep their vanilla garrison.
- Garrison buildings give ammunition to your armies in their region: City Guard Station and City Guard Compound (and their equivalents) +10% and +15%;
  Guard Tower (and equivalents) +10%, plus +5% (+10% for some cultures) when defending a siege; Ashur's garrison chain +15%, +20%, +25%;
  Babylon's Royal Garrison and Royal Garrison Palace +10% and +15%.

### Experience

Half the values of the "XP Followers Traits And Buildings Buffed" mod (Workshop 3456700913), rounded to the
nearest 5; that mod should be disabled. Unit experience per turn, in the province unless noted (vanilla in brackets):

- Champion's Hall (all cultures): +170 (+40). Kuru's Mercenary Hunting Camp and Village: +105, +210 (+25, +50).
- Warriors' Refuge: +170 for own armies in its region (+40).
- City Guard Station and City Guard Compound (and their equivalents): +100 and +150 for own armies in the region
  (vanilla none); Guard Tower (and equivalents): +75 (vanilla none).
- Royal War Academy: +235 (+70).
- Shrine of Amun, Shrine of Kumarbi: +65, +125 for own armies in the region (+15, +30).
- Sea Peoples: Trapping Sites, Hunters' Tents, Hunting Bivouac +50, +125, +255 (+20, +50, +120); Peleset Single
  Combat Arena, Fighting Games, Fighting Tournaments +75, +100, +190 (+30, +40, +75); Dueling Field, Battle Arena
  +145, +235 (+35, +70); Peleset Great Assembly +125 for all armies (+50).
- Officer School, Royal Officer School: +25, +55 experience per turn for characters (+20, +50).
- Followers and titles, unit experience for the army: Veteran Soldier and Clay Tablet +90 (+10); Mitanni Horse Trainer,
  Kushite Guards, Duellist, Blind Veteran, Strongman, Wise Nobleman, Obsidian Tools & Blades +165 (+20); Ceremonial
  Sword of Adad-narari I +175 (+25); Theban Veteran +115 (+20), unique version +175 (+20); Royal Steward and Man of the
  People +90, upgraded +165 (+50, +100); Lionlike in Wrath +125 (+75); Overseer of Militia +90 (+20).
- Traits, unit experience per turn: Grieving (Achilles) +190 (+100); Mentor +35 (+10).
- Training chains (vanilla none): Hanigalbat's Practice Halls, Training Compound, Arena of Trials +30, +60, +120;
  Proving Grounds and Training Grounds, Kuru's Mercenary Office and Mercenary Centre +20, +50.
- Hanigalbat's own buildings get 20% more than the matching shared ones (rounded to the nearest 5): Champion's Hall
  +205 (+40); City Guard Station, Inner Army Headquarters, Defenders' Fortress +120, +180, +240 for own armies in the
  region (vanilla none); Officers' School, Royal Officers' School, Palace of War +30, +65, +105 experience per turn for
  characters (+20, +50, +80).
- Buildings give half (rounded down) when damaged and at low or medium influence (the Officer Schools keep the full
  value at low and medium influence).

### Progressive difficulty

- AI factions get bonuses that grow during the campaign. Players and rebels never get them.
  The first tier applies from the start of the campaign; other factions only get the building upkeep bonus before turn 20.

  | Bonus | Major factions, start | Major, turn 20 | Major, turn 50 | Major, turn 80 | Other factions, start | Other, turn 20 | Other, turn 50 | Other, turn 80 |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | Upkeep cost of all units | -10% | -30% | -80% | -100% | - | -15% | -40% | -65% |
  | Recruitment cost of all units | -20% | -50% | -80% | -100% | - | -25% | -50% | -75% |
  | All resources produced | +20% | +60% | +120% | +180% | - | +20% | +30% | +50% |
  | Local recruitment capacity | +2 | +6 | +12 | +20 | - | +2 | +6 | +10 |
  | Construction cost of all buildings | - | -20% | -60% | -100% | - | -10% | -20% | -40% |
  | Gold, stone and wood upkeep of all buildings | -80% | -80% | -80% | -80% | -80% | -80% | -80% | -80% |
  | Happiness in every province | - | +5 | +8 | +10 | - | +2 | +4 | +5 |

- Each tier's bonuses replace the previous ones (they do not add up). They show as the "Progressive Difficulty 0/I/II/III" effect on the AI faction.
- The bonuses also apply to campaigns started before the mod was installed, from the next load.
- Every bonus given or removed is logged to `dynasties_rebalance.log` in the game folder (and to the game's script log when script logging is enabled).

### Campaign AI targets

- AI armies prefer nearby targets and defend their own territory more, so AI empires grow into their neighbours instead of
  spreading across the map. When and how often the AI goes to war is unchanged.
- Distance now counts when the AI picks targets for its armies: targets more than 2 turns away lose priority, down to 20% of it
  at the far end of the range (10% for armies that are recruiting). In vanilla, almost every AI faction ignored distance.
- Task priorities, for every culture:
  - Lower: taking an enemy's last settlement wherever it is (was the AI's top priority), attacking any enemy settlement when the
    AI has not expanded recently, attacking the main threat's settlements anywhere, helping allies in coordinated wars.
  - Higher: attacking enemy regions and provinces bordering the AI's own, completing a province, consolidating borders (unused in vanilla).
  - Higher: defending besieged settlements, threatened regions, own regions and the capital, retaking lost territory, guarding borders with enemies.
- Overrides the "War Coordination Priority" mod, which raises the priority of helping allies.

### Unique characters

- When an AI faction is destroyed, by anyone, its unique characters join you (the faction that destroyed it if it is a
  human player, else the first human player). Unique means immortal, or a legendary character (character type containing
  `_hero_`, which also covers characters added by other mods that follow the game's naming, e.g. Make Character Unique).
- A unique general of yours that is not on the map, is not wounded and has never led an army for you appears next to your
  capital, alone. This also fixes characters that joined you but stayed greyed out in general recruitment.
  It happens once per character: you can disband a unique general's army afterwards and it does not come back.
- The game's 27 unique characters can serve in any faction: they are permitted everywhere, their bodyguard units are allowed
  for every faction, and their bodyguards (defined for their own culture only, e.g. Tausret's) apply to every culture.
  This replaces the "Unique Character Join" mod, which should be disabled (it gives the characters to the AI faction that
  destroyed theirs).
- Compatibility add-on for Make Character Unique (`dynasties_rebalance_compat_make_character_unique.pack`): its 48
  unique characters can serve in any faction too, and the game's unique characters can serve in the faction it adds.
  Enable it only together with Make Character Unique.
- Logged to `dynasties_rebalance.log`.

### Confederations at the start (separate mod)

- Separate pack, `dynasties_start_confederations.pack`: enable it on its own, with or without the main mod.
- When you start a new campaign as Hanigalbat, you confederate the AI faction that owns Sangaritu at the start (not a
  player, not rebels). Only in new campaigns, once. Logged to `dynasties_rebalance.log`.
