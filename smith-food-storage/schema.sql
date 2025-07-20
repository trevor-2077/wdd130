-- -----------------------------------------------------
-- Drop old/unneeded tables (if they exist)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `quantity`;
DROP TABLE IF EXISTS `storage_location`;
DROP TABLE IF EXISTS `where_bought`;
DROP TABLE IF EXISTS `item`;
DROP TABLE IF EXISTS `location`;
DROP TABLE IF EXISTS `store`;
DROP TABLE IF EXISTS `category`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `program_runs`;

-- -----------------------------------------------------
-- Schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `smith_food_storage_db`
  DEFAULT CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;
USE `smith_food_storage_db`;

-- -----------------------------------------------------
-- users
-- -----------------------------------------------------
CREATE TABLE `users` (
  `user_id`    INT         NOT NULL AUTO_INCREMENT,
  `username`   VARCHAR(50) NOT NULL UNIQUE,
  `email`      VARCHAR(120) NOT NULL UNIQUE,
  `pw_hash`    VARCHAR(128) NOT NULL,
  `created_at` DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- store
-- -----------------------------------------------------
CREATE TABLE `store` (
  `store_id`   INT          NOT NULL AUTO_INCREMENT,
  `name`       VARCHAR(100) NOT NULL,
  PRIMARY KEY (`store_id`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- category
-- -----------------------------------------------------
CREATE TABLE `category` (
  `category_id` INT          NOT NULL AUTO_INCREMENT,
  `name`        VARCHAR(100) NOT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- location (with self‑reference parent_id)
-- -----------------------------------------------------
CREATE TABLE `location` (
  `location_id` INT          NOT NULL AUTO_INCREMENT,
  `user_id`     INT          NOT NULL,
  `name`        VARCHAR(100) NOT NULL,
  `parent_id`   INT          NULL,
  PRIMARY KEY (`location_id`),
  INDEX `idx_location_user`   (`user_id`),
  INDEX `idx_location_parent` (`parent_id`),
  CONSTRAINT `fk_location_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `users` (`user_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_location_parent`
    FOREIGN KEY (`parent_id`)
    REFERENCES `location` (`location_id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- item
-- -----------------------------------------------------
CREATE TABLE `item` (
  `item_id`        INT             NOT NULL AUTO_INCREMENT,
  `user_id`        INT             NOT NULL,
  `store_id`       INT             NULL,
  `category_id`    INT             NULL,
  `location_id`    INT             NULL,
  `name`           VARCHAR(100)    NOT NULL,
  `quantity`       INT             NOT NULL DEFAULT 1,
  `purchase_price` DECIMAL(8,2)    NULL,
  `expires`        DATE            NULL,
  `purchased_at`   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`item_id`),
  INDEX `idx_item_user`     (`user_id`),
  INDEX `idx_item_store`    (`store_id`),
  INDEX `idx_item_category` (`category_id`),
  INDEX `idx_item_location` (`location_id`),
  CONSTRAINT `fk_item_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `users` (`user_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_item_store`
    FOREIGN KEY (`store_id`)
    REFERENCES `store` (`store_id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `fk_item_category`
    FOREIGN KEY (`category_id`)
    REFERENCES `category` (`category_id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `fk_item_location`
    FOREIGN KEY (`location_id`)
    REFERENCES `location` (`location_id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- program_runs (logs of each assignment execution)
-- -----------------------------------------------------
CREATE TABLE `program_runs` (
  `id`        INT          NOT NULL AUTO_INCREMENT,
  `input`     VARCHAR(200) NULL,
  `output`    VARCHAR(200) NULL,
  `timestamp` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;
