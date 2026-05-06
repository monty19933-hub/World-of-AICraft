-- Syncs existing Demon Hunters after the spellbook tab and Fel Rush safety pass.
-- Apply after 2026_05_05_03_demon_hunter_mobility_passives_and_extra_specs.sql
-- and install the matching client MPQ/DBC rebuild.

USE acore_world;

DELETE FROM `playercreateinfo_skills`
WHERE `classMask` = 512
  AND `skill` IN (38, 39, 253);

DELETE FROM `playercreateinfo_skills`
WHERE `classMask` = 512
  AND `skill` IN (910, 911, 912);

INSERT INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(520, 512, 910, 0, 'Demon Hunter - Class'),
(520, 512, 911, 0, 'Demon Hunter - Havoc'),
(520, 512, 912, 0, 'Demon Hunter - Vengeance');

USE acore_characters;

DELETE ck
FROM `character_skills` ck
JOIN `characters` c ON c.`guid` = ck.`guid`
WHERE c.`class` = 10
  AND ck.`skill` IN (38, 39, 253);

INSERT IGNORE INTO `character_skills` (`guid`, `skill`, `value`, `max`)
SELECT `guid`, 910, 5, 5 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_skills` (`guid`, `skill`, `value`, `max`)
SELECT `guid`, 911, 5, 5 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_skills` (`guid`, `skill`, `value`, `max`)
SELECT `guid`, 912, 5, 5 FROM `characters` WHERE `class` = 10;

CREATE TEMPORARY TABLE `tmp_demon_hunter_spell_sync` (`spell` int unsigned NOT NULL PRIMARY KEY);
INSERT INTO `tmp_demon_hunter_spell_sync` (`spell`) VALUES
(910201), (910202), (910203), (910204), (910205), (910206), (910207), (910208),
(910209), (910210), (910211), (910212), (910213), (910214), (910215), (910216),
(910217), (910218), (910219), (910220), (910221), (910222), (910223), (910224),
(910225), (910226), (910227), (910228), (910229), (910230), (910231), (910232),
(910233), (910234), (910235), (910236), (910237), (910238), (910239), (910240),
(910241), (910242), (910243), (910244);

INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT c.`guid`, s.`spell`, 1
FROM `characters` c
CROSS JOIN `tmp_demon_hunter_spell_sync` s
WHERE c.`class` = 10;

DROP TEMPORARY TABLE `tmp_demon_hunter_spell_sync`;
