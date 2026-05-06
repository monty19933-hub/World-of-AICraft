-- Give the Remix shirt its custom inventory icon and matching item display row.

SET @REMIX_SHIRT := 900100;
SET @REMIX_SHIRT_DISPLAY := 900100;
SET @SOURCE_DISPLAY := 9891;
SET @REMIX_SHIRT_ICON := 'INV_Shirt_Duelist_A_01_Brown';

DELETE FROM `itemdisplayinfo_dbc` WHERE `ID` = @REMIX_SHIRT_DISPLAY;
INSERT INTO `itemdisplayinfo_dbc`
(`ID`, `ModelName_1`, `ModelName_2`, `ModelTexture_1`, `ModelTexture_2`, `InventoryIcon_1`, `InventoryIcon_2`,
 `GeosetGroup_1`, `GeosetGroup_2`, `GeosetGroup_3`, `Flags`, `SpellVisualID`, `GroupSoundIndex`,
 `HelmetGeosetVis_1`, `HelmetGeosetVis_2`,
 `Texture_1`, `Texture_2`, `Texture_3`, `Texture_4`, `Texture_5`, `Texture_6`, `Texture_7`, `Texture_8`,
 `ItemVisual`, `ParticleColorID`)
VALUES
(@REMIX_SHIRT_DISPLAY, '', '', '', '', @REMIX_SHIRT_ICON, '',
 0, 0, 0, 0, 0, 7,
 0, 0,
 '', '', '', 'Leather_A_05Yellow_Chest_TU', 'Leather_A_05Yellow_Chest_TL', '', '', '',
 0, 0);

UPDATE `item_template`
SET `displayid` = @REMIX_SHIRT_DISPLAY
WHERE `entry` = @REMIX_SHIRT;
