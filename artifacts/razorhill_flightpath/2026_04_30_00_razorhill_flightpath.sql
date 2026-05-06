-- Razor Hill flight path test for AzerothCore WotLK 3.3.5a.
-- Adds a Horde flight master and a client/server taxi node connected to Orgrimmar and Ratchet.
-- Client patch: Data\patch-4.MPQ

SET @RAZORHILL_NODE := 441;
SET @RAZORHILL_CREATURE := 900010;

DELETE FROM `creature` WHERE `id1` = @RAZORHILL_CREATURE;
DELETE FROM `creature_template_model` WHERE `CreatureID` = @RAZORHILL_CREATURE;
DELETE FROM `creature_equip_template` WHERE `CreatureID` = @RAZORHILL_CREATURE;
DELETE FROM `creature_template_movement` WHERE `CreatureId` = @RAZORHILL_CREATURE;
DELETE FROM `creature_template` WHERE `entry` = @RAZORHILL_CREATURE;
DELETE FROM `taxinodes_dbc` WHERE `ID` = @RAZORHILL_NODE;
DELETE FROM `taxipath_dbc` WHERE `ID` BETWEEN 1979 AND 1982;
DELETE FROM `taxipathnode_dbc` WHERE `PathID` BETWEEN 1979 AND 1982;

INSERT INTO `taxinodes_dbc`
(`ID`,`ContinentID`,`X`,`Y`,`Z`,`Name_Lang_enUS`,`Name_Lang_enGB`,`Name_Lang_koKR`,`Name_Lang_frFR`,`Name_Lang_deDE`,`Name_Lang_enCN`,`Name_Lang_zhCN`,`Name_Lang_enTW`,`Name_Lang_zhTW`,`Name_Lang_esES`,`Name_Lang_esMX`,`Name_Lang_ruRU`,`Name_Lang_ptPT`,`Name_Lang_ptBR`,`Name_Lang_itIT`,`Name_Lang_Unk`,`Name_Lang_Mask`,`MountCreatureID_1`,`MountCreatureID_2`)
VALUES
(@RAZORHILL_NODE,1,384.0,-4600.0,76.17,'Razor Hill, Durotar','', '', '', '', '', '', '', '', '', '', '', '', '', '', '',16712190,2224,0);

INSERT INTO `taxipath_dbc` (`ID`,`FromTaxiNode`,`ToTaxiNode`,`Cost`) VALUES
(1979,441,23,110),
(1980,23,441,110),
(1981,441,80,110),
(1982,80,441,110);

INSERT INTO `taxipathnode_dbc` (`ID`,`PathID`,`NodeIndex`,`ContinentID`,`LocX`,`LocY`,`LocZ`,`Flags`,`Delay`,`ArrivalEventID`,`DepartureEventID`) VALUES
(46875,1979,0,1,384.0,-4600.0,76.17,0,0,0,0),
(46876,1979,1,1,350.0,-4648.0,96.0,0,0,0,0),
(46877,1979,2,1,295.0,-4735.0,122.0,0,0,0,0),
(46878,1979,3,1,415.0,-4850.0,146.0,0,0,0,0),
(46879,1979,4,1,675.0,-4855.0,156.0,0,0,0,0),
(46880,1979,5,1,930.0,-4765.0,148.0,0,0,0,0),
(46881,1979,6,1,1060.0,-4595.0,126.0,0,0,0,0),
(46882,1979,7,1,1100.0,-4460.0,92.0,0,0,0,0),
(46883,1979,8,1,1105.0,-4358.0,62.0,0,0,0,0),
(46884,1979,9,1,1225.76,-4367.62,44.12,0,0,0,0),
(46885,1979,10,1,1348.87,-4378.23,39.12,0,0,0,0),
(46886,1979,11,1,1427.48,-4365.73,29.62,0,0,0,0),
(46887,1979,12,1,1439.58,-4419.2,29.62,0,0,0,0),
(46888,1979,13,1,1487.76,-4418.21,29.62,0,0,0,0),
(46889,1979,14,1,1562.84,-4414.54,46.7,0,0,0,0),
(46890,1979,15,1,1669.04,-4410.46,60.89,0,0,0,0),
(46891,1979,16,1,1713.89,-4374.61,67.25,0,0,0,0),
(46892,1979,17,1,1717.18,-4335.2,67.25,0,0,0,0),
(46893,1979,18,1,1677.59,-4315.7,61.17,0,0,0,0),
(46894,1980,0,1,1678.6,-4317.23,62.11,0,0,0,0),
(46895,1980,1,1,1717.18,-4335.2,67.25,0,0,0,0),
(46896,1980,2,1,1713.89,-4374.61,67.25,0,0,0,0),
(46897,1980,3,1,1669.04,-4410.46,60.89,0,0,0,0),
(46898,1980,4,1,1562.84,-4414.54,46.7,0,0,0,0),
(46899,1980,5,1,1487.76,-4418.21,29.62,0,0,0,0),
(46900,1980,6,1,1439.58,-4419.2,29.62,0,0,0,0),
(46901,1980,7,1,1427.48,-4365.73,29.62,0,0,0,0),
(46902,1980,8,1,1348.87,-4378.23,39.12,0,0,0,0),
(46903,1980,9,1,1225.76,-4367.62,44.12,0,0,0,0),
(46904,1980,10,1,1105.0,-4358.0,62.0,0,0,0,0),
(46905,1980,11,1,1100.0,-4460.0,92.0,0,0,0,0),
(46906,1980,12,1,1060.0,-4595.0,126.0,0,0,0,0),
(46907,1980,13,1,930.0,-4765.0,148.0,0,0,0,0),
(46908,1980,14,1,675.0,-4855.0,156.0,0,0,0,0),
(46909,1980,15,1,415.0,-4850.0,146.0,0,0,0,0),
(46910,1980,16,1,295.0,-4735.0,122.0,0,0,0,0),
(46911,1980,17,1,350.0,-4648.0,96.0,0,0,0,0),
(46912,1980,18,1,384.0,-4600.0,76.17,0,0,0,0),
(46913,1981,0,1,384.0,-4600.0,76.17,0,0,0,0),
(46914,1981,1,1,410.0,-4588.0,78.5,0,0,0,0),
(46915,1981,2,1,340.0,-4410.0,88.0,0,0,0,0),
(46916,1981,3,1,265.0,-4175.0,84.0,0,0,0,0),
(46917,1981,4,1,284.39,-3710.55,55.39,0,0,0,0),
(46918,1981,5,1,-86.96,-3707.59,55.39,0,0,0,0),
(46919,1981,6,1,-384.18,-3811.94,52.67,0,0,0,0),
(46920,1981,7,1,-613.95,-3862.66,80.72,0,0,0,0),
(46921,1981,8,1,-731.74,-3876.0,69.59,0,0,0,0),
(46922,1981,9,1,-828.3,-3830.81,34.34,0,0,0,0),
(46923,1981,10,1,-887.41,-3781.7,16.06,0,0,0,0),
(46924,1981,11,1,-894.6,-3773.0,11.5,0,0,0,0),
(46925,1982,0,1,-894.6,-3773.0,11.5,0,0,0,0),
(46926,1982,1,1,-886.65,-3783.26,16.56,0,0,0,0),
(46927,1982,2,1,-876.86,-3799.56,20.51,0,0,0,0),
(46928,1982,3,1,-820.48,-3899.81,55.26,0,0,0,0),
(46929,1982,4,1,-701.75,-3943.16,59.84,0,0,0,0),
(46930,1982,5,1,-373.71,-3888.38,60.26,0,0,0,0),
(46931,1982,6,1,-56.51,-3836.85,60.59,0,0,0,0),
(46932,1982,7,1,312.92,-3859.24,60.59,0,0,0,0),
(46933,1982,8,1,265.0,-4175.0,84.0,0,0,0,0),
(46934,1982,9,1,340.0,-4410.0,88.0,0,0,0,0),
(46935,1982,10,1,410.0,-4588.0,78.5,0,0,0,0),
(46936,1982,11,1,384.0,-4600.0,76.17,0,0,0,0);

