-- Adds another retail-informed Demon Hunter spellbook pass and syncs existing characters.
-- Apply after 2026_05_05_05_demon_hunter_retail_talent_pass.sql
-- and install the matching client MPQ/DBC rebuild.
--
-- Fel Rush safety note: the matching client build uses only the lightweight
-- channel overlay for spell 910204 and excludes cfx_demonhunter_felrush_statebase
-- from patch-4.MPQ because that retail state model can crash the 3.3.5a renderer.

USE acore_world;

DELETE FROM `playercreateinfo_spell_custom`
WHERE `classmask` = 512
  AND `Spell` BETWEEN 910261 AND 910280;

INSERT INTO `playercreateinfo_spell_custom` (`racemask`, `classmask`, `Spell`, `Note`) VALUES
(520, 512, 910261, 'Demon Hunter - Chaos Theory'),
(520, 512, 910262, 'Demon Hunter - Trail of Ruin'),
(520, 512, 910263, 'Demon Hunter - First Blood'),
(520, 512, 910264, 'Demon Hunter - Ragefire'),
(520, 512, 910265, 'Demon Hunter - Any Means Necessary'),
(520, 512, 910266, 'Demon Hunter - Know Your Enemy'),
(520, 512, 910267, 'Demon Hunter - Inner Demon'),
(520, 512, 910268, 'Demon Hunter - Initiative'),
(520, 512, 910269, 'Demon Hunter - Burning Wound'),
(520, 512, 910270, 'Demon Hunter - Rush of Chaos'),
(520, 512, 910271, 'Demon Hunter - Soul Furnace'),
(520, 512, 910272, 'Demon Hunter - Calcified Spikes'),
(520, 512, 910273, 'Demon Hunter - Illuminated Sigils'),
(520, 512, 910274, 'Demon Hunter - Void Reaver'),
(520, 512, 910275, 'Demon Hunter - Fallout'),
(520, 512, 910276, 'Demon Hunter - Feed the Demon'),
(520, 512, 910277, 'Demon Hunter - Burning Alive'),
(520, 512, 910278, 'Demon Hunter - Down in Flames'),
(520, 512, 910279, 'Demon Hunter - Ruinous Bulwark'),
(520, 512, 910280, 'Demon Hunter - Last Resort');

DELETE FROM `playercreateinfo_action`
WHERE `class` = 10
  AND `race` IN (4, 10)
  AND (`button` BETWEEN 62 AND 81 OR `action` BETWEEN 910261 AND 910280);

INSERT INTO `playercreateinfo_action` (`race`, `class`, `button`, `action`, `type`) VALUES
(4, 10, 62, 910261, 0),
(4, 10, 63, 910262, 0),
(4, 10, 64, 910263, 0),
(4, 10, 65, 910264, 0),
(4, 10, 66, 910265, 0),
(4, 10, 67, 910266, 0),
(4, 10, 68, 910267, 0),
(4, 10, 69, 910268, 0),
(4, 10, 70, 910269, 0),
(4, 10, 71, 910270, 0),
(4, 10, 72, 910271, 0),
(4, 10, 73, 910272, 0),
(4, 10, 74, 910273, 0),
(4, 10, 75, 910274, 0),
(4, 10, 76, 910275, 0),
(4, 10, 77, 910276, 0),
(4, 10, 78, 910277, 0),
(4, 10, 79, 910278, 0),
(4, 10, 80, 910279, 0),
(4, 10, 81, 910280, 0),
(10, 10, 62, 910261, 0),
(10, 10, 63, 910262, 0),
(10, 10, 64, 910263, 0),
(10, 10, 65, 910264, 0),
(10, 10, 66, 910265, 0),
(10, 10, 67, 910266, 0),
(10, 10, 68, 910267, 0),
(10, 10, 69, 910268, 0),
(10, 10, 70, 910269, 0),
(10, 10, 71, 910270, 0),
(10, 10, 72, 910271, 0),
(10, 10, 73, 910272, 0),
(10, 10, 74, 910273, 0),
(10, 10, 75, 910274, 0),
(10, 10, 76, 910275, 0),
(10, 10, 77, 910276, 0),
(10, 10, 78, 910277, 0),
(10, 10, 79, 910278, 0),
(10, 10, 80, 910279, 0),
(10, 10, 81, 910280, 0);

USE acore_characters;

CREATE TEMPORARY TABLE `tmp_demon_hunter_retail_spellbook_tabs_safety_pass` (
  `button` tinyint unsigned NOT NULL,
  `spell` int unsigned NOT NULL PRIMARY KEY
);

INSERT INTO `tmp_demon_hunter_retail_spellbook_tabs_safety_pass` (`button`, `spell`) VALUES
(62, 910261), (63, 910262), (64, 910263), (65, 910264),
(66, 910265), (67, 910266), (68, 910267), (69, 910268),
(70, 910269), (71, 910270), (72, 910271), (73, 910272),
(74, 910273), (75, 910274), (76, 910275), (77, 910276),
(78, 910277), (79, 910278), (80, 910279), (81, 910280);

INSERT IGNORE INTO `character_spell` (`guid`, `spell`, `specMask`)
SELECT c.`guid`, s.`spell`, 1
FROM `characters` c
CROSS JOIN `tmp_demon_hunter_retail_spellbook_tabs_safety_pass` s
WHERE c.`class` = 10;

DELETE ca
FROM `character_action` ca
JOIN `characters` c ON c.`guid` = ca.`guid`
WHERE c.`class` = 10
  AND (ca.`button` BETWEEN 62 AND 81 OR ca.`action` BETWEEN 910261 AND 910280);

INSERT INTO `character_action` (`guid`, `spec`, `button`, `action`, `type`)
SELECT c.`guid`, 0, s.`button`, s.`spell`, 0
FROM `characters` c
CROSS JOIN `tmp_demon_hunter_retail_spellbook_tabs_safety_pass` s
WHERE c.`class` = 10;

DROP TEMPORARY TABLE `tmp_demon_hunter_retail_spellbook_tabs_safety_pass`;
