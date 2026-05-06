-- Playable Goblin/Worgen first pass for 3.3.5a.
-- Goblins use the Orc starting point. Worgen use the Human starting point.

SET @GOBLIN := 9;
SET @WORGEN := 12;
SET @OLD_WORGEN := 22;
SET @GOBLIN_MASK := 256;
SET @WORGEN_MASK := 2048;
SET @OLD_WORGEN_MASK := 2097152;

DELETE FROM playercreateinfo WHERE race IN (@GOBLIN, @WORGEN, @OLD_WORGEN);
DELETE FROM playercreateinfo_action WHERE race IN (@GOBLIN, @WORGEN, @OLD_WORGEN);
DELETE FROM playercreateinfo_item WHERE race IN (@GOBLIN, @WORGEN, @OLD_WORGEN);

INSERT INTO playercreateinfo (race, class, map, zone, position_x, position_y, position_z, orientation) VALUES
(@GOBLIN, 1, 1, 14, -618.518, -4251.67, 38.718, 0),
(@GOBLIN, 3, 1, 14, -618.518, -4251.67, 38.718, 0),
(@GOBLIN, 4, 1, 14, -618.518, -4251.67, 38.718, 0),
(@GOBLIN, 5, 1, 14, -618.518, -4251.67, 38.718, 0),
(@GOBLIN, 6, 1, 14, -618.518, -4251.67, 38.718, 0),
(@GOBLIN, 7, 1, 14, -618.518, -4251.67, 38.718, 0),
(@GOBLIN, 8, 1, 14, -618.518, -4251.67, 38.718, 0),
(@GOBLIN, 9, 1, 14, -618.518, -4251.67, 38.718, 0),
(@WORGEN, 1, 0, 12, -8949.95, -132.493, 83.5312, 0),
(@WORGEN, 3, 0, 12, -8949.95, -132.493, 83.5312, 0),
(@WORGEN, 4, 0, 12, -8949.95, -132.493, 83.5312, 0),
(@WORGEN, 5, 0, 12, -8949.95, -132.493, 83.5312, 0),
(@WORGEN, 6, 0, 12, -8949.95, -132.493, 83.5312, 0),
(@WORGEN, 8, 0, 12, -8949.95, -132.493, 83.5312, 0),
(@WORGEN, 9, 0, 12, -8949.95, -132.493, 83.5312, 0),
(@WORGEN, 11, 0, 12, -8949.95, -132.493, 83.5312, 0);

INSERT INTO playercreateinfo_action (race, class, button, action, type)
SELECT @GOBLIN, class, button, action, type FROM playercreateinfo_action WHERE race = 2 AND class IN (1,3,4,6,7,9)
UNION ALL SELECT @GOBLIN, 5, button, action, type FROM playercreateinfo_action WHERE race = 8 AND class = 5
UNION ALL SELECT @GOBLIN, 8, button, action, type FROM playercreateinfo_action WHERE race = 5 AND class = 8
UNION ALL SELECT @WORGEN, class, button, action, type FROM playercreateinfo_action WHERE race = 1 AND class IN (1,4,5,6,8,9)
UNION ALL SELECT @WORGEN, 3, button, action, type FROM playercreateinfo_action WHERE race = 4 AND class = 3
UNION ALL SELECT @WORGEN, 11, button, action, type FROM playercreateinfo_action WHERE race = 4 AND class = 11;

INSERT IGNORE INTO playercreateinfo_skills (raceMask, classMask, skill, `rank`, `comment`) VALUES
(@GOBLIN_MASK, 0, 109, 0, 'Language: Orcish'),
(@WORGEN_MASK, 0, 98, 0, 'Language: Common');

DELETE FROM playercreateinfo_spell_custom WHERE racemask IN (@GOBLIN_MASK, @WORGEN_MASK, @OLD_WORGEN_MASK);
INSERT INTO playercreateinfo_spell_custom (racemask, classmask, Spell, Note) VALUES
(@GOBLIN_MASK, 0, 69041, 'Goblin - Rocket Barrage'),
(@GOBLIN_MASK, 0, 69042, 'Goblin - Time is Money'),
(@GOBLIN_MASK, 0, 69044, 'Goblin - Best Deals Anywhere'),
(@GOBLIN_MASK, 0, 69045, 'Goblin - Better Living Through Chemistry'),
(@GOBLIN_MASK, 0, 69046, 'Goblin - Pack Hobgoblin'),
(@GOBLIN_MASK, 0, 69070, 'Goblin - Rocket Jump'),
(@WORGEN_MASK, 0, 68975, 'Worgen - Viciousness'),
(@WORGEN_MASK, 0, 68976, 'Worgen - Aberration'),
(@WORGEN_MASK, 0, 68978, 'Worgen - Flayer'),
(@WORGEN_MASK, 0, 68992, 'Worgen - Darkflight'),
(@WORGEN_MASK, 0, 68996, 'Worgen - Two Forms'),
(@WORGEN_MASK, 0, 87840, 'Worgen - Running Wild');

DELETE FROM player_race_stats WHERE Race IN (@GOBLIN, @WORGEN, @OLD_WORGEN);
INSERT INTO player_race_stats (Race, Strength, Agility, Stamina, Intellect, Spirit) VALUES
(@GOBLIN, -3, 2, 0, 3, -2),
(@WORGEN, 1, 1, 0, -1, -1);
