SET @TOKEN_CREDITS := 900101;
SET @REBORN_TOKEN := 900113;
SET @REBORN_XP := 900114;
SET @REBORN_REPUTATION := 900115;
SET @REBORN_TOKEN_DROP := 900116;
SET @REBORN_MOVEMENT := 900117;
SET @CHROMIE_REBORN := 900150;
SET @UNICUS := 900151;
SET @REBORN_TEXT := 900101;
SET @UNICUS_TEXT := 900102;

DELETE FROM `item_template` WHERE `entry` = @REBORN_TOKEN;
DELETE FROM `currencytypes_dbc` WHERE `ID` = @REBORN_TOKEN OR `ItemID` = @REBORN_TOKEN;
DELETE FROM `spell_dbc` WHERE `ID` BETWEEN @REBORN_XP AND @REBORN_MOVEMENT;
DELETE FROM `npc_text` WHERE `ID` IN (@REBORN_TEXT, @UNICUS_TEXT);
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (@CHROMIE_REBORN, @UNICUS);
DELETE FROM `creature_template` WHERE `entry` IN (@CHROMIE_REBORN, @UNICUS);

INSERT INTO `item_template` (`entry`) VALUES (@REBORN_TOKEN);
UPDATE `item_template` SET
  `class` = 10,
  `subclass` = 0,
  `SoundOverrideSubclass` = -1,
  `name` = 'Reborn Token',
  `displayid` = 34853,
  `Quality` = 6,
  `Flags` = 64,
  `BuyCount` = 1,
  `InventoryType` = 0,
  `AllowableClass` = -1,
  `AllowableRace` = -1,
  `ItemLevel` = 1,
  `RequiredLevel` = 1,
  `maxcount` = 0,
  `stackable` = 2147483647,
  `bonding` = 1,
  `description` = 'Awarded when a character is Reborn.',
  `Material` = 4,
  `BagFamily` = 8192,
  `RequiredDisenchantSkill` = -1,
  `VerifiedBuild` = 12340
WHERE `entry` = @REBORN_TOKEN;

INSERT INTO `currencytypes_dbc` (`ID`, `ItemID`, `CategoryID`, `BitIndex`)
VALUES (@REBORN_TOKEN, @REBORN_TOKEN, 1, 31);

INSERT INTO `spell_dbc` (`ID`) VALUES
(@REBORN_XP),
(@REBORN_REPUTATION),
(@REBORN_TOKEN_DROP),
(@REBORN_MOVEMENT);

UPDATE `spell_dbc` SET
  `Attributes` = 2147483648,
  `AttributesEx3` = 1048576,
  `RangeIndex` = 1,
  `CastingTimeIndex` = 1,
  `DurationIndex` = 21,
  `CumulativeAura` = 255,
  `Effect_1` = 6,
  `EffectAura_1` = 4,
  `ImplicitTargetA_1` = 1,
  `SpellIconID` = `ID`,
  `ActiveIconID` = `ID`,
  `Name_Lang_Mask` = 1,
  `Description_Lang_Mask` = 1,
  `AuraDescription_Lang_Mask` = 1
WHERE `ID` BETWEEN @REBORN_XP AND @REBORN_MOVEMENT;

UPDATE `spell_dbc` SET
  `Name_Lang_enUS` = 'Reborn Experience',
  `Description_Lang_enUS` = 'Each stack grants +5% experience from kills and quests.',
  `AuraDescription_Lang_enUS` = 'Each stack grants +5% experience from kills and quests.'
WHERE `ID` = @REBORN_XP;

UPDATE `spell_dbc` SET
  `Name_Lang_enUS` = 'Reborn Reputation',
  `Description_Lang_enUS` = 'Each stack grants +5% reputation gained.',
  `AuraDescription_Lang_enUS` = 'Each stack grants +5% reputation gained.'
WHERE `ID` = @REBORN_REPUTATION;

UPDATE `spell_dbc` SET
  `Name_Lang_enUS` = 'Reborn Tokenfall',
  `Description_Lang_enUS` = 'Each stack grants +100% Remix Token drops.',
  `AuraDescription_Lang_enUS` = 'Each stack grants +100% Remix Token drops.'
