USE acore_characters;

-- Amor was created while the first Rogue-shell experiment could still save a
-- Demon Hunter back as a Rogue. Preserve the character and restore its native
-- class marker.
UPDATE characters
SET class = 10
WHERE name = 'Amor' AND race IN (4, 10) AND class = 4;

-- Remove Rogue startup abilities from true Demon Hunters. The client still
-- receives a Rogue shell for stability, but class-10 characters should not be
-- taught the Rogue kit.
DELETE cs
FROM character_spell cs
JOIN characters c ON c.guid = cs.guid
WHERE c.class = 10
  AND cs.spell IN (
      1752, 1784, 1804, 1856, 1857, 1966, 2098, 2567, 2764, 2983,
      3018, 5011, 5171, 5277, 6603, 6770, 703, 921, 1725, 1766,
      1776, 1943, 408, 51722, 7620
  );

-- Lockpicking is Rogue-specific and can leak in from the shell during older
-- test characters.
DELETE ck
FROM character_skills ck
JOIN characters c ON c.guid = ck.guid
WHERE c.class = 10
  AND ck.skill IN (633);

DELETE ck
FROM character_skills ck
JOIN characters c ON c.guid = ck.guid
WHERE c.class = 10
  AND ck.skill NOT IN (
      38, 39, 43, 95, 98, 109, 113, 118, 137, 162, 173, 176, 253,
      414, 415, 473, 756, 777, 778, 910
  );

INSERT IGNORE INTO character_spell (guid, spell, specMask)
SELECT guid, 674, 1 FROM characters WHERE class = 10;
INSERT IGNORE INTO character_spell (guid, spell, specMask)
SELECT guid, 910201, 1 FROM characters WHERE class = 10;
INSERT IGNORE INTO character_spell (guid, spell, specMask)
SELECT guid, 910202, 1 FROM characters WHERE class = 10;
INSERT IGNORE INTO character_spell (guid, spell, specMask)
SELECT guid, 910203, 1 FROM characters WHERE class = 10;
INSERT IGNORE INTO character_spell (guid, spell, specMask)
SELECT guid, 910204, 1 FROM characters WHERE class = 10;

INSERT IGNORE INTO character_skills (guid, skill, value, max)
SELECT guid, 118, 5, 5 FROM characters WHERE class = 10;
INSERT IGNORE INTO character_skills (guid, skill, value, max)
SELECT guid, 910, 5, 5 FROM characters WHERE class = 10;
INSERT IGNORE INTO character_skills (guid, skill, value, max)
SELECT guid, 98, 300, 300 FROM characters WHERE class = 10 AND race = 4;
INSERT IGNORE INTO character_skills (guid, skill, value, max)
SELECT guid, 113, 300, 300 FROM characters WHERE class = 10 AND race = 4;
INSERT IGNORE INTO character_skills (guid, skill, value, max)
SELECT guid, 109, 300, 300 FROM characters WHERE class = 10 AND race = 10;
INSERT IGNORE INTO character_skills (guid, skill, value, max)
SELECT guid, 137, 300, 300 FROM characters WHERE class = 10 AND race = 10;

UPDATE character_inventory ci
JOIN item_instance ii ON ii.guid = ci.item AND ii.itemEntry = 139013
JOIN characters c ON c.guid = ci.guid AND c.class = 10
LEFT JOIN character_inventory equipped ON equipped.guid = ci.guid AND equipped.bag = 0 AND equipped.slot = 16
SET ci.bag = 0, ci.slot = 16
WHERE equipped.item IS NULL;

DELETE ca
FROM character_action ca
JOIN characters c ON c.guid = ca.guid
WHERE c.class = 10
  AND (ca.button BETWEEN 0 AND 4 OR ca.action IN (
      1752, 1784, 1804, 1856, 1857, 1966, 2098, 2567, 2764, 2983,
      3018, 5011, 5171, 5277, 6603, 6770, 703, 921, 1725, 1766,
      1776, 1943, 408, 51722, 7620, 910201, 910202, 910203, 910204
  ));

INSERT INTO character_action (guid, spec, button, action, type)
SELECT guid, 0, 0, 6603, 0 FROM characters WHERE class = 10;
INSERT INTO character_action (guid, spec, button, action, type)
SELECT guid, 0, 1, 910201, 0 FROM characters WHERE class = 10;
INSERT INTO character_action (guid, spec, button, action, type)
SELECT guid, 0, 2, 910202, 0 FROM characters WHERE class = 10;
INSERT INTO character_action (guid, spec, button, action, type)
SELECT guid, 0, 3, 910203, 0 FROM characters WHERE class = 10;
INSERT INTO character_action (guid, spec, button, action, type)
SELECT guid, 0, 4, 910204, 0 FROM characters WHERE class = 10;
