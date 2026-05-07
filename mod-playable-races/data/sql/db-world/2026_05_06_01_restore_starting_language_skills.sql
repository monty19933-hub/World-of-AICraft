-- Restore startup language skills for every playable race.
-- Characters cannot speak a language unless the matching language skill is
-- present at a usable rank in character_skills.

SET @HUMAN_MASK := 1;
SET @ORC_MASK := 2;
SET @DWARF_MASK := 4;
SET @NIGHT_ELF_MASK := 8;
SET @UNDEAD_MASK := 16;
SET @TAUREN_MASK := 32;
SET @GNOME_MASK := 64;
SET @TROLL_MASK := 128;
SET @GOBLIN_MASK := 256;
SET @BLOOD_ELF_MASK := 512;
SET @DRAENEI_MASK := 1024;
SET @WORGEN_MASK := 2048;
SET @OLD_WORGEN_MASK := 2097152;

DELETE FROM `playercreateinfo_skills`
WHERE `classMask` = 0
  AND `skill` IN (98, 109, 111, 113, 115, 137, 313, 315, 673, 759)
  AND `raceMask` IN (
      @HUMAN_MASK, @ORC_MASK, @DWARF_MASK, @NIGHT_ELF_MASK,
      @UNDEAD_MASK, @TAUREN_MASK, @GNOME_MASK, @TROLL_MASK,
      @GOBLIN_MASK, @BLOOD_ELF_MASK, @DRAENEI_MASK,
      @WORGEN_MASK, @OLD_WORGEN_MASK
  );

INSERT INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@HUMAN_MASK, 0, 98, 300, 'Language: Common'),
(@ORC_MASK, 0, 109, 300, 'Language: Orcish'),
(@DWARF_MASK, 0, 98, 300, 'Language: Common'),
(@DWARF_MASK, 0, 111, 300, 'Language: Dwarven'),
(@NIGHT_ELF_MASK, 0, 98, 300, 'Language: Common'),
(@NIGHT_ELF_MASK, 0, 113, 300, 'Language: Darnassian'),
(@UNDEAD_MASK, 0, 109, 300, 'Language: Orcish'),
(@UNDEAD_MASK, 0, 673, 300, 'Language: Gutterspeak'),
(@TAUREN_MASK, 0, 109, 300, 'Language: Orcish'),
(@TAUREN_MASK, 0, 115, 300, 'Language: Taurahe'),
(@GNOME_MASK, 0, 98, 300, 'Language: Common'),
(@GNOME_MASK, 0, 313, 300, 'Language: Gnomish'),
(@TROLL_MASK, 0, 109, 300, 'Language: Orcish'),
(@TROLL_MASK, 0, 315, 300, 'Language: Troll'),
(@GOBLIN_MASK, 0, 109, 300, 'Language: Orcish'),
(@BLOOD_ELF_MASK, 0, 109, 300, 'Language: Orcish'),
(@BLOOD_ELF_MASK, 0, 137, 300, 'Language: Thalassian'),
(@DRAENEI_MASK, 0, 98, 300, 'Language: Common'),
(@DRAENEI_MASK, 0, 759, 300, 'Language: Draenei'),
(@WORGEN_MASK, 0, 98, 300, 'Language: Common'),
(@OLD_WORGEN_MASK, 0, 98, 300, 'Language: Common');
