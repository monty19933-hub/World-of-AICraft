-- Extends Demon Hunter startup/known spells after the spellbook tab pass.

USE acore_world;

DELETE FROM `playercreateinfo_spell_custom`
WHERE `classmask` = 512
  AND `Spell` IN (910205, 910206, 910207, 910208, 910209, 910210, 910211, 910212);

INSERT INTO `playercreateinfo_spell_custom` (`racemask`, `classmask`, `Spell`, `Note`) VALUES
(520, 512, 910205, 'Demon Hunter - Eye Beam'),
(520, 512, 910206, 'Demon Hunter - Blade Dance'),
(520, 512, 910207, 'Demon Hunter - Immolation Aura'),
(520, 512, 910208, 'Demon Hunter - Vengeful Retreat'),
(520, 512, 910209, 'Demon Hunter - Blur'),
(520, 512, 910210, 'Demon Hunter - Metamorphosis'),
(520, 512, 910211, 'Demon Hunter - Spectral Sight'),
(520, 512, 910212, 'Demon Hunter - Chaos Nova');

DELETE FROM `playercreateinfo_action`
WHERE `class` = 10
  AND `race` IN (4, 10)
  AND (`button` BETWEEN 6 AND 13 OR `action` IN (910205, 910206, 910207, 910208, 910209, 910210, 910211, 910212));

INSERT INTO `playercreateinfo_action` (`race`, `class`, `button`, `action`, `type`) VALUES
(4, 10, 6, 910205, 0),
(4, 10, 7, 910206, 0),
(4, 10, 8, 910207, 0),
(4, 10, 9, 910208, 0),
(4, 10, 10, 910209, 0),
(4, 10, 11, 910210, 0),
(4, 10, 12, 910211, 0),
(4, 10, 13, 910212, 0),
(10, 10, 6, 910205, 0),
(10, 10, 7, 910206, 0),
(10, 10, 8, 910207, 0),
(10, 10, 9, 910208, 0),
(10, 10, 10, 910209, 0),
(10, 10, 11, 910210, 0),
(10, 10, 12, 910211, 0),
(10, 10, 13, 910212, 0);

USE acore_characters;

INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910205, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910206, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910207, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910208, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910209, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910210, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910211, 1 FROM `characters` WHERE `class` = 10;
INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, 910212, 1 FROM `characters` WHERE `class` = 10;

DELETE ca
FROM `character_action` ca
JOIN `characters` c ON c.`guid` = ca.`guid`
WHERE c.`class` = 10
  AND (ca.`button` BETWEEN 6 AND 13 OR ca.`action` IN (910205, 910206, 910207, 910208, 910209, 910210, 910211, 910212));

INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 6, 910205, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 7, 910206, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 8, 910207, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 9, 910208, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 10, 910209, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 11, 910210, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 12, 910211, 0 FROM `characters` WHERE `class` = 10;
INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT `guid`, 0, 13, 910212, 0 FROM `characters` WHERE `class` = 10;
