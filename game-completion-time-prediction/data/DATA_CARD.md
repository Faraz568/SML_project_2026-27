# gaming_player_completion_dataset.csv: data card

**Player data is SYNTHETIC. Game titles are real.** Every player and every player-game record was produced by a simulation
(`generate_gaming_dataset.py`, seed 42). It is not real player telemetry. All `Player_ID` values start with `SYN_`.

## What is real and what is simulated
| Part | Source |
|---|---|
| 100 game titles, genre, typical main-story hours | Real: HowLongToBeat and Steam data supplied with this project |
| Mission count | Researched: the real number of main-story missions for each game; the unit (missions, chapters, acts, required bosses...) and a source link per game are in `game_catalogue.csv` |
| Difficulty | From each game's real Steam user tags: "Difficult" in the top 6 tags = Very_Hard; "Difficult" anywhere or "Souls-like" in the top 10 = Hard; Casual / Relaxing / Cute / Family Friendly / Walking Simulator / Interactive Fiction = Easy; otherwise Normal |
| Story complexity, side quests, puzzles | Approximate: simple rules on each game's Steam tags and length |
| Players, first-two-hour behaviour, completion times | Synthetic |

## Files
| File | Contents |
|---|---|
| `gaming_player_completion_dataset.csv` | Messy, real-world-style extract: 51,250 rows, 27 columns |
| `gaming_player_completion_dataset_clean.csv` | Ground truth: 50,000 unique player-game records, no defects |
| `game_catalogue.csv` | The 100 games, their attributes, `Mission_Unit` and `Source` (URL for the mission count) |

## Uneven distributions
- Players have 1 to 20 games each (mean 5); popular games (by real Steam reviews) appear far more often.
- Completion times are right-skewed: median about 23 hours, mean about 30 hours, with a long tail up to about 335 hours.
- Within each game, the median player takes about the game's real typical main-story time.
- `Missions_Completed` (first two hours) can be 0: games with long acts or chapters (Divinity: Original Sin II has 4 acts) often finish none in two hours, while Plants vs. Zombies players finish about 12 levels. When it is 0, `Average_Mission_Time_Minutes` is the time spent on the unfinished first mission.

## Data-quality problems in the messy file (simulated)
- Missing values in 22 of 27 columns (about 1.8% of cells); habit columns are blank more often for beginners, and long puzzle times are more often missing.
- 750 exact duplicate rows and 500 near-duplicates (the same player and game logged twice with small differences).
- Inconsistent labels: case, spaces, separators, `Y`/`TRUE`/`1` for Yes, and typos such as `Begginer` and `Stratergy`; game names in mixed case.
- Impossible values: negative counts, percentages above 100, missions completed above the mission count, zero or negative completion times.
- Completion times entered in minutes or with an extra digit.
- Numbers stored as text (`4.8 years`, `16.3h`, `1,8`) and stray spaces in IDs.

## Target
`Completion_Time_Hours`: total hours one player needs to finish the game's main story.
Do not use `Player_ID`, `Game_ID` or `Game_Name` as predictive features; split by `Player_ID` so no player is in both train and test.

