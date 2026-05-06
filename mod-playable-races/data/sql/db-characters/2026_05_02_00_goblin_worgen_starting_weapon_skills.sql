-- Backfill missing starting weapon proficiencies onto existing Goblin/Worgen characters.

SET @GOBLIN := 9;
SET @WORGEN := 12;

INSERT IGNORE INTO `character_skills` (`guid`, `skill`, `value`, `max`)
SELECT `guid`, 45, 1, GREATEST(5, LEAST(450, `level` * 5))
FROM `characters`
WHERE `race` IN (@GOBLIN, @WORGEN) AND `class` = 3;

INSERT IGNORE INTO `character_skills` (`guid`, `skill`, `value`, `max`)
SELECT `guid`, 46, 1, GREATEST(5, LEAST(450, `level` * 5))
FROM `characters`
WHERE `race` IN (@GOBLIN, @WORGEN) AND `class` = 3;

INSERT IGNORE INTO `character_skills` (`guid`, `skill`, `value`, `max`)
SELECT `guid`, 226, 1, GREATEST(5, LEAST(450, `level` * 5))
FROM `characters`
WHERE `race` IN (@GOBLIN, @WORGEN) AND `class` = 3;

INSERT IGNORE INTO `character_skills` (`guid`, `skill`, `value`, `max`)
SELECT `guid`, 160, 1, GREATEST(5, LEAST(450, `level` * 5))
FROM `characters`
WHERE `race` IN (@GOBLIN, @WORGEN) AND `class` = 1;

INSERT IGNORE INTO `character_skills` (`guid`, `skill`, `value`, `max`)
SELECT `guid`, 173, 1, GREATEST(5, LEAST(450, `level` * 5))
FROM `characters`
WHERE `race` IN (@GOBLIN, @WORGEN) AND `class` IN (4, 9);
