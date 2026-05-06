-- Starting weapon proficiencies for custom Goblin and Worgen characters.
-- Stock AzerothCore has several starting weapon skills restricted to original
-- race masks, so custom races need their own race-mask rows.

SET @GOBLIN_MASK := 256;
SET @WORGEN_MASK := 2048;
SET @CUSTOM_RACES := @GOBLIN_MASK | @WORGEN_MASK;

SET @CLASS_WARRIOR := 1;
SET @CLASS_HUNTER := 4;
SET @CLASS_ROGUE := 8;
SET @CLASS_WARLOCK := 256;

DELETE FROM `playercreateinfo_skills`
WHERE `raceMask` = @CUSTOM_RACES
  AND `skill` IN (45, 46, 160, 173, 226);

INSERT INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@CUSTOM_RACES, @CLASS_HUNTER, 45, 0, 'Goblin/Worgen Hunter - Bows'),
(@CUSTOM_RACES, @CLASS_HUNTER, 46, 0, 'Goblin/Worgen Hunter - Guns'),
(@CUSTOM_RACES, @CLASS_HUNTER, 226, 0, 'Goblin/Worgen Hunter - Crossbows'),
(@CUSTOM_RACES, @CLASS_WARRIOR, 160, 0, 'Goblin/Worgen Warrior - Two-Handed Maces'),
(@CUSTOM_RACES, @CLASS_ROGUE | @CLASS_WARLOCK, 173, 0, 'Goblin/Worgen Rogue/Warlock - Daggers');
