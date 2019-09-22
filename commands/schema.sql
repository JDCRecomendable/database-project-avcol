-- MySQL Script generated by MySQL Workbench
-- Fri 20 Sep 2019 00:03:26 NZST
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema online_shop_logistics
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema online_shop_logistics
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `online_shop_logistics` DEFAULT CHARACTER SET utf8 ;
USE `online_shop_logistics` ;

-- -----------------------------------------------------
-- Table `online_shop_logistics`.`customers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `online_shop_logistics`.`customers` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `last_name` VARCHAR(31) NOT NULL,
  `first_name` VARCHAR(31) NOT NULL,
  `email_address` VARCHAR(63) NOT NULL,
  `phone` VARCHAR(10) NOT NULL,
  `date_registered` DATE NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_address_UNIQUE` (`email_address` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `online_shop_logistics`.`products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `online_shop_logistics`.`products` (
  `gtin14` CHAR(14) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `description` VARCHAR(4095) NULL,
  `current_price` INT NOT NULL,
  `qty_in_stock` INT NOT NULL,
  PRIMARY KEY (`gtin14`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `online_shop_logistics`.`locations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `online_shop_logistics`.`locations` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `city` VARCHAR(31) NOT NULL,
  `road_name` VARCHAR(31) NOT NULL,
  `place_no` VARCHAR(7) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `location_UNIQUE` (`city` ASC, `road_name` ASC, `place_no` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `online_shop_logistics`.`customer_locations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `online_shop_logistics`.`customer_locations` (
  `customer_id` INT NOT NULL,
  `location_id` INT NOT NULL,
  PRIMARY KEY (`customer_id`, `location_id`),
  INDEX `location_id_idx` (`location_id` ASC),
  CONSTRAINT `fk_customer_locations_customer_id`
    FOREIGN KEY (`customer_id`)
    REFERENCES `online_shop_logistics`.`customers` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_customer_locations_location_id`
    FOREIGN KEY (`location_id`)
    REFERENCES `online_shop_logistics`.`locations` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `online_shop_logistics`.`customer_orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `online_shop_logistics`.`customer_orders` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `customer_id` INT NOT NULL,
  `datetime_ordered` DATETIME NOT NULL,
  `delivery_date` DATE NOT NULL,
  `delivery_location` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `customer_order_UNIQUE` (`customer_id` ASC, `datetime_ordered` ASC, `delivery_date` ASC, `delivery_location` ASC),
  INDEX `customer_location_idx` (`customer_id` ASC, `delivery_location` ASC),
  CONSTRAINT `fk_customer_orders_customer_location`
    FOREIGN KEY (`customer_id` , `delivery_location`)
    REFERENCES `online_shop_logistics`.`customer_locations` (`customer_id` , `location_id`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `online_shop_logistics`.`customer_order_items`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `online_shop_logistics`.`customer_order_items` (
  `customer_order_id` INT NOT NULL,
  `product_gtin14` CHAR(14) NOT NULL,
  `qty_bought` INT NOT NULL,
  `total_price_paid` INT NOT NULL,
  PRIMARY KEY (`customer_order_id`, `product_gtin14`),
  INDEX `product_id_idx` (`product_gtin14` ASC),
  CONSTRAINT `fk_order_items_customer_order_id`
    FOREIGN KEY (`customer_order_id`)
    REFERENCES `online_shop_logistics`.`customer_orders` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_order_items_product_id`
    FOREIGN KEY (`product_gtin14`)
    REFERENCES `online_shop_logistics`.`products` (`gtin14`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `online_shop_logistics`.`company_orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `online_shop_logistics`.`company_orders` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `product_gtin14` CHAR(14) NOT NULL,
  `datetime_ordered` DATETIME NOT NULL,
  `qty_bought` INT NOT NULL,
  `total_price_paid` INT NOT NULL,
  `delivery_date` DATE NOT NULL,
  PRIMARY KEY (`id`, `product_gtin14`),
  UNIQUE INDEX `company_order_UNIQUE` (`product_gtin14` ASC, `datetime_ordered` ASC, `qty_bought` ASC, `delivery_date` ASC),
  CONSTRAINT `fk_company_orders_product_id`
    FOREIGN KEY (`product_gtin14`)
    REFERENCES `online_shop_logistics`.`products` (`gtin14`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
