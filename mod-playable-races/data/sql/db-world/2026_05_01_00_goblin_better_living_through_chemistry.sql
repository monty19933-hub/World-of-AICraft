-- Goblin racial passive: Better Living Through Chemistry.
-- Gives +5 Alchemy and places the racial in the Goblin General spellbook.

SET @GOBLIN_MASK := 256;
SET @SPELL_BETTER_LIVING := 69045;
SET @SKILL_RACIAL_GOBLIN := 790;
SET @SKILL_LINE_ABILITY := 21986;

DELETE FROM `spell_dbc` WHERE `ID` = @SPELL_BETTER_LIVING;
INSERT INTO `spell_dbc`
(`ID`, `Attributes`, `CastingTimeIndex`, `ProcChance`, `DurationIndex`, `RangeIndex`, `EquippedItemClass`,
 `Effect_1`, `EffectDieSides_1`, `EffectBasePoints_1`, `ImplicitTargetA_1`, `EffectAura_1`, `EffectMiscValue_1`,
 `SpellIconID`, `Name_Lang_enUS`, `NameSubtext_Lang_enUS`, `Description_Lang_enUS`,
 `Name_Lang_Mask`, `NameSubtext_Lang_Mask`, `Description_Lang_Mask`, `AuraDescription_Lang_Mask`,
 `EffectChainAmplitude_1`, `SchoolMask`, `EffectBonusMultiplier_1`, `EffectBonusMultiplier_2`, `EffectBonusMultiplier_3`)
VALUES
(@SPELL_BETTER_LIVING, 80, 1, 101, 21, 1, -1,
 6, 1, 4, 1, 98, 171,
 370670, 'Better Living Through Chemistry', 'Racial Passive', 'Alchemy skill increased by $s1.',
 16712190, 16712190, 16712190, 16712190,
 1, 1, 1, 1, 1);

DELETE FROM `skillline_dbc` WHERE `ID` = @SKILL_RACIAL_GOBLIN;
INSERT INTO `skillline_dbc`
(`ID`, `CategoryID`, `SkillCostsID`, `DisplayName_Lang_enUS`, `DisplayName_Lang_Mask`, `Description_Lang_Mask`, `SpellIconID`, `AlternateVerb_Lang_Mask`, `CanLink`)
VALUES
(@SKILL_RACIAL_GOBLIN, 9, 0, 'Racial - Goblin', 16712190, 16712172, 133032, 16712172, 0);

DELETE FROM `skilllineability_dbc` WHERE `ID` = @SKILL_LINE_ABILITY OR `Spell` = @SPELL_BETTER_LIVING;
INSERT INTO `skilllineability_dbc`
(`ID`, `SkillLine`, `Spell`, `RaceMask`, `ClassMask`, `ExcludeRace`, `ExcludeClass`, `MinSkillLineRank`, `SupercededBySpell`, `AcquireMethod`, `TrivialSkillLineRankHigh`, `TrivialSkillLineRankLow`, `CharacterPoints_1`, `CharacterPoints_2`)
VALUES
(@SKILL_LINE_ABILITY, @SKILL_RACIAL_GOBLIN, @SPELL_BETTER_LIVING, @GOBLIN_MASK, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0);

INSERT IGNORE INTO `playercreateinfo_spell_custom` (`racemask`, `classmask`, `Spell`, `Note`)
VALUES (@GOBLIN_MASK, 0, @SPELL_BETTER_LIVING, 'Goblin - Better Living Through Chemistry');
