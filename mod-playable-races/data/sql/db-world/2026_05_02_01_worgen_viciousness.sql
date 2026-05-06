-- Worgen racial passive: Viciousness.
-- Gives +1% critical strike chance and places the racial in the Worgen General spellbook.

SET @WORGEN_MASK := 2048;
SET @SPELL_VICIOUSNESS := 68975;
SET @SKILL_RACIAL_WORGEN := 789;
SET @SKILL_LINE_ABILITY := 21981;

DELETE FROM `spell_dbc` WHERE `ID` = @SPELL_VICIOUSNESS;
INSERT INTO `spell_dbc`
(`ID`, `Attributes`, `CastingTimeIndex`, `ProcChance`, `RangeIndex`, `EquippedItemClass`,
 `Effect_1`, `EffectDieSides_1`, `EffectBasePoints_1`, `ImplicitTargetA_1`, `EffectAura_1`,
 `SpellIconID`, `Name_Lang_enUS`, `NameSubtext_Lang_enUS`, `Description_Lang_enUS`, `AuraDescription_Lang_enUS`,
 `Name_Lang_Mask`, `NameSubtext_Lang_Mask`, `Description_Lang_Mask`, `AuraDescription_Lang_Mask`,
 `EffectChainAmplitude_1`, `SchoolMask`, `EffectBonusMultiplier_1`, `EffectBonusMultiplier_2`, `EffectBonusMultiplier_3`)
VALUES
(@SPELL_VICIOUSNESS, 80, 1, 101, 1, -1,
 6, 1, 0, 1, 290,
 1573, 'Viciousness', 'Racial Passive', 'Increases critical strike chance by $s1%.', 'Critical strike chance increased by $s1%.',
 16712190, 16712190, 16712190, 16712190,
 1, 1, 1, 1, 0);

DELETE FROM `skillline_dbc` WHERE `ID` = @SKILL_RACIAL_WORGEN;
INSERT INTO `skillline_dbc`
(`ID`, `CategoryID`, `SkillCostsID`, `DisplayName_Lang_enUS`, `DisplayName_Lang_Mask`, `Description_Lang_Mask`, `SpellIconID`, `AlternateVerb_Lang_Mask`, `CanLink`)
VALUES
(@SKILL_RACIAL_WORGEN, 9, 0, 'Racial - Worgen', 16712190, 16712172, 132203, 16712172, 0);

DELETE FROM `skilllineability_dbc` WHERE `ID` = @SKILL_LINE_ABILITY OR `Spell` = @SPELL_VICIOUSNESS;
INSERT INTO `skilllineability_dbc`
(`ID`, `SkillLine`, `Spell`, `RaceMask`, `ClassMask`, `ExcludeRace`, `ExcludeClass`, `MinSkillLineRank`, `SupercededBySpell`, `AcquireMethod`, `TrivialSkillLineRankHigh`, `TrivialSkillLineRankLow`, `CharacterPoints_1`, `CharacterPoints_2`)
VALUES
(@SKILL_LINE_ABILITY, @SKILL_RACIAL_WORGEN, @SPELL_VICIOUSNESS, @WORGEN_MASK, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0);

INSERT IGNORE INTO `playercreateinfo_spell_custom` (`racemask`, `classmask`, `Spell`, `Note`)
VALUES (@WORGEN_MASK, 0, @SPELL_VICIOUSNESS, 'Worgen - Viciousness');
