-- Adds the next retail-style Demon Hunter spell pass after the spellbook tab split.
-- Requires the matching client MPQ/DBC rebuild so the custom spell IDs resolve in the client.

USE acore_world;

DELETE FROM `playercreateinfo_spell_custom`
WHERE `classmask` = 512
  AND `Spell` IN (910223, 910224, 910225, 910226, 910227, 910228, 910229, 910230);

INSERT INTO `playercreateinfo_spell_custom` (`racemask`, `classmask`, `Spell`, `Note`) VALUES
(520, 512, 910223, 'Demon Hunter - Felblade'),
(520, 512, 910224, 'Demon Hunter - Death Sweep'),
(520, 512, 910225, 'Demon Hunter - Darkness'),
(520, 512, 910226, 'Demon Hunter - The Hunt'),
(520, 512, 910227, 'Demon Hunter - Fel Devastation'),
(520, 512, 910228, 'Demon Hunter - Sigil of Misery'),
(520, 512, 910229, 'Demon Hunter - Sigil of Silence'),
(520, 512, 910230, 'Demon Hunter - Sigil of Chains');

DELETE FROM `playercreateinfo_action`
WHERE `class` = 10
  AND `race` IN (4, 10)
  AND (`button` BETWEEN 24 AND 31 OR `action` IN (
      910223, 910224, 910225, 910226,
      910227, 910228, 910229, 910230
  ));

INSERT INTO `playercreateinfo_action` (`race`, `class`, `button`, `action`, `type`) VALUES
(4, 10, 24, 910223, 0),
(4, 10, 25, 910224, 0),
(4, 10, 26, 910225, 0),
(4, 10, 27, 910226, 0),
(4, 10, 28, 910227, 0),
(4, 10, 29, 910228, 0),
(4, 10, 30, 910229, 0),
(4, 10, 31, 910230, 0),
(10, 10, 24, 910223, 0),
(10, 10, 25, 910224, 0),
(10, 10, 26, 910225, 0),
(10, 10, 27, 910226, 0),
(10, 10, 28, 910227, 0),
(10, 10, 29, 910228, 0),
(10, 10, 30, 910229, 0),
(10, 10, 31, 910230, 0);

USE acore_characters;

INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910223, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910224, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910225, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910226, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910227, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910228, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910229, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910230, 1 FROM `characters` WHERE `class` = 10;

DELETE ca
FROM `character_action` ca
JOIN `characters` c ON c.`guid` = ca.`guid`
WHERE c.`class` = 10
  AND (ca.`button` BETWEEN 24 AND 31 OR ca.`action` IN (
      910223, 910224, 910225, 910226,
      910227, 910228, 910229, 910230
  ));

INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 24, 910223, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 25, 910224, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 26, 910225, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 27, 910226, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 28, 910227, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 29, 910228, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 30, 910229, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 31, 910230, 0 FROM `characters` WHERE `class` = 10;
