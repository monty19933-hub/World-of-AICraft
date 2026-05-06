CREATE TABLE IF NOT EXISTS `remix_character_progress` (
  `guid` int unsigned NOT NULL,
  `stamina_rank` int unsigned NOT NULL DEFAULT 0,
  `agility_rank` int unsigned NOT NULL DEFAULT 0,
  `strength_rank` int unsigned NOT NULL DEFAULT 0,
  `intellect_rank` int unsigned NOT NULL DEFAULT 0,
  `crit_rank` int unsigned NOT NULL DEFAULT 0,
  `hit_rank` int unsigned NOT NULL DEFAULT 0,
  `spell_power_rank` int unsigned NOT NULL DEFAULT 0,
  `attack_power_rank` int unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`guid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `remix_account_progress` (
  `account_id` int unsigned NOT NULL,
  `xp_rank` int unsigned NOT NULL DEFAULT 0,
  `gold_rank` int unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
