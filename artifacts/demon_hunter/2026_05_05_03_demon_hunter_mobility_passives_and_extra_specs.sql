-- Adds the next retail-style Demon Hunter pass: core mobility/passives plus Havoc and Vengeance follow-up abilities.
-- Requires the matching client MPQ/DBC rebuild so the custom spell IDs resolve in the client.

USE acore_world;

DELETE FROM `playercreateinfo_spell_custom`
WHERE `classmask` = 512
  AND `Spell` BETWEEN 910231 AND 910244;

INSERT INTO `playercreateinfo_spell_custom` (`racemask`, `classmask`, `Spell`, `Note`) VALUES
(520, 512, 910231, 'Demon Hunter - Glide'),
(520, 512, 910232, 'Demon Hunter - Double Jump'),
(520, 512, 910233, 'Demon Hunter - Reverse Magic'),
(520, 512, 910234, 'Demon Hunter - Shattered Souls'),
(520, 512, 910235, 'Demon Hunter - Chaos Brand'),
(520, 512, 910236, 'Demon Hunter - Annihilation'),
(520, 512, 910237, 'Demon Hunter - Glaive Tempest'),
(520, 512, 910238, 'Demon Hunter - Fel Barrage'),
(520, 512, 910239, 'Demon Hunter - Demonic'),
(520, 512, 910240, 'Demon Hunter - Netherwalk'),
(520, 512, 910241, 'Demon Hunter - Fracture'),
(520, 512, 910242, 'Demon Hunter - Spirit Bomb'),
(520, 512, 910243, 'Demon Hunter - Soul Barrier'),
(520, 512, 910244, 'Demon Hunter - Soul Carver');

DELETE FROM `playercreateinfo_action`
WHERE `class` = 10
  AND `race` IN (4, 10)
  AND (`button` BETWEEN 32 AND 45 OR `action` BETWEEN 910231 AND 910244);

INSERT INTO `playercreateinfo_action` (`race`, `class`, `button`, `action`, `type`) VALUES
(4, 10, 32, 910231, 0),
(4, 10, 33, 910232, 0),
(4, 10, 34, 910233, 0),
(4, 10, 35, 910234, 0),
(4, 10, 36, 910235, 0),
(4, 10, 37, 910236, 0),
(4, 10, 38, 910237, 0),
(4, 10, 39, 910238, 0),
(4, 10, 40, 910239, 0),
(4, 10, 41, 910240, 0),
(4, 10, 42, 910241, 0),
(4, 10, 43, 910242, 0),
(4, 10, 44, 910243, 0),
(4, 10, 45, 910244, 0),
(10, 10, 32, 910231, 0),
(10, 10, 33, 910232, 0),
(10, 10, 34, 910233, 0),
(10, 10, 35, 910234, 0),
(10, 10, 36, 910235, 0),
(10, 10, 37, 910236, 0),
(10, 10, 38, 910237, 0),
(10, 10, 39, 910238, 0),
(10, 10, 40, 910239, 0),
(10, 10, 41, 910240, 0),
(10, 10, 42, 910241, 0),
(10, 10, 43, 910242, 0),
(10, 10, 44, 910243, 0),
(10, 10, 45, 910244, 0);

USE acore_characters;

INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910231, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910232, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910233, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910234, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910235, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910236, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910237, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910238, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910239, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910240, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910241, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910242, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910243, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910244, 1 FROM `characters` WHERE `class` = 10;

DELETE ca
FROM `character_action` ca
JOIN `characters` c ON c.`guid` = ca.`guid`
WHERE c.`class` = 10
  AND (ca.`button` BETWEEN 32 AND 45 OR ca.`action` BETWEEN 910231 AND 910244);

INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 32, 910231, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 33, 910232, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 34, 910233, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 35, 910234, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 36, 910235, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 37, 910236, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 38, 910237, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 39, 910238, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 40, 910239, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 41, 910240, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 42, 910241, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 43, 910242, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 44, 910243, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 45, 910244, 0 FROM `characters` WHERE `class` = 10;
