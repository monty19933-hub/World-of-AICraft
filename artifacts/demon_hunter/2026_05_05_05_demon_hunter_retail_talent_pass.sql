-- Adds another retail-informed Demon Hunter spell pass and syncs existing characters.
-- Apply after 2026_05_05_04_demon_hunter_felrush_safety_spellbook_sync.sql
-- and install the matching client MPQ/DBC rebuild.

USE acore_world;

DELETE FROM `playercreateinfo_spell_custom`
WHERE `classmask` = 512
  AND `Spell` BETWEEN 910245 AND 910260;

INSERT INTO `playercreateinfo_spell_custom` (`racemask`, `classmask`, `Spell`, `Note`) VALUES
(520, 512, 910245, 'Demon Hunter - Demon Blades'),
(520, 512, 910246, 'Demon Hunter - Essence Break'),
(520, 512, 910247, 'Demon Hunter - Fel Eruption'),
(520, 512, 910248, 'Demon Hunter - Unbound Chaos'),
(520, 512, 910249, 'Demon Hunter - Momentum'),
(520, 512, 910250, 'Demon Hunter - Tactical Retreat'),
(520, 512, 910251, 'Demon Hunter - Burning Hatred'),
(520, 512, 910252, 'Demon Hunter - Reaver''s Glaive'),
(520, 512, 910253, 'Demon Hunter - Demonic Wards'),
(520, 512, 910254, 'Demon Hunter - Mastery: Fel Blood'),
(520, 512, 910255, 'Demon Hunter - Sigil of Spite'),
(520, 512, 910256, 'Demon Hunter - Elysian Decree'),
(520, 512, 910257, 'Demon Hunter - Frailty'),
(520, 512, 910258, 'Demon Hunter - Bulk Extraction'),
(520, 512, 910259, 'Demon Hunter - Charred Warblades'),
(520, 512, 910260, 'Demon Hunter - Demonsurge');

DELETE FROM `playercreateinfo_action`
WHERE `class` = 10
  AND `race` IN (4, 10)
  AND (`button` BETWEEN 46 AND 61 OR `action` BETWEEN 910245 AND 910260);

INSERT INTO `playercreateinfo_action` (`race`, `class`, `button`, `action`, `type`) VALUES
(4, 10, 46, 910245, 0),
(4, 10, 47, 910246, 0),
(4, 10, 48, 910247, 0),
(4, 10, 49, 910248, 0),
(4, 10, 50, 910249, 0),
(4, 10, 51, 910250, 0),
(4, 10, 52, 910251, 0),
(4, 10, 53, 910252, 0),
(4, 10, 54, 910253, 0),
(4, 10, 55, 910254, 0),
(4, 10, 56, 910255, 0),
(4, 10, 57, 910256, 0),
(4, 10, 58, 910257, 0),
(4, 10, 59, 910258, 0),
(4, 10, 60, 910259, 0),
(4, 10, 61, 910260, 0),
(10, 10, 46, 910245, 0),
(10, 10, 47, 910246, 0),
(10, 10, 48, 910247, 0),
(10, 10, 49, 910248, 0),
(10, 10, 50, 910249, 0),
(10, 10, 51, 910250, 0),
(10, 10, 52, 910251, 0),
(10, 10, 53, 910252, 0),
(10, 10, 54, 910253, 0),
(10, 10, 55, 910254, 0),
(10, 10, 56, 910255, 0),
(10, 10, 57, 910256, 0),
(10, 10, 58, 910257, 0),
(10, 10, 59, 910258, 0),
(10, 10, 60, 910259, 0),
(10, 10, 61, 910260, 0);

USE acore_characters;

CREATE TEMPORARY TABLE `tmp_demon_hunter_retail_talent_pass` (
  `button` tinyint unsigned NOT NULL,
  `spell` int unsigned NOT NULL PRIMARY KEY
);
INSERT INTO `tmp_demon_hunter_retail_talent_pass` (`button`, `spell`) VALUES
(46, 910245), (47, 910246), (48, 910247), (49, 910248),
(50, 910249), (51, 910250), (52, 910251), (53, 910252),
(54, 910253), (55, 910254), (56, 910255), (57, 910256),
(58, 910257), (59, 910258), (60, 910259), (61, 910260);

INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT c.`guid`, s.`spell`, 1
FROM `characters` c
CROSS JOIN `tmp_demon_hunter_retail_talent_pass` s
WHERE c.`class` = 10;

DELETE ca
FROM `character_action` ca
JOIN `characters` c ON c.`guid` = ca.`guid`
WHERE c.`class` = 10
  AND (ca.`button` BETWEEN 46 AND 61 OR ca.`action` BETWEEN 910245 AND 910260);

INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT c.`guid`, 0, s.`button`, s.`spell`, 0
FROM `characters` c
CROSS JOIN `tmp_demon_hunter_retail_talent_pass` s
WHERE c.`class` = 10;

DROP TEMPORARY TABLE `tmp_demon_hunter_retail_talent_pass`;
