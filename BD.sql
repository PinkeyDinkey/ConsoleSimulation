-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema Sovkombank_bot
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema Sovkombank_bot
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Sovkombank_bot` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
USE `Sovkombank_bot` ;

-- -----------------------------------------------------
-- Table `Sovkombank_bot`.`Session`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Sovkombank_bot`.`Session` (
  `idSession` INT NOT NULL AUTO_INCREMENT,
  `StartTime` DATETIME NOT NULL,
  `EndTime` DATETIME NULL,
  PRIMARY KEY (`idSession`),
  UNIQUE INDEX `idSession_UNIQUE` (`idSession` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Sovkombank_bot`.`Message`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Sovkombank_bot`.`Message` (
  `idMessage` INT NOT NULL AUTO_INCREMENT,
  `MessageTime` DATETIME NOT NULL,
  `idSession` INT NOT NULL,
  `Text` LONGTEXT NULL,
  `idClient` INT NOT NULL,
  PRIMARY KEY (`idMessage`, `idSession`, `idClient`),
  UNIQUE INDEX `idMessage_UNIQUE` (`idMessage` ASC) VISIBLE,
  INDEX `Session_idx` (`idSession` ASC) VISIBLE,
  CONSTRAINT `Session`
    FOREIGN KEY (`idSession`)
    REFERENCES `Sovkombank_bot`.`Session` (`idSession`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
