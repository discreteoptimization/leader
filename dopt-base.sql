SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `dopt` DEFAULT CHARACTER SET latin1 ;
USE `dopt` ;

-- -----------------------------------------------------
-- Table `dopt`.`assignment`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `dopt`.`assignment` (
  `assignmentID` INT(11) NOT NULL AUTO_INCREMENT ,
  `assignmentName` VARCHAR(512) NOT NULL ,
  `sense` INT(2) NOT NULL DEFAULT '0' ,
  PRIMARY KEY (`assignmentID`) )
ENGINE = MyISAM
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `dopt`.`problem`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `dopt`.`problem` (
  `problemID` INT(11) NOT NULL AUTO_INCREMENT ,
  `partID` VARCHAR(64) NOT NULL ,
  `partNumber` INT(5) NOT NULL ,
  `problemName` VARCHAR(512) NOT NULL ,
  `problemNameLong` VARCHAR(512) NOT NULL ,
  `grade1` INT(11) NOT NULL ,
  `grade2` INT(11) NOT NULL ,
  PRIMARY KEY (`problemID`) )
ENGINE = MyISAM
AUTO_INCREMENT = 51
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `dopt`.`leader`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `dopt`.`leader` (
  `ID` BIGINT(20) NOT NULL AUTO_INCREMENT ,
  `courseraUserID` INT(11) NOT NULL ,
  `assignmentID` INT(11) NOT NULL ,
  `partID` VARCHAR(64) NOT NULL ,
  `quality` DOUBLE NOT NULL ,
  `proof` INT(3) NOT NULL ,
  `time` DOUBLE NOT NULL ,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
  PRIMARY KEY (`ID`) ,
  INDEX `sort` (`quality` ASC, `proof` ASC, `timestamp` ASC) ,
  INDEX `parts` (`partID` ASC) ,
  INDEX `assignments` (`assignmentID` ASC) )
ENGINE = MyISAM
AUTO_INCREMENT = 199101
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `dopt`.`leader_2`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `dopt`.`leader_2` (
  `ID` BIGINT(20) NOT NULL AUTO_INCREMENT ,
  `courseraUserID` INT(11) NOT NULL ,
  `assignmentID` INT(11) NOT NULL ,
  `partID` VARCHAR(64) NOT NULL ,
  `fileName` VARCHAR(64) NOT NULL ,
  `quality` DOUBLE NOT NULL ,
  `proof` INT(3) NOT NULL ,
  `time` DOUBLE NOT NULL ,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
  PRIMARY KEY (`ID`) ,
  INDEX `sort` (`quality` ASC, `proof` ASC, `timestamp` ASC) ,
  INDEX `parts` (`partID` ASC) ,
  INDEX `assignments` (`assignmentID` ASC) , 
  INDEX `files` (`fileName` ASC) )
ENGINE = MyISAM
AUTO_INCREMENT = 199101
DEFAULT CHARACTER SET = utf8;



-- -----------------------------------------------------
-- Table `dopt`.`submission`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `dopt`.`submission` (
  `submissionID` BIGINT(20) NOT NULL AUTO_INCREMENT ,
  `courseraUserID` INT(11) NOT NULL ,
  `assignmentID` INT(11) NOT NULL ,
  `partID` VARCHAR(64) NOT NULL ,
  `subtime` INT(16) NOT NULL ,
  `feedbackCode` INT(11) NOT NULL ,
  `grade` INT(11) NOT NULL ,
  `leaderID` BIGINT(20) NULL DEFAULT NULL ,
  `quality` DOUBLE NULL DEFAULT NULL ,
  `proof` INT(3) NULL DEFAULT NULL ,
  `time` DOUBLE NULL DEFAULT NULL ,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ,
  PRIMARY KEY (`submissionID`) ,
  INDEX `userassignmentpart` (`courseraUserID` ASC, `assignmentID` ASC, `partID` ASC) ,
  INDEX `user` (`courseraUserID` ASC) ,
  INDEX `assignments` (`assignmentID` ASC) ,
  INDEX `parts` (`partID` ASC) )
