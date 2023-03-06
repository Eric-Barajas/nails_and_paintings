-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema nails_and_paintings
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema nails_and_paintings
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `nails_and_paintings` DEFAULT CHARACTER SET utf8 ;
USE `nails_and_paintings` ;

-- -----------------------------------------------------
-- Table `nails_and_paintings`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nails_and_paintings`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `credit_card` INT NULL,
  `address` VARCHAR(45) NULL,
  `phone_number` INT NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nails_and_paintings`.`nails`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nails_and_paintings`.`nails` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `sizes` VARCHAR(45) NULL,
  `shape` VARCHAR(45) NULL,
  `color` VARCHAR(45) NULL,
  `theme` VARCHAR(45) NULL,
  `price` INT NULL,
  `description` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `user_id` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_nails_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_nails_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `nails_and_paintings`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nails_and_paintings`.`paintings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nails_and_paintings`.`paintings` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NULL,
  `description` VARCHAR(255) NULL,
  `date` DATE NULL,
  `measurement` VARCHAR(45) NULL,
  `price` INT NULL,
  `category` VARCHAR(45) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `user_id` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_paintings_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_paintings_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `nails_and_paintings`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nails_and_paintings`.`carts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nails_and_paintings`.`carts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `user_id` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_carts_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_carts_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `nails_and_paintings`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