INSERT INTO `creature_template`
(`entry`,`difficulty_entry_1`,`difficulty_entry_2`,`difficulty_entry_3`,`KillCredit1`,`KillCredit2`,`name`,`subname`,`IconName`,`gossip_menu_id`,`minlevel`,`maxlevel`,`exp`,`faction`,`npcflag`,`speed_walk`,`speed_run`,`speed_swim`,`speed_flight`,`detection_range`,`rank`,`dmgschool`,`DamageModifier`,`BaseAttackTime`,`RangeAttackTime`,`BaseVariance`,`RangeVariance`,`unit_class`,`unit_flags`,`unit_flags2`,`dynamicflags`,`family`,`type`,`type_flags`,`lootid`,`pickpocketloot`,`skinloot`,`PetSpellDataId`,`VehicleId`,`mingold`,`maxgold`,`AIName`,`MovementType`,`HoverHeight`,`HealthModifier`,`ManaModifier`,`ArmorModifier`,`ExperienceModifier`,`RacialLeader`,`movementId`,`RegenHealth`,`CreatureImmunitiesId`,`flags_extra`,`ScriptName`,`VerifiedBuild`)
VALUES
(@RAZORHILL_CREATURE,0,0,0,0,0,'Gor''mul Windtamer','Wind Rider Master',NULL,0,55,55,0,29,8195,1,1.14286,1,1,20,0,0,1,2000,2000,1,1,1,0,0,0,0,7,0,0,0,0,0,0,0,0,'',0,1,1,1,1,1,0,0,1,0,0,'',12340);

INSERT INTO `creature_template_model` (`CreatureID`,`Idx`,`CreatureDisplayID`,`DisplayScale`,`Probability`,`VerifiedBuild`)
VALUES (@RAZORHILL_CREATURE,0,1311,1,1,12340);

INSERT INTO `creature_equip_template` (`CreatureID`,`ID`,`ItemID1`,`ItemID2`,`ItemID3`,`VerifiedBuild`)
VALUES (@RAZORHILL_CREATURE,1,3433,0,0,18019);

INSERT INTO `creature`
(`id1`,`id2`,`id3`,`map`,`zoneId`,`areaId`,`spawnMask`,`phaseMask`,`equipment_id`,`position_x`,`position_y`,`position_z`,`orientation`,`spawntimesecs`,`wander_distance`,`currentwaypoint`,`curhealth`,`curmana`,`MovementType`,`npcflag`,`unit_flags`,`dynamicflags`,`ScriptName`,`VerifiedBuild`,`CreateObject`,`Comment`)
VALUES
(@RAZORHILL_CREATURE,0,0,1,14,362,1,1,1,384.0,-4600.0,76.17,3.89208,600,0,0,10572,0,0,0,0,0,'',0,0,'Codex Razorhill Flightpath: Flight Master');
