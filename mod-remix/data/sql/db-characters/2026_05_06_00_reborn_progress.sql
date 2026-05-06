CREATE TABLE IF NOT EXISTS `remix_reborn_progress` (
  `account_id` int unsigned NOT NULL,
  `reborn_count` int unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
