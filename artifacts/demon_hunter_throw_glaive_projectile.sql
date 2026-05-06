-- Dedicated visual template for Demon Hunter Throw Glaive.
-- Cloned from the invisible world trigger, but with the Illidan glaive display
-- assigned at template load so the client never sees the trigger's fallback model.
DELETE FROM `creature_template_model` WHERE `CreatureID` = 910350;
DELETE FROM `creature_template` WHERE `entry` = 910350;

CREATE TEMPORARY TABLE `tmp_gpt_dh_throw_glaive_template`
SELECT * FROM `creature_template` WHERE `entry` = 12999 LIMIT 1;

UPDATE `tmp_gpt_dh_throw_glaive_template`
SET
    `entry` = 910350,
    `name` = '',
    `subname` = NULL,
    `faction` = 35,
    `unit_flags` = 33587970,
    `unit_flags2` = 2048,
    `flags_extra` = 130,
    `VerifiedBuild` = 0;

INSERT INTO `creature_template`
SELECT * FROM `tmp_gpt_dh_throw_glaive_template`;

DROP TEMPORARY TABLE `tmp_gpt_dh_throw_glaive_template`;

INSERT INTO `creature_template_model`
    (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`)
VALUES
    (910350, 0, 21431, 0.38, 1, 0);
