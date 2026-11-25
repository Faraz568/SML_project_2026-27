"""
SYNTHETIC DATA GENERATOR  (player behaviour is simulated; game titles are real)
==============================================================================
Creates three files:

  gaming_player_completion_dataset_clean.csv  ground truth: 50,000 unique player-game records, no defects
  gaming_player_completion_dataset.csv        the SAME experiences as a real-world-style MESSY extract
                                              (missing values, duplicates, inconsistent labels, impossible values,
                                              numbers stored as text, uneven distributions)
  game_catalogue.csv                          the 100 real games and their attributes

WHAT IS REAL AND WHAT IS SYNTHETIC
  Real:       the 100 game titles, their genres, and their typical main-story length (from the HowLongToBeat data
              supplied with this project) and Steam review counts (used only to make popular games more common).
  Researched:  Mission_Count = the game's real number of main-story missions/chapters/acts/required bosses (unit and
              source URL per game in game_catalogue.csv). Game_Difficulty from the game's Steam user tags
              ('Difficult' in top 6 -> Very_Hard; 'Difficult' or 'Souls-like' -> Hard; Casual/Relaxing/Cute... -> Easy).
  Approximate: story complexity, side-quest and puzzle labels (simple rules on Steam tags and length).
  Synthetic:  every player and every player-game record: experience, playstyle, behaviour in the first two hours,
              and the completion time. No real player data is used. Player_ID values start with "SYN_".

Usage:  python generate_gaming_dataset.py [output_directory]
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
N_PLAYERS = 10_000
N_RECORDS = 50_000
OUT_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
OUT_DIR.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(SEED)

# -------------------------------------------------------------------------------------------------
# 1. REAL GAME CATALOGUE
# (Game_ID, Game_Name, Genre, Difficulty, Open_World, Mission_Count, Complexity, Side_Quests, Puzzles, Typical_Hours, Steam_Reviews, Mission_Unit, Source)
# -------------------------------------------------------------------------------------------------
CATALOGUE = [
    ('G001', 'Elden Ring', 'RPG', 'Very_Hard', 'Yes', 12, 'High', 'Yes', 'Low', 59.8, 1056677, 'mandatory bosses', 'https://gamerant.com/elden-ring-all-mandatory-bosses-order-godrick-radagon'),
    ('G002', 'The Witcher 3: Wild Hunt', 'RPG', 'Normal', 'Yes', 55, 'High', 'Yes', 'Low', 51.5, 835349, 'main quests', 'https://www.gamepressure.com/thewitcher3/main-storyline/z978a9'),
    ('G003', "Baldur's Gate 3", 'RPG', 'Normal', 'No', 30, 'High', 'Yes', 'Low', 70.3, 760662, 'main story quests (prologue + 3 acts)', 'https://www.videogamer.com/guides/baldurs-gate-3-acts'),
    ('G004', 'Cyberpunk 2077', 'RPG', 'Normal', 'Yes', 30, 'High', 'Yes', 'Medium', 25.7, 844921, 'main story missions (approx.)', 'https://www.videogamer.com/news/cyberpunk-2077-main-story-mission-list/'),
    ('G005', 'Dark Souls III', 'RPG', 'Very_Hard', 'Yes', 13, 'High', 'Yes', 'Medium', 31.6, 413775, 'mandatory bosses', 'https://darksouls3.wiki.fextralife.com/Bosses'),
    ('G006', 'Fallout 4', 'RPG', 'Normal', 'Yes', 11, 'High', 'Yes', 'Medium', 27.5, 392287, 'main quests', 'https://fallout.fandom.com/wiki/Fallout_4_quests'),
    ('G007', 'The Elder Scrolls V: Skyrim', 'RPG', 'Normal', 'Yes', 17, 'High', 'Yes', 'Low', 34.7, 317279, 'required main quests', 'https://en.uesp.net/wiki/Skyrim:Main_Quest'),
    ('G008', 'Fallout: New Vegas', 'RPG', 'Normal', 'Yes', 13, 'High', 'Yes', 'Medium', 26.9, 227700, 'main quests on one route (5 shared + 7 Mr. House + final battle)', 'https://www.gamepressure.com/falloutnewvegas/main-storyline/z429fc'),
    ('G009', "Assassin's Creed Odyssey", 'RPG', 'Normal', 'Yes', 76, 'High', 'Yes', 'Medium', 45.4, 172193, 'main quests (9 chapters)', 'https://gamepressure.com/assassins-creed-odyssey/list-of-all-main-quests/zcb613'),
    ('G010', 'Kingdom Come: Deliverance', 'RPG', 'Normal', 'Yes', 29, 'High', 'Yes', 'Low', 41.8, 162206, 'main quests', 'https://kingdom-come-deliverance.fandom.com/wiki/Main_quests_(KCD)'),
    ('G011', 'Persona 5 Royal', 'RPG', 'Normal', 'No', 8, 'High', 'Yes', 'Medium', 101.3, 103144, 'palaces (main dungeons)', 'https://progameguides.com/persona/how-many-palaces-are-there-in-persona-5-royal/'),
    ('G012', 'Divinity: Original Sin II', 'RPG', 'Normal', 'No', 4, 'High', 'Yes', 'Medium', 59.1, 190124, 'acts', 'https://gamingbolt.com/divinity-original-sin-2s-four-acts-were-originally-one-map'),
    ('G013', "Dragon's Dogma II", 'RPG', 'Normal', 'Yes', 18, 'Medium', 'Yes', 'Low', 30.7, 106939, 'main story quests', 'https://www.videogamer.com/guides/dragons-dogma-2-quests-main-story-side-missions'),
    ('G014', 'Black Myth: Wukong', 'RPG', 'Hard', 'No', 6, 'High', 'Yes', 'Low', 37.6, 1150098, 'chapters', 'https://shacknews.com/article/141068/how-many-chapters-in-black-myth-wukong'),
    ('G015', 'Final Fantasy XV: Royal Edition', 'RPG', 'Normal', 'Yes', 14, 'High', 'Yes', 'Low', 27.3, 53688, 'chapters', 'https://www.rpgsite.net/feature/5143-final-fantasy-xv-guide-chapters-umbra-and-understanding-points-of-no-return'),
    ('G016', 'The Witcher 2: Assassins of Kings', 'RPG', 'Hard', 'Yes', 5, 'High', 'Yes', 'Low', 24.1, 87064, 'story parts (prologue + 3 chapters + epilogue)', 'https://www.wikiwand.com/en/articles/Witcher_2'),
    ('G017', 'Persona 4 Golden', 'RPG', 'Normal', 'No', 8, 'High', 'Yes', 'Medium', 67.5, 78346, 'main story dungeons', 'https://www.thegamer.com/persona-4-golden-dungeons-ranked/'),
    ('G018', 'Starfield', 'RPG', 'Normal', 'Yes', 19, 'High', 'Yes', 'Medium', 23.2, 165527, 'main missions', 'https://www.gameleap.com/articles/starfield-how-many-main-quest-missions-are-there'),
    ('G019', 'Borderlands 3', 'RPG', 'Normal', 'Yes', 23, 'Medium', 'Yes', 'Low', 23.4, 149065, 'main story missions (numbered list)', 'https://primagames.com/tips/borderlands-3-main-story-mission-list'),
    ('G020', 'Dark Souls: Remastered', 'RPG', 'Very_Hard', 'No', 13, 'High', 'Yes', 'Medium', 29.5, 129299, 'mandatory bosses', 'https://darksouls.wiki.fextralife.com/Area+Bosses'),
    ('G021', 'Dark Souls II: Scholar of the First Sin', 'RPG', 'Very_Hard', 'No', 12, 'High', 'Yes', 'Low', 35.7, 116710, 'required bosses (8 main bosses + 4 Great Soul bosses)', 'https://gamertweak.com/main-bosses-dark-souls-2'),
    ('G022', 'Monster Hunter: World', 'RPG', 'Hard', 'Yes', 27, 'High', 'Yes', 'Medium', 47.1, 493390, 'assignments (base game)', 'https://monsterhunterworld.wiki.fextralife.com/Assignments'),
    ('G023', 'South Park: The Stick of Truth', 'RPG', 'Normal', 'Yes', 8, 'Medium', 'Yes', 'Medium', 11.4, 68305, 'main story quests', 'https://en.wikibooks.org/wiki/South_Park:_The_Stick_of_Truth/Printable_version'),
    ('G024', 'Middle-Earth: Shadow of War', 'RPG', 'Normal', 'Yes', 44, 'High', 'Yes', 'Medium', 20.9, 107218, 'main story missions (prologue + acts 1-3)', 'https://www.gamepressure.com/middle-earth-shadow-of-war/list-of-all-main-missions/z410739'),
    ('G025', 'Star Wars Jedi: Survivor', 'RPG', 'Hard', 'Yes', 23, 'High', 'Yes', 'Medium', 20.3, 67054, 'main story missions (6 chapters)', 'https://www.charlieintel.com/star-wars-jedi/how-many-chapters-in-star-wars-jedi-survivor-full-mission-list-248409/'),
    ('G026', 'Resident Evil 4', 'Action', 'Hard', 'No', 16, 'Medium', 'No', 'Low', 15.6, 82434, 'chapters', 'https://www.pushsquare.com/guides/resident-evil-4-remake-how-many-chapters-are-there'),
    ('G027', 'Doom', 'Action', 'Hard', 'No', 13, 'Medium', 'No', 'Low', 11.7, 207279, 'missions', 'https://stevivor.com/guides/many-missions-doom/'),
    ('G028', 'Doom Eternal', 'Action', 'Hard', 'No', 13, 'Medium', 'No', 'Low', 14.4, 206026, 'missions', 'https://powerup-gaming.com/2020/03/18/how-many-missions-are-in-doom-eternal/'),
    ('G029', 'Half-Life 2', 'Action', 'Normal', 'No', 13, 'Medium', 'No', 'Low', 12.9, 245627, 'chapters', 'https://developer.valvesoftware.com/wiki/Half-Life_2'),
    ('G030', 'Resident Evil Village', 'Action', 'Normal', 'Yes', 5, 'Medium', 'Yes', 'Low', 9.8, 119350, "story segments (4 lords' domains + finale)", 'https://ggrecon.com/articles/how-long-is-resident-evil-village'),
    ('G031', 'Cuphead', 'Action', 'Very_Hard', 'No', 28, 'Medium', 'No', 'Low', 10.6, 186835, 'bosses (base game)', 'https://cuphead.wiki.gg/wiki/List_of_Bosses'),
    ('G032', 'Devil May Cry 5', 'Action', 'Hard', 'No', 20, 'Medium', 'No', 'Low', 11.1, 146133, 'missions', 'https://press-start.com.au/guides/2019/03/07/heres-how-many-missions-are-in-devil-may-cry-5/'),
    ('G033', 'Ori and the Will of the Wisps', 'Action', 'Hard', 'Yes', 13, 'Medium', 'Yes', 'Medium', 11.9, 136690, 'levels/areas', 'https://powerup-gaming.com/2020/03/10/how-many-levels-are-in-ori-and-the-will-of-the-wisps'),
    ('G034', 'Hotline Miami', 'Action', 'Hard', 'No', 19, 'Low', 'No', 'Low', 5.2, 106657, 'chapters', 'https://handwiki.org/wiki/Software:Hotline_Miami'),
    ('G035', 'Sekiro: Shadows Die Twice', 'Action', 'Very_Hard', 'Yes', 13, 'High', 'Yes', 'Medium', 30.0, 322234, 'main bosses (incl. some optional)', 'https://www.pushsquare.com/news/2019/04/guide_sekiro_shadows_die_twice_-_how_to_kill_all_main_bosses'),
    ('G036', 'Hollow Knight', 'Action', 'Very_Hard', 'Yes', 10, 'High', 'Yes', 'Medium', 27.0, 415946, 'required bosses (approx.)', 'https://rogueranker.com/hollow-knight-boss-order/'),
    ('G037', 'Metal Gear Rising: Revengeance', 'Action', 'Hard', 'No', 7, 'Medium', 'No', 'Medium', 7.2, 83293, 'chapters', 'https://attackofthefanboy.com/?p=186723'),
    ('G038', 'Dishonored', 'Action', 'Normal', 'Yes', 10, 'Medium', 'Yes', 'Medium', 12.2, 82370, 'missions', 'https://dishonored.fandom.com/wiki/Category:Missions'),
    ('G039', 'Armored Core VI: Fires of Rubicon', 'Action', 'Hard', 'No', 37, 'Medium', 'No', 'Low', 17.6, 77042, 'missions listed for one playthrough (5 chapters)', 'https://www.pushsquare.com/guides/armored-core-6-how-many-missions-and-chapters-are-there'),
    ('G040', 'Ghostrunner', 'Action', 'Very_Hard', 'No', 17, 'Low', 'No', 'Low', 7.1, 63149, 'missions', 'https://www.gamerevolution.com/guides/663773-ghostrunner-mission-list-how-many-levels'),
    ('G041', 'Black Mesa', 'Action', 'Normal', 'No', 19, 'High', 'No', 'Low', 15.2, 127693, 'chapters', 'https://developer.valvesoftware.com/wiki/Black_Mesa_(Source)'),
    ('G042', 'Titanfall 2', 'Action', 'Normal', 'No', 9, 'Low', 'No', 'Low', 6.1, 256188, 'missions', 'https://StrategyWiki.org/wiki/Titanfall_2/Walkthrough'),
    ('G043', 'Half-Life', 'Action', 'Hard', 'No', 19, 'Medium', 'No', 'Low', 12.0, 148221, 'playable chapters', 'https://developer.valvesoftware.com/wiki/Half-Life'),
    ('G044', 'Dishonored 2', 'Action', 'Normal', 'Yes', 9, 'Medium', 'Yes', 'Medium', 12.5, 62782, 'missions', 'https://stevivor.com/guides/many-missions-dishonored-2/'),
    ('G045', 'Borderlands 2', 'Action', 'Normal', 'Yes', 19, 'Medium', 'Yes', 'Low', 30.2, 295218, 'story missions', 'https://borderlands.fandom.com/wiki/Borderlands_2_Story_Missions'),
    ('G046', 'Control', 'Action', 'Hard', 'Yes', 10, 'Medium', 'Yes', 'Medium', 11.7, 50448, 'main story missions', 'https://www.gamepressure.com/control/main-story-missions-list/z3c826'),
    ('G047', 'Star Wars Jedi: Fallen Order', 'Action', 'Hard', 'Yes', 6, 'High', 'Yes', 'Medium', 17.2, 158579, 'chapters', 'https://www.pcgamesn.com/star-wars-jedi-fallen-order/how-many-chapters-in-jedi-fallen-order'),
    ('G048', 'Portal 2', 'Adventure', 'Normal', 'No', 9, 'Medium', 'No', 'High', 8.6, 433510, 'chapters', 'https://strategywiki.org/wiki/Portal_2/Table_of_Contents'),
    ('G049', 'Undertale', 'Adventure', 'Normal', 'No', 5, 'Medium', 'No', 'Low', 6.9, 272932, 'main areas', 'https://undertale.wiki/w/Underground'),
    ('G050', 'Tomb Raider', 'Adventure', 'Normal', 'No', 24, 'Medium', 'Yes', 'Medium', 11.3, 247930, 'walkthrough chapters', 'https://strategywiki.org/wiki/Tomb_Raider_(2013)'),
    ('G051', 'Detroit: Become Human', 'Adventure', 'Normal', 'No', 32, 'Medium', 'No', 'Low', 12.1, 169199, 'chapters', 'https://powerup-gaming.com/2018/05/24/detroit-become-human-chapters'),
    ('G052', 'God of War', 'Adventure', 'Normal', 'Yes', 17, 'High', 'Yes', 'Medium', 20.6, 158017, 'main journey objectives', 'https://powerup-gaming.com/2018/04/20/how-many-chapters-in-god-of-war/'),
    ('G053', 'Stray', 'Adventure', 'Easy', 'Yes', 12, 'Low', 'Yes', 'Medium', 5.1, 156607, 'chapters', 'https://www.pushsquare.com/guides/stray-how-many-chapters-are-there'),
    ('G054', 'BioShock Infinite', 'Adventure', 'Normal', 'No', 39, 'Medium', 'No', 'Low', 11.6, 140682, 'walkthrough chapters', 'https://www.gamepressure.com/bioshockinfinite'),
    ('G055', 'NieR: Automata', 'Adventure', 'Normal', 'Yes', 27, 'High', 'Yes', 'Low', 21.2, 140169, 'chapters (routes A to C)', 'https://www.gamepressure.com/nier-automata/list-of-all-routes-and-chapters/z0eae5'),
    ('G056', 'Rise of the Tomb Raider', 'Adventure', 'Normal', 'Yes', 39, 'Medium', 'Yes', 'Medium', 13.3, 136180, 'walkthrough chapters', 'https://www.gamepressure.com/riseofthetombraider/all-chapters-list/z2d671'),
    ('G057', 'The Last of Us Part I', 'Adventure', 'Normal', 'No', 12, 'Medium', 'No', 'Low', 14.3, 79855, 'chapters', 'https://www.pushsquare.com/guides/the-last-of-us-1-all-chapters-and-how-long-to-beat'),
    ('G058', 'Max Payne 3', 'Adventure', 'Normal', 'Yes', 14, 'Medium', 'Yes', 'Low', 10.0, 57076, 'chapters', 'https://www.gamepressure.com/maxpayne3/walkthrough/ze3a7c'),
    ('G059', 'A Plague Tale: Innocence', 'Adventure', 'Normal', 'No', 17, 'Medium', 'No', 'Medium', 10.9, 63042, 'chapters', 'https://progameguides.com/a-plague-tale-innocence/a-plague-tale-innocence-chapter-list/'),
    ('G060', 'Life Is Strange 2', 'Adventure', 'Normal', 'No', 5, 'High', 'No', 'Medium', 16.1, 36634, 'episodes', 'https://stevivor.com/news/life-is-strange-2-release-date-number-of-episodes-confirmed'),
    ('G061', 'Alan Wake', 'Adventure', 'Normal', 'No', 6, 'Medium', 'No', 'Medium', 11.2, 49163, 'episodes', 'https://www.gamesradar.com/how-long-is-alan-wake'),
    ('G062', 'Little Nightmares II', 'Adventure', 'Normal', 'No', 5, 'Medium', 'No', 'High', 5.6, 43042, 'chapters', 'https://republicworld.com/tech/gaming/how-many-chapters-are-there-in-little-nightmares-2-know-details'),
    ('G063', 'The Wolf Among Us', 'Adventure', 'Normal', 'No', 5, 'Medium', 'No', 'Medium', 8.6, 35678, 'episodes', 'https://fables.fandom.com/wiki/The_Wolf_Among_Us'),
    ('G064', 'Metro 2033 Redux', 'Adventure', 'Normal', 'Yes', 37, 'Medium', 'Yes', 'Medium', 9.1, 110967, 'missions (7 chapters + prologue)', 'https://sportskeeda.com/esports/how-long-metro-2033-redux-complete-list-missions-provided'),
    ('G065', 'Ori and the Blind Forest: Definitive Edition', 'Adventure', 'Hard', 'Yes', 15, 'Medium', 'Yes', 'Medium', 9.0, 66979, 'walkthrough parts (areas)', 'https://gamerwalkthroughs.com/ori-and-the-blind-forest/'),
    ('G066', 'Age of Empires IV', 'Strategy', 'Normal', 'Yes', 35, 'Medium', 'Yes', 'Medium', 28.2, 80870, 'campaign missions', 'https://www.gamepressure.com/age-of-empires-iv/list-of-all-missions/zef2cc'),
    ('G067', 'XCOM: Enemy Unknown', 'Strategy', 'Hard', 'No', 4, 'Medium', 'No', 'Medium', 26.7, 56414, 'storyline missions', 'https://xcom.fandom.com/wiki/Missions_(XCOM:_Enemy_Unknown)'),
    ('G068', 'Plants vs. Zombies', 'Strategy', 'Easy', 'No', 50, 'Low', 'No', 'Medium', 8.2, 139925, 'adventure mode levels', 'https://plantsvszombies.wiki.gg/wiki/Plants_vs_Zombies'),
    ('G069', 'Company of Heroes 2', 'Strategy', 'Normal', 'No', 14, 'Medium', 'No', 'Medium', 15.5, 109825, 'campaign missions', 'https://www.gamepressure.com/companyofheroes2/the-campaign-mode/z75189'),
    ('G070', 'Shadow Tactics: Blades of the Shogun', 'Strategy', 'Hard', 'No', 13, 'Medium', 'No', 'Medium', 24.9, 37237, 'campaign missions', 'https://www.gamepressure.com/shadowtactics/campaign/zf9420'),
    ('G071', 'FTL: Faster Than Light', 'Strategy', 'Hard', 'No', 8, 'Medium', 'No', 'Medium', 12.2, 75052, 'sectors per run', 'https://ftl.fandom.com/wiki/Sectors'),
    ('G072', 'Age of Empires II: Definitive Edition', 'Strategy', 'Normal', 'No', 31, 'Medium', 'No', 'Medium', 39.9, 162462, 'original Age of Kings campaign scenarios', 'https://ageofempires.fandom.com/wiki/Campaign_(Age_of_Empires_II)'),
    ('G073', 'Command & Conquer Remastered Collection', 'Strategy', 'Normal', 'No', 100, 'Medium', 'No', 'Medium', 32.1, 32960, 'campaign missions (approx.; incl. expansions)', 'https://www.wikiwand.com/en/articles/Command_&_Conquer_Remastered_Collection'),
    ('G074', 'Age of Mythology: Extended Edition', 'Strategy', 'Normal', 'No', 32, 'High', 'No', 'Medium', 28.6, 35308, 'campaign missions', 'https://speeddemosarchive.com/AgeOfMythology.html'),
    ('G075', 'Warhammer 40,000: Dawn of War III', 'Strategy', 'Normal', 'No', 17, 'High', 'No', 'Medium', 17.3, 22517, 'campaign missions', 'https://gamepressure.com/newsroom/dawn-of-war-iii-will-offer-17-solo-missions-for-a-10-hour-campaig/zc2ee'),
    ('G076', 'Northgard', 'Strategy', 'Normal', 'No', 11, 'Medium', 'No', 'Medium', 14.5, 64695, 'campaign chapters', 'https://www.pcgamer.com/northgard-release-date-set-11-chapter-campaign-incoming'),
    ('G077', 'Days Gone', 'Survival', 'Normal', 'Yes', 113, 'High', 'Yes', 'Low', 36.3, 103143, 'story missions (15 chapters)', 'https://www.gamepressure.com/days-gone/list-of-all-story-missions/z5c297'),
    ('G078', 'Dead Space 2', 'Survival', 'Normal', 'No', 15, 'Medium', 'No', 'Low', 9.1, 25946, 'chapters', 'https://strategywiki.org/wiki/Dead_Space_2/Table_of_Contents'),
    ('G079', 'Far Cry Primal', 'Survival', 'Normal', 'Yes', 31, 'Medium', 'Yes', 'Medium', 14.8, 32892, 'story missions', 'https://www.gamepressure.com/farcryprimal/walkthrough/za8648'),
    ('G080', 'S.T.A.L.K.E.R.: Shadow of Chernobyl', 'Survival', 'Hard', 'Yes', 41, 'Medium', 'Yes', 'Low', 15.1, 47291, 'main quests', 'https://www.gamepressure.com/stalker/full-list-of-main-quests/zba6d'),
    ('G081', 'Dead Island: Definitive Edition', 'Survival', 'Normal', 'Yes', 28, 'Medium', 'Yes', 'Low', 15.9, 25527, 'main quest entries (4 acts)', 'https://gamepressure.com/deadisland'),
    ('G082', 'The Long Dark', 'Survival', 'Hard', 'Yes', 5, 'Medium', 'Yes', 'Medium', 21.9, 112575, 'story episodes (Wintermute)', 'https://www.pcgamer.com/games/survival-crafting/the-end-of-the-long-dark-is-in-sight-after-over-a-decade-in-development-culminating-in-a-fifth-and-final-story-episode-that-is-3-to-4-times-as-big-as-episode-4'),
    ('G083', 'Valheim', 'Survival', 'Hard', 'Yes', 7, 'High', 'Yes', 'Medium', 79.4, 499828, 'bosses (the Forsaken)', 'https://allthings.how/valheim-boss-order-all-seven-forsaken-and-how-to-summon-them/'),
    ('G084', "Don't Starve", 'Survival', 'Hard', 'Yes', 6, 'Medium', 'Yes', 'Medium', 29.0, 109816, 'adventure mode chapters (5 + epilogue)', 'https://dontstarve.wiki.gg/wiki/Adventure_Mode'),
    ('G085', 'Grand Theft Auto V', 'Open_World', 'Normal', 'Yes', 69, 'Medium', 'Yes', 'Low', 32.0, 1990556, 'story missions', 'https://www.sportskeeda.com/gta/gta-5-how-many-missions-game'),
    ('G086', 'Red Dead Redemption 2', 'Open_World', 'Normal', 'Yes', 104, 'High', 'Yes', 'Low', 50.5, 733542, 'story missions', 'https://stevivor.com/guides/many-chapters-missions-red-dead-redemption-2'),
    ('G087', 'Horizon Zero Dawn - Complete Edition', 'Open_World', 'Normal', 'Yes', 23, 'High', 'Yes', 'Medium', 29.3, 125197, 'main story missions', 'https://expertbeacon.com/how-many-levels-is-horizon-zero-dawn/'),
    ('G088', 'Hogwarts Legacy', 'Open_World', 'Normal', 'Yes', 42, 'High', 'Yes', 'Medium', 26.7, 321395, 'main quests', 'https://www.ginx.tv/en/?p=42397'),
    ('G089', "Marvel's Spider-Man: Game of the Year Edition", 'Open_World', 'Normal', 'Yes', 41, 'High', 'Yes', 'Medium', 17.9, 112392, 'main missions', 'https://www.gamepressure.com/marvels-spider-man/main-missions/z0b419'),
    ('G090', 'Ghost of Tsushima', 'Open_World', 'Normal', 'Yes', 26, 'High', 'Yes', 'Medium', 25.1, 65115, 'main tales', 'https://www.gamepressure.com/ghost-of-tsushima/all-main-tales-list/zfd6cb'),
    ('G091', 'Batman: Arkham Knight', 'Open_World', 'Normal', 'Yes', 36, 'High', 'Yes', 'Medium', 17.0, 140048, 'campaign walkthrough chapters', 'https://www.gamerguides.com/batman-arkham-knight/guide/walkthrough/campaign-walkthrough/countdown-to-knightfall-free-roam'),
    ('G092', 'Metal Gear Solid V: The Phantom Pain', 'Open_World', 'Normal', 'Yes', 51, 'High', 'Yes', 'Medium', 45.6, 99922, 'main missions', 'https://www.gamerevolution.com/guides/68911-metal-gear-solid-v-the-phantom-pain-full-mission-and-episode-list-no-spoilers'),
    ('G093', 'Mafia: Definitive Edition', 'Open_World', 'Normal', 'Yes', 20, 'Medium', 'Yes', 'Low', 10.6, 91793, 'chapters', 'https://stevivor.com/guides/many-chapters-mafia-definitive-edition'),
    ('G094', 'Watch Dogs 2', 'Open_World', 'Normal', 'Yes', 15, 'High', 'Yes', 'Medium', 19.4, 82379, 'main operations', 'https://www.itechguides.com/watch-dogs-2-how-many-main-operations-are-there/'),
    ('G095', 'Far Cry 3', 'Open_World', 'Normal', 'Yes', 39, 'High', 'Yes', 'Medium', 15.8, 114019, 'main missions', 'https://www.gamepressure.com/farcry3/main-missions/zb44b1'),
    ('G096', 'Dying Light', 'Open_World', 'Normal', 'Yes', 15, 'High', 'Yes', 'Medium', 18.0, 457632, 'main story quests', 'https://dyinglight.wiki.gg/wiki/Quests_(Dying_Light)'),
    ('G097', 'Middle-Earth: Shadow of Mordor', 'Open_World', 'Normal', 'Yes', 21, 'High', 'Yes', 'Medium', 15.8, 90715, 'main missions', 'https://www.gamepressure.com/shadowofmordor/main-missions/z669be'),
    ('G098', 'Mafia II', 'Open_World', 'Normal', 'Yes', 15, 'Medium', 'Yes', 'Low', 12.1, 54997, 'chapters', 'https://www.goodnovel.com/qa/many-chapters-mafia-2'),
    ('G099', "Assassin's Creed II", 'Open_World', 'Normal', 'Yes', 14, 'High', 'Yes', 'Medium', 19.2, 54646, 'sequences', 'https://www.gamepur.com/guides/assassins-creed-2-how-many-sequences-are-in-ac2'),
    ('G100', 'Sleeping Dogs: Definitive Edition', 'Open_World', 'Normal', 'Yes', 28, 'Medium', 'Yes', 'Low', 14.3, 69029, 'story missions', 'https://www.gamesradar.com/sleeping-dogs-story-missions-guide/'),
]
games = pd.DataFrame(CATALOGUE, columns=["Game_ID", "Game_Name", "Game_Genre", "Game_Difficulty", "Open_World", "Mission_Count",
                                         "Main_Story_Complexity", "Side_Quest_Availability", "Puzzle_Intensity", "Typical_Hours", "Reviews", "Mission_Unit", "Source"])
N_GAMES = len(games)

LEVELS = np.array(["Low", "Medium", "High"])
GAME_DIFFS = ["Easy", "Normal", "Hard", "Very_Hard"]
COMBAT_BY_GENRE = {"Action": 1.0, "Survival": 1.0, "RPG": 0.6, "Open_World": 0.5, "Strategy": 0.1, "Adventure": 0.1}

g_diff = games["Game_Difficulty"].map({d: i for i, d in enumerate(GAME_DIFFS)}).values
g_open = (games["Open_World"] == "Yes").astype(int).values
g_side = (games["Side_Quest_Availability"] == "Yes").astype(int).values
g_complex = games["Main_Story_Complexity"].map({"Low": 0, "Medium": 1, "High": 2}).values
g_puzzle = games["Puzzle_Intensity"].map({"Low": 0, "Medium": 1, "High": 2}).values
g_missions = games["Mission_Count"].values
g_hours = games["Typical_Hours"].values                                  # real typical main-story hours
g_combat = games["Game_Genre"].map(COMBAT_BY_GENRE).values
g_early_len = np.exp(rng.normal(0, 0.30, N_GAMES)).clip(0.5, 1.8)         # how long the early missions are
g_front_load = np.exp(rng.normal(0, 0.40, N_GAMES)).clip(0.4, 2.5)        # how much story the first 2 hours cover
popularity = games["Reviews"].values.astype(float) ** 0.6                 # popular real games are played more often

# -------------------------------------------------------------------------------------------------
# 2. SYNTHETIC PLAYERS (their profile never changes between their games)
# -------------------------------------------------------------------------------------------------
EXPERIENCE = np.array(["Beginner", "Intermediate", "Advanced", "Expert"])
PLAYSTYLES = np.array(["Explorer", "Completionist", "Speedrunner", "Story_Focused", "Balanced"])
PLAYER_DIFFS = np.array(["Easy", "Normal", "Hard"])

exp_idx = rng.choice(4, size=N_PLAYERS, p=[0.25, 0.35, 0.28, 0.12])
skill = np.array([-1.0, -0.25, 0.5, 1.25])[exp_idx] + rng.normal(0, 0.45, N_PLAYERS)
years = np.round(rng.uniform(np.array([0.2, 2, 5, 10])[exp_idx], np.array([2, 6, 12, 25])[exp_idx]), 1)

style_probs = np.array([[0.22, 0.14, 0.03, 0.35, 0.26], [0.22, 0.20, 0.07, 0.25, 0.26],
                        [0.22, 0.22, 0.15, 0.18, 0.23], [0.18, 0.22, 0.25, 0.12, 0.23]])
style_idx = np.array([rng.choice(5, p=style_probs[e]) for e in exp_idx])
diff_probs = np.array([[0.60, 0.38, 0.02], [0.20, 0.62, 0.18], [0.05, 0.50, 0.45], [0.02, 0.28, 0.70]])
pref_diff_idx = np.array([rng.choice(3, p=diff_probs[e]) for e in exp_idx])

thoroughness = np.array([0.7, 1.0, -1.0, -0.1, 0.2])[style_idx] + rng.normal(0, 0.30, N_PLAYERS)
daily_hours_base = np.exp(rng.normal(np.log(1.6) + 0.10 * exp_idx, 0.50, N_PLAYERS)).clip(0.3, 9.0)
sessions_base = rng.poisson(3 + 1.3 * daily_hours_base).clip(1, 14)

# -------------------------------------------------------------------------------------------------
# 3. WHO PLAYS WHICH GAMES (uneven: some players try 1 game, others 15+; some games are far more popular)
# -------------------------------------------------------------------------------------------------
counts = (1 + rng.negative_binomial(2, 2 / 6, size=N_PLAYERS)).clip(1, 20)
gap = N_RECORDS - counts.sum()
while gap != 0:
    i = rng.integers(0, N_PLAYERS)
    step = 1 if gap > 0 else -1
    if 1 <= counts[i] + step <= 20:
        counts[i] += step
        gap -= step

boost = {"Explorer": {"Open_World": 1.6, "Adventure": 1.5, "RPG": 1.3}, "Completionist": {"RPG": 1.5, "Open_World": 1.4},
         "Speedrunner": {"Action": 1.5, "Strategy": 1.3}, "Story_Focused": {"RPG": 1.6, "Adventure": 1.6}, "Balanced": {}}
genre_of_game = games["Game_Genre"].values

player_rows, game_rows = [], []
for p in range(N_PLAYERS):
    b = boost[PLAYSTYLES[style_idx[p]]]
    taste = {g: b.get(g, 1.0) * np.exp(rng.normal(0, 0.5)) for g in COMBAT_BY_GENRE}
    w = popularity * np.array([taste[g] for g in genre_of_game])
    chosen = rng.choice(N_GAMES, size=counts[p], replace=False, p=w / w.sum())
    player_rows.extend([p] * counts[p])
    game_rows.extend(chosen.tolist())

pi, gi = np.array(player_rows), np.array(game_rows)
n = len(pi)

# -------------------------------------------------------------------------------------------------
# 4. PLAYER-GAME LATENT FACTORS AND COMPLETION TIME
# -------------------------------------------------------------------------------------------------
s, thorough = skill[pi], thoroughness[pi]
style = style_idx[pi]
explorer, completionist = (style == 0).astype(float), (style == 1).astype(float)
speedrunner, story_focused = (style == 2).astype(float), (style == 3).astype(float)
diff_g, open_g, side_g, comp_g, puz_g, miss_g = g_diff[gi], g_open[gi], g_side[gi], g_complex[gi], g_puzzle[gi], g_missions[gi]

affinity, engagement = rng.normal(0, 1, n), rng.normal(0, 1, n)       # hidden: genre affinity and distraction level
pain = diff_g - (pref_diff_idx[pi] + 0.45 * s)                          # how much harder the game is than the player is comfortable with
pain_up, pain_down = np.clip(pain, 0, 3), np.clip(-pain, 0, 2)
t_eff = thorough + 0.25 * side_g * (thorough > 0) + 0.15 * open_g * (thorough > 0)
daily_hours = np.round((daily_hours_base[pi] * np.exp(rng.normal(0, 0.12, n))).clip(0.3, 10.0), 1)
sessions = np.clip(sessions_base[pi] + rng.integers(-1, 2, n), 1, 14)

# log speed multiplier (positive = slower than the typical player of this game)
L = (-0.20 * np.tanh(1.1 * s) + 0.17 * t_eff + 0.10 * pain_up + 0.035 * pain_up ** 2 - 0.04 * pain_down
     + 0.12 * explorer * open_g + 0.10 * completionist * side_g - 0.08 * speedrunner * side_g
     + 0.05 * story_focused * (comp_g == 2) - 0.07 * affinity + 0.07 * engagement - 0.03 * np.log(daily_hours / 1.6))
L = L - pd.Series(L).groupby(gi).transform('median').values              # each game's median player takes about its real typical hours


noise = rng.normal(0, 1, n) * (0.10 + 0.04 * diff_g + 0.03 * comp_g)
delay = np.where(rng.random(n) < 0.05, rng.uniform(1.15, 1.8, n), 1.0)  # occasional long breaks / getting stuck
completion = (g_hours[gi] * np.exp(L + noise) * delay).clip(2.5, 400)

# -------------------------------------------------------------------------------------------------
# 5. BEHAVIOUR IN THE FIRST TWO HOURS (noisy signals of the hidden traits)
# -------------------------------------------------------------------------------------------------
exploration = (24 + 17 * t_eff + 11 * open_g + 4 * side_g + 3.5 * puz_g + 4 * engagement + rng.normal(0, 9, n)).clip(2, 98)
death_rate = np.exp(0.35 + 0.42 * pain_up + 0.22 * diff_g - 0.38 * np.tanh(s) + 0.25 * g_combat[gi] + 0.10 * exploration / 100 + 0.10 * engagement)
deaths = rng.poisson(death_rate * rng.gamma(2.0, 0.5, n)).clip(0, 80)
retries = rng.poisson(0.55 * deaths + 0.5 + 1.1 * puz_g * (1 - 0.25 * np.tanh(s))).clip(0, 100)
combat_eff = (52 + 17 * np.tanh(s) - 5.5 * diff_g + 3 * g_combat[gi] - 2.5 * pain_up + rng.normal(0, 8, n)).clip(5, 98)
puzzle_time = (np.array([3.0, 9.0, 20.0])[puz_g] * np.exp(-0.30 * np.tanh(s) + 0.10 * pain_up + rng.normal(0, 0.35, n))).clip(0.5, 75)
side_quests = np.where(side_g == 1, rng.poisson(0.2 + 0.035 * exploration + 0.5 * np.maximum(t_eff, 0)).clip(0, 8), 0)
collectibles = rng.poisson(0.5 + 0.12 * exploration * (1 + 0.5 * open_g) + 1.5 * np.maximum(t_eff, 0)).clip(0, 60)

mission_len = (0.6 * (g_hours[gi] * 60 / miss_g) * g_early_len[gi] * np.exp(0.55 * L + rng.normal(0, 0.28, n))).clip(3, 1500)
mission_share = np.clip(0.70 - 0.0022 * exploration + rng.normal(0, 0.07, n), 0.25, 0.92)
mission_minutes = np.clip(mission_share * 120 - 0.5 * puzzle_time, 20, 110)
missions_done = np.minimum(np.floor(mission_minutes / mission_len).astype(int), np.minimum(miss_g, 15))   # opening missions are shorter than average; long acts -> often 0 in 2 hours
avg_mission_min = mission_minutes / np.maximum(missions_done, 1)       # 0 finished -> minutes spent on the unfinished first mission

story_share = np.clip(0.55 - 0.0035 * (exploration - 25) + rng.normal(0, 0.18, n), 0.12, 0.88)
progress_by_time = 100 * 2 * story_share * g_front_load[gi] / completion
progress_by_missions = 100 * (mission_minutes / mission_len) / miss_g * np.exp(rng.normal(0, 0.45, n))  # partial missions count too
progress = (0.35 * progress_by_time + 0.65 * progress_by_missions).clip(0.3, 70)

# -------------------------------------------------------------------------------------------------
# 6. CLEAN DATASET (ground truth)
# -------------------------------------------------------------------------------------------------
clean = pd.DataFrame({
    "Player_ID": [f"SYN_P{p + 1:05d}" for p in pi],
    "Gaming_Experience": EXPERIENCE[exp_idx[pi]],
    "Years_Of_Experience": years[pi],
    "Preferred_Playstyle": PLAYSTYLES[style_idx[pi]],
    "Preferred_Difficulty": PLAYER_DIFFS[pref_diff_idx[pi]],
    "Game_ID": games["Game_ID"].values[gi],
    "Game_Name": games["Game_Name"].values[gi],
    "Game_Genre": games["Game_Genre"].values[gi],
    "Game_Difficulty": games["Game_Difficulty"].values[gi],
    "Open_World": games["Open_World"].values[gi],
    "Mission_Count": miss_g,
    "Main_Story_Complexity": games["Main_Story_Complexity"].values[gi],
    "Side_Quest_Availability": games["Side_Quest_Availability"].values[gi],
    "Puzzle_Intensity": games["Puzzle_Intensity"].values[gi],
    "Exploration_Percentage": np.round(exploration, 1),
    "Death_Count": deaths.astype(int),
    "Retry_Count": retries.astype(int),
    "Side_Quests_Completed": side_quests.astype(int),
    "Missions_Completed": missions_done,
    "Average_Mission_Time_Minutes": np.round(avg_mission_min, 1),
    "Collectibles_Found": collectibles.astype(int),
    "Combat_Efficiency": np.round(combat_eff, 1),
    "Puzzle_Solving_Time_Minutes": np.round(puzzle_time, 1),
    "Average_Daily_Gaming_Hours": daily_hours,
    "Sessions_Per_Week": sessions.astype(int),
    "Main_Story_Progress_Percentage": np.round(progress, 1),
    "Completion_Time_Hours": np.round(completion, 1),
})
clean = clean.sort_values(["Player_ID", "Game_ID"]).reset_index(drop=True)
clean.to_csv(OUT_DIR / "gaming_player_completion_dataset_clean.csv", index=False)
games.drop(columns=["Reviews"]).rename(columns={"Typical_Hours": "Typical_Main_Story_Hours"}).to_csv(OUT_DIR / "game_catalogue.csv", index=False)

# =================================================================================================
# 7. REAL-WORLD MESS LAYER  (separate random generator; the clean data above never changes)
# =================================================================================================
mrng = np.random.default_rng(2024)
m = clean.copy()
N = len(m)


def pick(rate):
    # True for a random share of rows (rate can be a single number or one number per row)
    return mrng.random(N) < rate


# ---- 7.1 impossible values (sensor glitches, typing mistakes, "not recorded" codes)
for col, rate in [("Death_Count", 0.0025), ("Retry_Count", 0.002)]:
    m.loc[pick(rate), col] = -1
for col, rate, low, high in [("Exploration_Percentage", 0.0025, 100.5, 130), ("Combat_Efficiency", 0.0015, 100.5, 125),
                             ("Main_Story_Progress_Percentage", 0.001, 100.5, 140)]:
    hit = pick(rate)
    m.loc[hit, col] = np.round(mrng.uniform(low, high, hit.sum()), 1)
hit = pick(0.0015)
m.loc[hit, "Completion_Time_Hours"] = np.where(mrng.random(hit.sum()) < 0.5, 0.0, -np.round(mrng.uniform(1, 20, hit.sum()), 1))
hit = pick(0.0012)
m.loc[hit, "Completion_Time_Hours"] = np.round(m.loc[hit, "Completion_Time_Hours"] * 60, 1)      # minutes typed as hours
hit = pick(0.001)
m.loc[hit, "Completion_Time_Hours"] = np.round(m.loc[hit, "Completion_Time_Hours"] * 10, 1)      # extra digit
hit = pick(0.0015)
m.loc[hit, "Missions_Completed"] = m.loc[hit, "Mission_Count"] + mrng.integers(1, 6, hit.sum())
m.loc[pick(0.001), "Average_Mission_Time_Minutes"] = 0.0
hit = pick(0.0015)
m.loc[hit, "Years_Of_Experience"] = np.where(mrng.random(hit.sum()) < 0.5, -mrng.integers(1, 4, hit.sum()), 99.0)
hit = pick(0.0008)
m.loc[hit, "Puzzle_Solving_Time_Minutes"] = mrng.integers(150, 1000, hit.sum())
hit = pick(0.001)
m.loc[hit, "Average_Daily_Gaming_Hours"] = np.round(mrng.uniform(25, 48, hit.sum()), 1)
hit = pick(0.001)
m.loc[hit, "Sessions_Per_Week"] = mrng.integers(22, 40, hit.sum())

# ---- 7.2 missing values
random_missing = {"Exploration_Percentage": 0.02, "Death_Count": 0.015, "Retry_Count": 0.015, "Collectibles_Found": 0.025,
                  "Combat_Efficiency": 0.03, "Side_Quests_Completed": 0.015, "Average_Mission_Time_Minutes": 0.01,
                  "Main_Story_Progress_Percentage": 0.01, "Missions_Completed": 0.008,
                  "Years_Of_Experience": 0.03, "Preferred_Difficulty": 0.025, "Preferred_Playstyle": 0.025, "Gaming_Experience": 0.015,
                  "Main_Story_Complexity": 0.02, "Puzzle_Intensity": 0.02, "Side_Quest_Availability": 0.015, "Mission_Count": 0.01,
                  "Game_Name": 0.015, "Completion_Time_Hours": 0.004}
for col, rate in random_missing.items():
    m[col] = m[col].astype(object).where(~pick(rate), np.nan)

# self-reported habits are left blank more often by less experienced players
habit_missing = clean["Gaming_Experience"].map({"Beginner": 0.14, "Intermediate": 0.08, "Advanced": 0.04, "Expert": 0.04}).values
for col in ["Average_Daily_Gaming_Hours", "Sessions_Per_Week"]:
    m[col] = m[col].astype(object).where(~pick(habit_missing), np.nan)

# very long puzzle timers overflow and are not stored
puzzle_missing = np.where(clean["Puzzle_Solving_Time_Minutes"].values > 35, 0.15, 0.015)
m["Puzzle_Solving_Time_Minutes"] = m["Puzzle_Solving_Time_Minutes"].astype(object).where(~pick(puzzle_missing), np.nan)

# ---- 7.3 inconsistent labels (case, spaces, separators, abbreviations, typos)
YES_NO = {"Yes": ["yes", "YES", "Y", "y", "TRUE", "true", "1"], "No": ["no", "NO", "N", "n", "FALSE", "false", "0"]}
TYPOS = {"Beginner": ["Begginer", "Beginer"], "Intermediate": ["Intermedate", "Intermidiate"], "Advanced": ["Advance", "Advanced."],
         "Completionist": ["Complitionist"], "Story_Focused": ["Story Focussed"], "Speedrunner": ["Speed Runner", "Speed-runner"],
         "Strategy": ["Stratergy"], "Adventure": ["Adventrue"], "Survival": ["Survial"]}


def label_variants(label):
    if label in YES_NO:
        return YES_NO[label]
    variants = [label.lower(), label.upper(), f" {label}", f"{label} ", label.replace("_", " "), label.replace("_", "-"),
                label.replace("_", " ").lower(), label.replace("_", "")] + TYPOS.get(label, [])
    return [v for v in dict.fromkeys(variants) if v != label]


label_rates = {"Gaming_Experience": 0.05, "Preferred_Playstyle": 0.05, "Preferred_Difficulty": 0.04, "Game_Genre": 0.04, "Game_Difficulty": 0.05,
               "Open_World": 0.04, "Main_Story_Complexity": 0.04, "Side_Quest_Availability": 0.04, "Puzzle_Intensity": 0.04}
for col, rate in label_rates.items():
    values = m[col].copy()
    hit = pick(rate) & values.notna().values
    values[hit] = [mrng.choice(label_variants(v)) for v in values[hit]]
    m[col] = values

# game names: some typed in lower or upper case
for col_rate, change in [(0.02, str.lower), (0.01, str.upper)]:
    hit = pick(col_rate) & m["Game_Name"].notna().values
    m.loc[hit, "Game_Name"] = [change(v) for v in m.loc[hit, "Game_Name"]]

# ---- 7.4 numbers stored as text in some records
years_text = pick(0.004) & m["Years_Of_Experience"].notna().values
hours_comma = pick(0.003) & m["Average_Daily_Gaming_Hours"].notna().values
target_text = pick(0.002) & m["Completion_Time_Hours"].notna().values
m.loc[years_text, "Years_Of_Experience"] = [f"{v} years" for v in clean.loc[years_text, "Years_Of_Experience"]]
m.loc[hours_comma, "Average_Daily_Gaming_Hours"] = [str(v).replace(".", ",") for v in clean.loc[hours_comma, "Average_Daily_Gaming_Hours"]]
m.loc[target_text, "Completion_Time_Hours"] = [f"{v}h" if mrng.random() < 0.5 else f"{v} hrs" for v in clean.loc[target_text, "Completion_Time_Hours"]]

# ---- 7.5 stray spaces inside IDs and names
for col in ["Player_ID", "Game_ID", "Game_Name"]:
    hit = pick(0.004) & m[col].notna().values
    m.loc[hit, col] = [(" " + v) if mrng.random() < 0.5 else (v + " ") for v in m.loc[hit, col]]

# ---- 7.6 duplicates: exact copies (double ingestion) and near-duplicates (same experience logged twice with small differences)
exact_rows = mrng.choice(N, size=int(0.015 * N), replace=False)
exact = m.iloc[exact_rows].copy()

near_rows = mrng.choice(np.setdiff1d(np.arange(N), exact_rows), size=int(0.010 * N), replace=False)
near = clean.iloc[near_rows].copy()
for col in ["Exploration_Percentage", "Combat_Efficiency", "Puzzle_Solving_Time_Minutes", "Average_Mission_Time_Minutes",
            "Main_Story_Progress_Percentage", "Completion_Time_Hours"]:
    near[col] = np.round(near[col] * mrng.normal(1.0, 0.03, len(near)), 1)
near["Collectibles_Found"] = np.maximum(0, near["Collectibles_Found"] + mrng.integers(-1, 2, len(near)))

messy = pd.concat([m, exact, near], ignore_index=True)
messy = messy.sample(frac=1.0, random_state=7).reset_index(drop=True)      # real extracts are not sorted
messy.to_csv(OUT_DIR / "gaming_player_completion_dataset.csv", index=False)

print(f"clean dataset : {clean.shape[0]:,} rows x {clean.shape[1]} columns")
print(f"messy dataset : {messy.shape[0]:,} rows x {messy.shape[1]} columns "
      f"({len(exact):,} exact duplicate rows + {len(near):,} near-duplicate rows added)")
print(f"players: {clean['Player_ID'].nunique():,} | games: {clean['Game_ID'].nunique()} | records per player: min {counts.min()} max {counts.max()} mean {counts.mean():.1f}")