WHERE `ID` = @REBORN_TOKEN_DROP;

UPDATE `spell_dbc` SET
  `Effect_1` = 6,
  `Effect_2` = 6,
  `Effect_3` = 6,
  `EffectAura_1` = 31,
  `EffectAura_2` = 58,
  `EffectAura_3` = 206,
  `EffectBasePoints_1` = 1,
  `EffectBasePoints_2` = 1,
  `EffectBasePoints_3` = 1,
  `ImplicitTargetA_1` = 1,
  `ImplicitTargetA_2` = 1,
  `ImplicitTargetA_3` = 1,
  `Name_Lang_enUS` = 'Reborn Momentum',
  `Description_Lang_enUS` = 'Each stack grants +2% movement speed.',
  `AuraDescription_Lang_enUS` = 'Each stack grants +2% movement speed.'
WHERE `ID` = @REBORN_MOVEMENT;

INSERT INTO `npc_text` (`ID`, `text0_0`, `Probability0`, `VerifiedBuild`) VALUES
(@REBORN_TEXT, 'Time is not a line, $N.  It is an invitation.  I can return you to the beginning, but you will carry the echoes forward.', 1, 12340),
(@UNICUS_TEXT, 'Unicus has found the reins history forgot.  Ten Token Credits per mount, no haggling with timelines.', 1, 12340);

-- Attach the Reborn gossip to existing Chromie templates, and provide a
-- dedicated spawnable Chromie template for realms without a convenient Chromie.
UPDATE `creature_template`
SET `npcflag` = `npcflag` | 1,
    `ScriptName` = 'npc_chromie_reborn'
WHERE `name` = 'Chromie';

INSERT INTO `creature_template` (
  `entry`,`difficulty_entry_1`,`difficulty_entry_2`,`difficulty_entry_3`,`KillCredit1`,`KillCredit2`,
  `name`,`subname`,`IconName`,`gossip_menu_id`,`minlevel`,`maxlevel`,`exp`,`faction`,`npcflag`,
  `speed_walk`,`speed_run`,`speed_swim`,`speed_flight`,`detection_range`,`rank`,`dmgschool`,
  `DamageModifier`,`BaseAttackTime`,`RangeAttackTime`,`BaseVariance`,`RangeVariance`,`unit_class`,
  `unit_flags`,`unit_flags2`,`dynamicflags`,`family`,`type`,`type_flags`,`lootid`,`pickpocketloot`,`skinloot`,`PetSpellDataId`,`VehicleId`,
  `mingold`,`maxgold`,`AIName`,`MovementType`,`HoverHeight`,`HealthModifier`,`ManaModifier`,`ArmorModifier`,
  `ExperienceModifier`,`RacialLeader`,`movementId`,`RegenHealth`,`CreatureImmunitiesId`,`flags_extra`,`ScriptName`,`VerifiedBuild`
) VALUES
(@CHROMIE_REBORN, 0, 0, 0, 0, 0, 'Chromie', 'Reborn Guide', NULL, 0, 80, 80, 2, 35, 1, 1, 1.14286, 1, 1, 20, 0, 0, 1, 2000, 2000, 1, 1, 1, 512, 2048, 0, 0, 7, 134217728, 0, 0, 0, 0, 0, 0, 0, '', 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 2, 'npc_chromie_reborn', 12340),
(@UNICUS, 0, 0, 0, 0, 0, 'Unicus', 'Lost Mount Curator', NULL, 0, 80, 80, 2, 35, 1, 1, 1.14286, 1, 1, 20, 0, 0, 1, 2000, 2000, 1, 1, 1, 512, 2048, 0, 0, 7, 134217728, 0, 0, 0, 0, 0, 0, 0, '', 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 2, 'npc_unicus_reborn_vendor', 12340);

INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(@CHROMIE_REBORN, 0, 24877, 1, 1, 0),
(@UNICUS, 0, 19294, 1, 1, 0);
