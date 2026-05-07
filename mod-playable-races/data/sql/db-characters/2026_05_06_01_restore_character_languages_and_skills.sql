-- Backfill missing startup skills on existing characters.
-- This repairs characters that were created or reborn while language/default
-- skill rows were missing or seeded at rank 0.

USE acore_characters;

CREATE TEMPORARY TABLE `tmp_starting_languages`
(
    `race` tinyint unsigned NOT NULL,
    `skill` smallint unsigned NOT NULL,
    `comment` varchar(64) NOT NULL,
    PRIMARY KEY (`race`, `skill`)
);

INSERT INTO `tmp_starting_languages` (`race`, `skill`, `comment`) VALUES
(1, 98, 'Language: Common'),
(2, 109, 'Language: Orcish'),
(3, 98, 'Language: Common'),
(3, 111, 'Language: Dwarven'),
(4, 98, 'Language: Common'),
(4, 113, 'Language: Darnassian'),
(5, 109, 'Language: Orcish'),
(5, 673, 'Language: Gutterspeak'),
(6, 109, 'Language: Orcish'),
(6, 115, 'Language: Taurahe'),
(7, 98, 'Language: Common'),
(7, 313, 'Language: Gnomish'),
(8, 109, 'Language: Orcish'),
(8, 315, 'Language: Troll'),
(9, 109, 'Language: Orcish'),
(10, 109, 'Language: Orcish'),
(10, 137, 'Language: Thalassian'),
(11, 98, 'Language: Common'),
(11, 759, 'Language: Draenei'),
(12, 98, 'Language: Common'),
(22, 98, 'Language: Common');

INSERT INTO `character_skills` (`guid`, `skill`, `value`, `max`)
SELECT c.`guid`, l.`skill`, 300, 300
FROM `characters` c
JOIN `tmp_starting_languages` l ON l.`race` = c.`race`
ON DUPLICATE KEY UPDATE
    `value` = GREATEST(`value`, VALUES(`value`)),
    `max` = GREATEST(`max`, VALUES(`max`));

DROP TEMPORARY TABLE `tmp_starting_languages`;

CREATE TEMPORARY TABLE `tmp_playercreateinfo_skill_backfill`
(
    `guid` int unsigned NOT NULL,
    `skill` smallint unsigned NOT NULL,
    `value` smallint unsigned NOT NULL,
    `max` smallint unsigned NOT NULL,
    PRIMARY KEY (`guid`, `skill`)
);

INSERT INTO `tmp_playercreateinfo_skill_backfill` (`guid`, `skill`, `value`, `max`)
SELECT
    c.`guid`,
    s.`skill`,
    MAX(CASE
        WHEN s.`rank` > 0 THEN s.`rank`
        ELSE 1
    END) AS `value`,
    MAX(CASE
        WHEN s.`rank` > 0 THEN s.`rank`
        ELSE GREATEST(5, LEAST(450, c.`level` * 5))
    END) AS `max`
FROM `characters` c
JOIN `acore_world`.`playercreateinfo_skills` s
  ON (s.`raceMask` = 0 OR (s.`raceMask` & (1 << (c.`race` - 1))) <> 0)
 AND (s.`classMask` = 0 OR (s.`classMask` & (1 << (c.`class` - 1))) <> 0)
WHERE c.`race` BETWEEN 1 AND 22
GROUP BY c.`guid`, s.`skill`;

INSERT INTO `character_skills` (`guid`, `skill`, `value`, `max`)
SELECT `guid`, `skill`, `value`, `max`
FROM `tmp_playercreateinfo_skill_backfill`
ON DUPLICATE KEY UPDATE
    `value` = GREATEST(`value`, VALUES(`value`)),
    `max` = GREATEST(`max`, VALUES(`max`));

DROP TEMPORARY TABLE `tmp_playercreateinfo_skill_backfill`;
