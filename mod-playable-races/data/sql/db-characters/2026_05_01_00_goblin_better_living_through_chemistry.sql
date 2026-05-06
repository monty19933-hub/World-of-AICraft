-- Teach Better Living Through Chemistry to existing Goblin characters.

SET @GOBLIN := 9;
SET @SPELL_BETTER_LIVING := 69045;

INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT `guid`, @SPELL_BETTER_LIVING, 1
FROM `characters`
WHERE `race` = @GOBLIN;