ENGINE = MyISAM
AUTO_INCREMENT = 471639
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `dopt`.`submission_2`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `dopt`.`submission_2` (
  `submissionID` BIGINT(20) NOT NULL AUTO_INCREMENT ,
  `courseraUserID` INT(11) NOT NULL ,
  `assignmentID` INT(11) NOT NULL ,
  `partID` VARCHAR(64) NOT NULL ,
  `fileName` VARCHAR(64) NOT NULL ,
  `subtime` INT(16) NOT NULL ,
  `feedbackCode` INT(11) NOT NULL ,
  `grade` INT(11) NOT NULL ,
  `leaderID` BIGINT(20) NULL DEFAULT NULL ,
  `quality` DOUBLE NULL DEFAULT NULL ,
  `proof` INT(3) NULL DEFAULT NULL ,
  `time` DOUBLE NULL DEFAULT NULL ,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ,
  PRIMARY KEY (`submissionID`) ,
  INDEX `userassignmentpart` (`courseraUserID` ASC, `assignmentID` ASC, `partID` ASC, `fileName` ASC) ,
  INDEX `user` (`courseraUserID` ASC) ,
  INDEX `assignments` (`assignmentID` ASC) ,
  INDEX `parts` (`partID` ASC) ,
  INDEX `files` (`fileName` ASC) )
ENGINE = MyISAM
AUTO_INCREMENT = 471639
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `dopt`.`user`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `dopt`.`user` (
  `userID` INT(11) NOT NULL AUTO_INCREMENT ,
  `courseraUserID` INT(11) NOT NULL ,
  `userName` VARCHAR(128) NOT NULL ,
  PRIMARY KEY (`userID`) )
ENGINE = MyISAM
AUTO_INCREMENT = 44944
DEFAULT CHARACTER SET = utf8;

USE `dopt` ;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `dopt`.`assignment`
-- -----------------------------------------------------
START TRANSACTION;
USE `dopt`;
INSERT INTO `dopt`.`assignment` (`assignmentID`, `assignmentName`, `sense`) VALUES (1, 'Knapsack', 1);
INSERT INTO `dopt`.`assignment` (`assignmentID`, `assignmentName`, `sense`) VALUES (2, 'Graph Coloring', 0);
INSERT INTO `dopt`.`assignment` (`assignmentID`, `assignmentName`, `sense`) VALUES (3, 'Traveling Salesman', 0);
INSERT INTO `dopt`.`assignment` (`assignmentID`, `assignmentName`, `sense`) VALUES (4, 'Warehouse Location', 0);
INSERT INTO `dopt`.`assignment` (`assignmentID`, `assignmentName`, `sense`) VALUES (5, 'Vehicle Routing', 0);
INSERT INTO `dopt`.`assignment` (`assignmentID`, `assignmentName`, `sense`) VALUES (6, 'Puzzle Challenge', 1);

COMMIT;

