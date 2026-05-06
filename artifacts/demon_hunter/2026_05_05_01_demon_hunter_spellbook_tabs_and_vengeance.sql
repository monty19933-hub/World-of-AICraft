-- Adds retail-style Demon Hunter spellbook tabs and the next class/Vengeance spell pass.
-- Apply after the base Demon Hunter playercreate and spellbook SQL files.

USE acore_world;

DELETE FROM `playercreateinfo_spell_custom`
WHERE `classmask` = 512
  AND `Spell` IN (
      910213, 910214, 910215, 910216, 910217,
      910218, 910219, 910220, 910221, 910222
  );

INSERT INTO `playercreateinfo_spell_custom` (`racemask`, `classmask`, `Spell`, `Note`) VALUES
(520, 512, 910213, 'Demon Hunter - Consume Magic'),
(520, 512, 910214, 'Demon Hunter - Disrupt'),
(520, 512, 910215, 'Demon Hunter - Imprison'),
(520, 512, 910216, 'Demon Hunter - Torment'),
(520, 512, 910217, 'Demon Hunter - Shear'),
(520, 512, 910218, 'Demon Hunter - Soul Cleave'),
(520, 512, 910219, 'Demon Hunter - Infernal Strike'),
(520, 512, 910220, 'Demon Hunter - Demon Spikes'),
(520, 512, 910221, 'Demon Hunter - Fiery Brand'),
(520, 512, 910222, 'Demon Hunter - Sigil of Flame');

DELETE FROM `playercreateinfo_skills`
WHERE `classMask` = 512
  AND `skill` IN (38, 39, 253, 910, 911, 912);

INSERT INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(520, 512, 910, 0, 'Demon Hunter - Class'),
(520, 512, 911, 0, 'Demon Hunter - Havoc'),
(520, 512, 912, 0, 'Demon Hunter - Vengeance');

DELETE FROM `playercreateinfo_action`
WHERE `class` = 10
  AND `race` IN (4, 10)
  AND (`button` BETWEEN 14 AND 23 OR `action` IN (
      910213, 910214, 910215, 910216, 910217,
      910218, 910219, 910220, 910221, 910222
  ));

INSERT INTO `playercreateinfo_action` (`race`, `class`, `button`, `action`, `type`) VALUES
(4, 10, 14, 910213, 0),
(4, 10, 15, 910214, 0),
(4, 10, 16, 910215, 0),
(4, 10, 17, 910216, 0),
(4, 10, 18, 910217, 0),
(4, 10, 19, 910218, 0),
(4, 10, 20, 910219, 0),
(4, 10, 21, 910220, 0),
(4, 10, 22, 910221, 0),
(4, 10, 23, 910222, 0),
(10, 10, 14, 910213, 0),
(10, 10, 15, 910214, 0),
(10, 10, 16, 910215, 0),
(10, 10, 17, 910216, 0),
(10, 10, 18, 910217, 0),
(10, 10, 19, 910218, 0),
(10, 10, 20, 910219, 0),
(10, 10, 21, 910220, 0),
(10, 10, 22, 910221, 0),
(10, 10, 23, 910222, 0);

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

INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910213, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910214, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910215, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910216, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910217, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910218, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910219, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910220, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910221, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910222, 1 FROM `characters` WHERE `class` = 10;

DELETE ca
FROM `character_action` ca
JOIN `characters` c ON c.`guid` = ca.`guid`
WHERE c.`class` = 10
  AND (ca.`button` BETWEEN 14 AND 23 OR ca.`action` IN (
      910213, 910214, 910215, 910216, 910217,
      910218, 910219, 910220, 910221, 910222
  ));

INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 14, 910213, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 15, 910214, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 16, 910215, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 17, 910216, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 18, 910217, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 19, 910218, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 20, 910219, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 21, 910220, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 22, 910221, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 23, 910222, 0 FROM `characters` WHERE `class` = 10;
