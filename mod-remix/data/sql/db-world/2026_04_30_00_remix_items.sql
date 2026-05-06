SET @REMIX_SHIRT := 900100;
SET @TOKEN_CREDITS := 900101;
SET @REMIX_USE_SPELL := 900102;
SET @REMIX_STAMINA := 900103;
SET @REMIX_AGILITY := 900104;
SET @REMIX_STRENGTH := 900105;
SET @REMIX_INTELLECT := 900106;
SET @REMIX_CRIT := 900107;
SET @REMIX_HIT := 900108;
SET @REMIX_SPELL_POWER := 900109;
SET @REMIX_ATTACK_POWER := 900110;
SET @REMIX_XP := 900111;
SET @REMIX_GOLD := 900112;
SET @REMIX_GOSSIP_TEXT := 900100;

DELETE FROM `item_template` WHERE `entry` IN (@REMIX_SHIRT, @TOKEN_CREDITS);
DELETE FROM `currencytypes_dbc` WHERE `ID` = @TOKEN_CREDITS OR `ItemID` = @TOKEN_CREDITS;
DELETE FROM `spell_dbc` WHERE `ID` BETWEEN @REMIX_USE_SPELL AND @REMIX_GOLD;
DELETE FROM `npc_text` WHERE `ID` = @REMIX_GOSSIP_TEXT;

INSERT INTO `item_template` (`entry`) VALUES (@REMIX_SHIRT);
UPDATE `item_template` SET
  `class` = 4,
  `subclass` = 0,
  `name` = 'Chrono-Thread Shirt',
  `displayid` = 9891,
  `Quality` = 6,
  `Flags` = 64,
  `BuyCount` = 1,
  `InventoryType` = 4,
  `AllowableClass` = -1,
  `AllowableRace` = -1,
  `ItemLevel` = 1,
  `RequiredLevel` = 1,
  `spellid_1` = @REMIX_USE_SPELL,
  `spelltrigger_1` = 0,
  `spellcooldown_1` = 1000,
  `bonding` = 1,
  `description` = 'Right-click to upgrade Remix stats with Token Credits.',
  `Material` = 7,
  `ScriptName` = 'item_remix_shirt',
  `VerifiedBuild` = 12340
WHERE `entry` = @REMIX_SHIRT;

INSERT INTO `item_template` (`entry`) VALUES (@TOKEN_CREDITS);
UPDATE `item_template` SET
  `class` = 10,
  `subclass` = 0,
  `SoundOverrideSubclass` = -1,
  `name` = 'Token Credits',
  `displayid` = 32278,
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
  `description` = 'A Remix upgrade currency stored in the currency tab.',
  `Material` = 4,
  `BagFamily` = 8192,
  `RequiredDisenchantSkill` = -1,
  `VerifiedBuild` = 12340
WHERE `entry` = @TOKEN_CREDITS;

INSERT INTO `currencytypes_dbc` (`ID`, `ItemID`, `CategoryID`, `BitIndex`)
VALUES (@TOKEN_CREDITS, @TOKEN_CREDITS, 1, 30);

INSERT INTO `spell_dbc` (`ID`) VALUES
(@REMIX_USE_SPELL),
(@REMIX_STAMINA),
(@REMIX_AGILITY),
(@REMIX_STRENGTH),
(@REMIX_INTELLECT),
(@REMIX_CRIT),
(@REMIX_HIT),
(@REMIX_SPELL_POWER),
(@REMIX_ATTACK_POWER),
(@REMIX_XP),
(@REMIX_GOLD);

UPDATE `spell_dbc` SET
  `RangeIndex` = 1,
  `CastingTimeIndex` = 1,
  `SpellIconID` = @REMIX_USE_SPELL,
  `ActiveIconID` = @REMIX_USE_SPELL,
  `Name_Lang_enUS` = 'Remix Interface',
  `Description_Lang_enUS` = 'Opens the Chrono-Thread upgrade interface.',
  `AuraDescription_Lang_enUS` = '',
  `Name_Lang_Mask` = 1,
  `Description_Lang_Mask` = 1,
  `AuraDescription_Lang_Mask` = 1