-- -----------------------------------------------------
-- Data for table `dopt`.`problem`
-- -----------------------------------------------------
START TRANSACTION;
USE `dopt`;
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (1, 'UB1HKrQ7', 1, 'Knapsack 1', 'Knapsack Problem 1', 92000, 99798);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (2, 'u6sleLfT', 2, 'Knapsack 2', 'Knapsack Problem 2', 141956, 142156);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (3, 'DLtBFO66', 3, 'Knapsack 3', 'Knapsack Problem 3', 100062, 100236);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (4, 'zVGvzWRJ', 4, 'Knapsack 4', 'Knapsack Problem 4', 3966813, 3967028);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (5, 'yD06cKUp', 5, 'Knapsack 5', 'Knapsack Problem 5', 109869, 109899);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (6, 'MLjl5jzP', 6, 'Knapsack 6', 'Knapsack Problem 6', 1099870, 1099881);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (7, 'upNcCDtk', 1, 'Coloring 1', 'Coloring Problem 1', 8, 6);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (8, 'Cy6WMCm7', 2, 'Coloring 2', 'Coloring Problem 2', 20, 17);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (9, 'UOKSlXMq', 3, 'Coloring 3', 'Coloring Problem 3', 21, 16);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (10, 'ecjBwfpP', 4, 'Coloring 4', 'Coloring Problem 4', 95, 78);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (11, 'a10G1b1U', 5, 'Coloring 5', 'Coloring Problem 5', 18, 16);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (12, 'pIzekcCG', 6, 'Coloring 6', 'Coloring Problem 6', 124, 100);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (13, 'WdrlJtJq', 1, 'TSP 1', 'Traveling Salesman Problem 1', 482, 430);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (14, 'dTewhF6o', 2, 'TSP 2', 'Traveling Salesman Problem 2', 23433, 20800);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (15, 'OlJBvw72', 3, 'TSP 3', 'Traveling Salesman Problem 3', 35985, 30000);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (16, 'KZQYdfck', 4, 'TSP 4', 'Traveling Salesman Problem 4', 40000, 37600);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (17, 'vViyejW4', 5, 'TSP 5', 'Traveling Salesman Problem 5', 378069, 323000);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (18, 'vLKzhJhP', 6, 'TSP 6', 'Traveling Salesman Problem 6', 78478868, 67700000);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (19, '8zVuNh0L', 1, 'WLP 1', 'Warehouse Location Problem 1', 1727125, 976740);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (20, 'eaOs8z3l', 2, 'WLP 2', 'Warehouse Location Problem 2', 1248144, 796650);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (21, 'pxIsuCQe', 3, 'WLP 3', 'Warehouse Location Problem 3', 1153610, 793441);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (22, 'clCLq0Vb', 4, 'WLP 4', 'Warehouse Location Problem 4', 26311921, 17765203);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (23, '2gHetJOV', 5, 'WLP 5', 'Warehouse Location Problem 5', 3897, 2688);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (24, 'ASSX0Lq4', 6, 'WLP 6', 'Warehouse Location Problem 6', 4485, 2610);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (25, 'OXs89Owz', 7, 'WLP 7', 'Warehouse Location Problem 7', 9094, 6120);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (26, 'AO0FA8y8', 8, 'WLP 8', 'Warehouse Location Problem 8', 17378, 13000);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (27, 'AbP3LXz3', 0, 'VRP 1', 'Vehicle Routing Problem 1', 387, 280);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (28, 'qUskNlyI', 1, 'VRP 2', 'Vehicle Routing Problem 2', 1019, 630);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (29, 'WrJzs7t7', 2, 'VRP 3', 'Vehicle Routing Problem 3', 713, 540);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (30, 'Fhfahwgd', 3, 'VRP 4', 'Vehicle Routing Problem 4', 1193, 830);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (31, 'i5cdcvuF', 4, 'VRP 5', 'Vehicle Routing Problem 5', 3719, 1400);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (32, 'kIKqylL1', 5, 'VRP 6', 'Vehicle Routing Problem 6', 2392, 2000);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (33, '1SxQohvJ', 0, 'N-Queens', 'N-Queens', -100, 32768);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (34, 's8Mt3ofs', 1, 'All Interval Series', 'All Interval Series', -100, 1048576);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (35, 'MfTvElXE', 2, 'Magic Series', 'Magic Series', -100, 1048576);
INSERT INTO `dopt`.`problem` (`problemID`, `partID`, `partNumber`, `problemName`, `problemNameLong`, `grade1`, `grade2`) VALUES (36, 'mBtMalnR', 3, 'Magic Square', 'Magic Square', -1, 1024);

COMMIT;


START TRANSACTION;

CREATE USER 'coursera'@'%' IDENTIFIED BY 'optimization is fun';
GRANT SELECT ON `dopt`.* TO 'coursera'@'%';
GRANT INSERT, UPDATE ON `dopt`.`leader` TO 'coursera'@'%';
GRANT INSERT, UPDATE ON `dopt`.`leader_2` TO 'coursera'@'%';
GRANT INSERT, UPDATE ON `dopt`.`submission` TO 'coursera'@'%';
GRANT INSERT, UPDATE ON `dopt`.`submission_2` TO 'coursera'@'%';
GRANT INSERT, UPDATE ON `dopt`.`user` TO 'coursera'@'%';

COMMIT;
