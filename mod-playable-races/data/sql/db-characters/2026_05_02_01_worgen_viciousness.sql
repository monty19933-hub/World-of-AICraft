-- Teach Viciousness to existing Worgen characters.

SET @WORGEN := 12;
SET @SPELL_VICIOUSNESS := 68975;

INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, @SPELL_VICIOUSNESS, 1
FROM `characters`
WHERE `race` = @WORGEN;