## Mission count sources
| Game | Missions | Unit | Source |
|---|---|---|---|
| Elden Ring | 12 | mandatory bosses | [link](https://gamerant.com/elden-ring-all-mandatory-bosses-order-godrick-radagon) |
| The Witcher 3: Wild Hunt | 55 | main quests | [link](https://www.gamepressure.com/thewitcher3/main-storyline/z978a9) |
| Baldur's Gate 3 | 30 | main story quests (prologue + 3 acts) | [link](https://www.videogamer.com/guides/baldurs-gate-3-acts) |
| Cyberpunk 2077 | 30 | main story missions (approx.) | [link](https://www.videogamer.com/news/cyberpunk-2077-main-story-mission-list/) |
| Dark Souls III | 13 | mandatory bosses | [link](https://darksouls3.wiki.fextralife.com/Bosses) |
| Fallout 4 | 11 | main quests | [link](https://fallout.fandom.com/wiki/Fallout_4_quests) |
| The Elder Scrolls V: Skyrim | 17 | required main quests | [link](https://en.uesp.net/wiki/Skyrim:Main_Quest) |
| Fallout: New Vegas | 13 | main quests on one route (5 shared + 7 Mr. House + final battle) | [link](https://www.gamepressure.com/falloutnewvegas/main-storyline/z429fc) |
| Assassin's Creed Odyssey | 76 | main quests (9 chapters) | [link](https://gamepressure.com/assassins-creed-odyssey/list-of-all-main-quests/zcb613) |
| Kingdom Come: Deliverance | 29 | main quests | [link](https://kingdom-come-deliverance.fandom.com/wiki/Main_quests_(KCD)) |
| Persona 5 Royal | 8 | palaces (main dungeons) | [link](https://progameguides.com/persona/how-many-palaces-are-there-in-persona-5-royal/) |
| Divinity: Original Sin II | 4 | acts | [link](https://gamingbolt.com/divinity-original-sin-2s-four-acts-were-originally-one-map) |
| Dragon's Dogma II | 18 | main story quests | [link](https://www.videogamer.com/guides/dragons-dogma-2-quests-main-story-side-missions) |
| Black Myth: Wukong | 6 | chapters | [link](https://shacknews.com/article/141068/how-many-chapters-in-black-myth-wukong) |
| Final Fantasy XV: Royal Edition | 14 | chapters | [link](https://www.rpgsite.net/feature/5143-final-fantasy-xv-guide-chapters-umbra-and-understanding-points-of-no-return) |
| The Witcher 2: Assassins of Kings | 5 | story parts (prologue + 3 chapters + epilogue) | [link](https://www.wikiwand.com/en/articles/Witcher_2) |
| Persona 4 Golden | 8 | main story dungeons | [link](https://www.thegamer.com/persona-4-golden-dungeons-ranked/) |
| Starfield | 19 | main missions | [link](https://www.gameleap.com/articles/starfield-how-many-main-quest-missions-are-there) |
| Borderlands 3 | 23 | main story missions (numbered list) | [link](https://primagames.com/tips/borderlands-3-main-story-mission-list) |
| Dark Souls: Remastered | 13 | mandatory bosses | [link](https://darksouls.wiki.fextralife.com/Area+Bosses) |
| Dark Souls II: Scholar of the First Sin | 12 | required bosses (8 main bosses + 4 Great Soul bosses) | [link](https://gamertweak.com/main-bosses-dark-souls-2) |
| Monster Hunter: World | 27 | assignments (base game) | [link](https://monsterhunterworld.wiki.fextralife.com/Assignments) |
| South Park: The Stick of Truth | 8 | main story quests | [link](https://en.wikibooks.org/wiki/South_Park:_The_Stick_of_Truth/Printable_version) |
| Middle-Earth: Shadow of War | 44 | main story missions (prologue + acts 1-3) | [link](https://www.gamepressure.com/middle-earth-shadow-of-war/list-of-all-main-missions/z410739) |
| Star Wars Jedi: Survivor | 23 | main story missions (6 chapters) | [link](https://www.charlieintel.com/star-wars-jedi/how-many-chapters-in-star-wars-jedi-survivor-full-mission-list-248409/) |
| Resident Evil 4 | 16 | chapters | [link](https://www.pushsquare.com/guides/resident-evil-4-remake-how-many-chapters-are-there) |
| Doom | 13 | missions | [link](https://stevivor.com/guides/many-missions-doom/) |
| Doom Eternal | 13 | missions | [link](https://powerup-gaming.com/2020/03/18/how-many-missions-are-in-doom-eternal/) |
| Half-Life 2 | 13 | chapters | [link](https://developer.valvesoftware.com/wiki/Half-Life_2) |
| Resident Evil Village | 5 | story segments (4 lords' domains + finale) | [link](https://ggrecon.com/articles/how-long-is-resident-evil-village) |
| Cuphead | 28 | bosses (base game) | [link](https://cuphead.wiki.gg/wiki/List_of_Bosses) |
| Devil May Cry 5 | 20 | missions | [link](https://press-start.com.au/guides/2019/03/07/heres-how-many-missions-are-in-devil-may-cry-5/) |
| Ori and the Will of the Wisps | 13 | levels/areas | [link](https://powerup-gaming.com/2020/03/10/how-many-levels-are-in-ori-and-the-will-of-the-wisps) |
| Hotline Miami | 19 | chapters | [link](https://handwiki.org/wiki/Software:Hotline_Miami) |
| Sekiro: Shadows Die Twice | 13 | main bosses (incl. some optional) | [link](https://www.pushsquare.com/news/2019/04/guide_sekiro_shadows_die_twice_-_how_to_kill_all_main_bosses) |
| Hollow Knight | 10 | required bosses (approx.) | [link](https://rogueranker.com/hollow-knight-boss-order/) |
| Metal Gear Rising: Revengeance | 7 | chapters | [link](https://attackofthefanboy.com/?p=186723) |
| Dishonored | 10 | missions | [link](https://dishonored.fandom.com/wiki/Category:Missions) |
| Armored Core VI: Fires of Rubicon | 37 | missions listed for one playthrough (5 chapters) | [link](https://www.pushsquare.com/guides/armored-core-6-how-many-missions-and-chapters-are-there) |
| Ghostrunner | 17 | missions | [link](https://www.gamerevolution.com/guides/663773-ghostrunner-mission-list-how-many-levels) |
| Black Mesa | 19 | chapters | [link](https://developer.valvesoftware.com/wiki/Black_Mesa_(Source)) |
| Titanfall 2 | 9 | missions | [link](https://StrategyWiki.org/wiki/Titanfall_2/Walkthrough) |
| Half-Life | 19 | playable chapters | [link](https://developer.valvesoftware.com/wiki/Half-Life) |
| Dishonored 2 | 9 | missions | [link](https://stevivor.com/guides/many-missions-dishonored-2/) |
| Borderlands 2 | 19 | story missions | [link](https://borderlands.fandom.com/wiki/Borderlands_2_Story_Missions) |
| Control | 10 | main story missions | [link](https://www.gamepressure.com/control/main-story-missions-list/z3c826) |
| Star Wars Jedi: Fallen Order | 6 | chapters | [link](https://www.pcgamesn.com/star-wars-jedi-fallen-order/how-many-chapters-in-jedi-fallen-order) |
| Portal 2 | 9 | chapters | [link](https://strategywiki.org/wiki/Portal_2/Table_of_Contents) |
| Undertale | 5 | main areas | [link](https://undertale.wiki/w/Underground) |
| Tomb Raider | 24 | walkthrough chapters | [link](https://strategywiki.org/wiki/Tomb_Raider_(2013)) |
| Detroit: Become Human | 32 | chapters | [link](https://powerup-gaming.com/2018/05/24/detroit-become-human-chapters) |
| God of War | 17 | main journey objectives | [link](https://powerup-gaming.com/2018/04/20/how-many-chapters-in-god-of-war/) |
| Stray | 12 | chapters | [link](https://www.pushsquare.com/guides/stray-how-many-chapters-are-there) |
| BioShock Infinite | 39 | walkthrough chapters | [link](https://www.gamepressure.com/bioshockinfinite) |
| NieR: Automata | 27 | chapters (routes A to C) | [link](https://www.gamepressure.com/nier-automata/list-of-all-routes-and-chapters/z0eae5) |
| Rise of the Tomb Raider | 39 | walkthrough chapters | [link](https://www.gamepressure.com/riseofthetombraider/all-chapters-list/z2d671) |
| The Last of Us Part I | 12 | chapters | [link](https://www.pushsquare.com/guides/the-last-of-us-1-all-chapters-and-how-long-to-beat) |
| Max Payne 3 | 14 | chapters | [link](https://www.gamepressure.com/maxpayne3/walkthrough/ze3a7c) |
| A Plague Tale: Innocence | 17 | chapters | [link](https://progameguides.com/a-plague-tale-innocence/a-plague-tale-innocence-chapter-list/) |
| Life Is Strange 2 | 5 | episodes | [link](https://stevivor.com/news/life-is-strange-2-release-date-number-of-episodes-confirmed) |
| Alan Wake | 6 | episodes | [link](https://www.gamesradar.com/how-long-is-alan-wake) |
| Little Nightmares II | 5 | chapters | [link](https://republicworld.com/tech/gaming/how-many-chapters-are-there-in-little-nightmares-2-know-details) |
| The Wolf Among Us | 5 | episodes | [link](https://fables.fandom.com/wiki/The_Wolf_Among_Us) |
| Metro 2033 Redux | 37 | missions (7 chapters + prologue) | [link](https://sportskeeda.com/esports/how-long-metro-2033-redux-complete-list-missions-provided) |
| Ori and the Blind Forest: Definitive Edition | 15 | walkthrough parts (areas) | [link](https://gamerwalkthroughs.com/ori-and-the-blind-forest/) |
| Age of Empires IV | 35 | campaign missions | [link](https://www.gamepressure.com/age-of-empires-iv/list-of-all-missions/zef2cc) |
| XCOM: Enemy Unknown | 4 | storyline missions | [link](https://xcom.fandom.com/wiki/Missions_(XCOM:_Enemy_Unknown)) |
| Plants vs. Zombies | 50 | adventure mode levels | [link](https://plantsvszombies.wiki.gg/wiki/Plants_vs_Zombies) |
| Company of Heroes 2 | 14 | campaign missions | [link](https://www.gamepressure.com/companyofheroes2/the-campaign-mode/z75189) |
| Shadow Tactics: Blades of the Shogun | 13 | campaign missions | [link](https://www.gamepressure.com/shadowtactics/campaign/zf9420) |
| FTL: Faster Than Light | 8 | sectors per run | [link](https://ftl.fandom.com/wiki/Sectors) |
| Age of Empires II: Definitive Edition | 31 | original Age of Kings campaign scenarios | [link](https://ageofempires.fandom.com/wiki/Campaign_(Age_of_Empires_II)) |
| Command & Conquer Remastered Collection | 100 | campaign missions (approx.; incl. expansions) | [link](https://www.wikiwand.com/en/articles/Command_&_Conquer_Remastered_Collection) |
| Age of Mythology: Extended Edition | 32 | campaign missions | [link](https://speeddemosarchive.com/AgeOfMythology.html) |
| Warhammer 40,000: Dawn of War III | 17 | campaign missions | [link](https://gamepressure.com/newsroom/dawn-of-war-iii-will-offer-17-solo-missions-for-a-10-hour-campaig/zc2ee) |
| Northgard | 11 | campaign chapters | [link](https://www.pcgamer.com/northgard-release-date-set-11-chapter-campaign-incoming) |
| Days Gone | 113 | story missions (15 chapters) | [link](https://www.gamepressure.com/days-gone/list-of-all-story-missions/z5c297) |
| Dead Space 2 | 15 | chapters | [link](https://strategywiki.org/wiki/Dead_Space_2/Table_of_Contents) |
| Far Cry Primal | 31 | story missions | [link](https://www.gamepressure.com/farcryprimal/walkthrough/za8648) |
| S.T.A.L.K.E.R.: Shadow of Chernobyl | 41 | main quests | [link](https://www.gamepressure.com/stalker/full-list-of-main-quests/zba6d) |
| Dead Island: Definitive Edition | 28 | main quest entries (4 acts) | [link](https://gamepressure.com/deadisland) |
| The Long Dark | 5 | story episodes (Wintermute) | [link](https://www.pcgamer.com/games/survival-crafting/the-end-of-the-long-dark-is-in-sight-after-over-a-decade-in-development-culminating-in-a-fifth-and-final-story-episode-that-is-3-to-4-times-as-big-as-episode-4) |
| Valheim | 7 | bosses (the Forsaken) | [link](https://allthings.how/valheim-boss-order-all-seven-forsaken-and-how-to-summon-them/) |
| Don't Starve | 6 | adventure mode chapters (5 + epilogue) | [link](https://dontstarve.wiki.gg/wiki/Adventure_Mode) |
| Grand Theft Auto V | 69 | story missions | [link](https://www.sportskeeda.com/gta/gta-5-how-many-missions-game) |
| Red Dead Redemption 2 | 104 | story missions | [link](https://stevivor.com/guides/many-chapters-missions-red-dead-redemption-2) |
| Horizon Zero Dawn - Complete Edition | 23 | main story missions | [link](https://expertbeacon.com/how-many-levels-is-horizon-zero-dawn/) |
| Hogwarts Legacy | 42 | main quests | [link](https://www.ginx.tv/en/?p=42397) |
| Marvel's Spider-Man: Game of the Year Edition | 41 | main missions | [link](https://www.gamepressure.com/marvels-spider-man/main-missions/z0b419) |
| Ghost of Tsushima | 26 | main tales | [link](https://www.gamepressure.com/ghost-of-tsushima/all-main-tales-list/zfd6cb) |
| Batman: Arkham Knight | 36 | campaign walkthrough chapters | [link](https://www.gamerguides.com/batman-arkham-knight/guide/walkthrough/campaign-walkthrough/countdown-to-knightfall-free-roam) |
| Metal Gear Solid V: The Phantom Pain | 51 | main missions | [link](https://www.gamerevolution.com/guides/68911-metal-gear-solid-v-the-phantom-pain-full-mission-and-episode-list-no-spoilers) |
| Mafia: Definitive Edition | 20 | chapters | [link](https://stevivor.com/guides/many-chapters-mafia-definitive-edition) |
| Watch Dogs 2 | 15 | main operations | [link](https://www.itechguides.com/watch-dogs-2-how-many-main-operations-are-there/) |
| Far Cry 3 | 39 | main missions | [link](https://www.gamepressure.com/farcry3/main-missions/zb44b1) |
| Dying Light | 15 | main story quests | [link](https://dyinglight.wiki.gg/wiki/Quests_(Dying_Light)) |
| Middle-Earth: Shadow of Mordor | 21 | main missions | [link](https://www.gamepressure.com/shadowofmordor/main-missions/z669be) |
| Mafia II | 15 | chapters | [link](https://www.goodnovel.com/qa/many-chapters-mafia-2) |
| Assassin's Creed II | 14 | sequences | [link](https://www.gamepur.com/guides/assassins-creed-2-how-many-sequences-are-in-ac2) |
| Sleeping Dogs: Definitive Edition | 28 | story missions | [link](https://www.gamesradar.com/sleeping-dogs-story-missions-guide/) |

Counts marked "approx." are rounded figures from the source; units differ between games because each game structures its story differently.