WHERE `ID` = @REMIX_USE_SPELL;

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
WHERE `ID` BETWEEN @REMIX_STAMINA AND @REMIX_GOLD;

UPDATE `spell_dbc` SET `Name_Lang_enUS` = 'Remix Stamina', `Description_Lang_enUS` = 'Each stack grants +10 Stamina.', `AuraDescription_Lang_enUS` = 'Each stack grants +10 Stamina.' WHERE `ID` = @REMIX_STAMINA;
UPDATE `spell_dbc` SET `Name_Lang_enUS` = 'Remix Agility', `Description_Lang_enUS` = 'Each stack grants +5% Agility.', `AuraDescription_Lang_enUS` = 'Each stack grants +5% Agility.' WHERE `ID` = @REMIX_AGILITY;
UPDATE `spell_dbc` SET `Name_Lang_enUS` = 'Remix Strength', `Description_Lang_enUS` = 'Each stack grants +5% Strength.', `AuraDescription_Lang_enUS` = 'Each stack grants +5% Strength.' WHERE `ID` = @REMIX_STRENGTH;
UPDATE `spell_dbc` SET `Name_Lang_enUS` = 'Remix Intellect', `Description_Lang_enUS` = 'Each stack grants +5% Intellect.', `AuraDescription_Lang_enUS` = 'Each stack grants +5% Intellect.' WHERE `ID` = @REMIX_INTELLECT;
UPDATE `spell_dbc` SET `Name_Lang_enUS` = 'Remix Critical Strike', `Description_Lang_enUS` = 'Each stack grants +5% melee, ranged, and spell critical strike.', `AuraDescription_Lang_enUS` = 'Each stack grants +5% melee, ranged, and spell critical strike.' WHERE `ID` = @REMIX_CRIT;
UPDATE `spell_dbc` SET `Name_Lang_enUS` = 'Remix Hit', `Description_Lang_enUS` = 'Each stack grants +5% melee, ranged, and spell hit.', `AuraDescription_Lang_enUS` = 'Each stack grants +5% melee, ranged, and spell hit.' WHERE `ID` = @REMIX_HIT;
UPDATE `spell_dbc` SET `Name_Lang_enUS` = 'Remix Spell Damage', `Description_Lang_enUS` = 'Each stack grants +5% Spell Damage.', `AuraDescription_Lang_enUS` = 'Each stack grants +5% Spell Damage.' WHERE `ID` = @REMIX_SPELL_POWER;
UPDATE `spell_dbc` SET `Name_Lang_enUS` = 'Remix Attack Power', `Description_Lang_enUS` = 'Each stack grants +5% melee and ranged Attack Power.', `AuraDescription_Lang_enUS` = 'Each stack grants +5% melee and ranged Attack Power.' WHERE `ID` = @REMIX_ATTACK_POWER;
UPDATE `spell_dbc` SET `Name_Lang_enUS` = 'Remix Experience', `Description_Lang_enUS` = 'Each stack grants +5% account-wide experience.', `AuraDescription_Lang_enUS` = 'Each stack grants +5% account-wide experience.' WHERE `ID` = @REMIX_XP;
UPDATE `spell_dbc` SET `Name_Lang_enUS` = 'Remix Gold Loot', `Description_Lang_enUS` = 'Each stack grants +1% account-wide gold from loot.', `AuraDescription_Lang_enUS` = 'Each stack grants +1% account-wide gold from loot.' WHERE `ID` = @REMIX_GOLD;

INSERT INTO `npc_text` (`ID`, `text0_0`, `Probability0`, `VerifiedBuild`)
VALUES (@REMIX_GOSSIP_TEXT, 'Greetings, $N.  Welcome to the Upgrade Menu', 1, 12340);

DELETE FROM `playercreateinfo_item` WHERE `itemid` = @REMIX_SHIRT;
INSERT INTO `playercreateinfo_item` (`race`, `class`, `itemid`, `amount`, `Note`)
VALUES (0, 0, @REMIX_SHIRT, 1, 'Codex Remix starter shirt');
