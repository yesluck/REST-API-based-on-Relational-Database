-- People -- 

ALTER TABLE `lahman2017raw`.`people`  CHANGE COLUMN `playerID` `playerID` VARCHAR(12) NOT NULL;
ALTER TABLE `People` ADD PRIMARY KEY ( `playerID` );

-- Batting --

select playerID, yearID, teamID, stint, count(*) as count_of_rows from batting  group by playerID, yearID, teamID, stint order by count_of_rows desc limit 10;

ALTER TABLE `lahman2017raw`.`Batting` 
CHANGE COLUMN `playerID` `playerID` VARCHAR(12) NOT NULL,
CHANGE COLUMN `yearID` `yearID` VARCHAR(4) NOT NULL,
CHANGE COLUMN `stint` `stint` VARCHAR(1) NOT NULL,
CHANGE COLUMN `teamID` `teamID` VARCHAR(3) NOT NULL;

ALTER TABLE `Batting` ADD PRIMARY KEY ( playerID, yearID, stint );

-- Appearances --

select playerID, yearID, teamID, count(*) as count_of_rows from appearances  group by playerID, yearID, teamID order by count_of_rows desc limit 10;

ALTER TABLE `lahman2017raw`.`Appearances` 
CHANGE COLUMN `yearID` `yearID` VARCHAR(4) NOT NULL,
CHANGE COLUMN `teamID` `teamID` VARCHAR(3) NOT NULL,
CHANGE COLUMN `playerID` `playerID` VARCHAR(12) NOT NULL;

ALTER TABLE `Appearances` ADD PRIMARY KEY ( playerID, yearID, teamID);

-- Managers --

select playerID,yearID, teamID, inseason, count(*) as count_of_rows from managers  group by playerID,yearID,teamID,inseason order by count_of_rows desc limit 100;

ALTER TABLE `lahman2017raw`.`Managers` 
CHANGE COLUMN `playerID` `playerID` VARCHAR(12) NOT NULL,
CHANGE COLUMN `yearID` `yearID` VARCHAR(4) NOT NULL,
CHANGE COLUMN `teamID` `teamID` VARCHAR(3) NOT NULL,
CHANGE COLUMN `inseason` `inseason` VARCHAR(1) NOT NULL;

ALTER TABLE `Managers` ADD PRIMARY KEY (playerID,yearID, teamID, inseason);

-- Fielding --

describe fielding;
select * from fielding;
select playerID, yearID, stint, pos, count(*) as count_of_rows from fielding  group by playerID, yearID, stint, pos order by count_of_rows desc limit 100;

SET SQL_SAFE_UPDATES = 0;
update `Fielding` set `G` = NULL WHERE `G` = "";
update `Fielding` set `GS` = NULL WHERE `GS` = "";
update `Fielding` set `InnOuts` = NULL WHERE `InnOuts` = "";
update `Fielding` set `PO` = NULL WHERE `PO` = "";
update `Fielding` set `A` = NULL WHERE `A` = "";
update `Fielding` set `E` = NULL WHERE `E` = "";
update `Fielding` set `DP` = NULL WHERE `DP` = "";
update `Fielding` set `PB` = NULL WHERE `PB` = "";
update `Fielding` set `WP` = NULL WHERE `WP` = "";
update `Fielding` set `SB` = NULL WHERE `SB` = "";
update `Fielding` set `CS` = NULL WHERE `CS` = "";
update `Fielding` set `ZR` = NULL WHERE `ZR` = "";

ALTER TABLE `lahman2017raw`.`Fielding` 
CHANGE COLUMN `playerID` `playerID` VARCHAR(12)  NOT NULL,
CHANGE COLUMN `yearID` `yearID` VARCHAR(4)  NOT NULL,
CHANGE COLUMN `stint` `stint` VARCHAR(1) NOT NULL,
CHANGE COLUMN `teamID` `teamID` VARCHAR(3) NOT NULL,
CHANGE COLUMN `POS` `POS` VARCHAR(2) NOT NULL,
CHANGE COLUMN `G` `G` INT NULL DEFAULT NULL,
CHANGE COLUMN `GS` `GS` INT NULL DEFAULT NULL,
CHANGE COLUMN `InnOuts` `InnOuts` INT NULL DEFAULT NULL,
CHANGE COLUMN `PO` `PO` INT NULL DEFAULT NULL,
CHANGE COLUMN `A` `A` INT NULL DEFAULT NULL,
CHANGE COLUMN `E` `E` INT NULL DEFAULT NULL,
CHANGE COLUMN `DP` `DP` INT NULL DEFAULT NULL,
CHANGE COLUMN `PB` `PB` INT NULL DEFAULT NULL,
CHANGE COLUMN `WP` `WP` INT NULL DEFAULT NULL,
CHANGE COLUMN `SB` `SB` INT NULL DEFAULT NULL,
CHANGE COLUMN `CS` `CS` INT NULL DEFAULT NULL,
CHANGE COLUMN `ZR` `ZR` INT NULL DEFAULT NULL;

ALTER TABLE `Fielding` ADD PRIMARY KEY (playerID, yearID, stint, pos);

-- Teams --

describe teams;
select * from teams;
select yearID, teamID, count(*) as count_of_rows from teams  group by yearID, teamID order by count_of_rows desc limit 100;

ALTER TABLE `lahman2017raw`.`Teams` 
CHANGE COLUMN `yearID` `yearID` VARCHAR(4) ,
CHANGE COLUMN `teamID` `teamID` VARCHAR(3);

ALTER TABLE `Teams` ADD PRIMARY KEY (yearID, teamID);


-- foreign keys --

ALTER TABLE `lahman2017raw`.`Batting` 
ADD CONSTRAINT `FK_player`
  FOREIGN KEY (`playerID`)
  REFERENCES `lahman2017raw`.`people` (`playerID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
  
ALTER TABLE `lahman2017raw`.`Teams` 
ADD INDEX `teamid_idx` (`teamID` ASC) VISIBLE;

ALTER TABLE `lahman2017raw`.`Batting` 
ADD CONSTRAINT `FK_teams`
  FOREIGN KEY (`teamID`)
  REFERENCES `lahman2017raw`.`Teams` (`teamID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `lahman2017raw`.`Batting` 
ADD CONSTRAINT `FK_years`
  FOREIGN KEY (`yearID`)
  REFERENCES `lahman2017raw`.`Teams` (`yearID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;


ALTER TABLE `lahman2017raw`.`Appearances` 
ADD CONSTRAINT `FK-player`
  FOREIGN KEY (`playerID`)
  REFERENCES `lahman2017raw`.`people` (`playerID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `FK-team`
  FOREIGN KEY (`teamID`)
  REFERENCES `lahman2017raw`.`Teams` (`teamID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `FK-year`
  FOREIGN KEY (`yearID`)
  REFERENCES `lahman2017raw`.`Teams` (`yearID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;


ALTER TABLE `lahman2017raw`.`Managers` 
ADD CONSTRAINT `FK-mana-player`
  FOREIGN KEY (`playerID`)
  REFERENCES `lahman2017raw`.`people` (`playerID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `FK-mana-team`
  FOREIGN KEY (`teamID`)
  REFERENCES `lahman2017raw`.`Teams` (`teamID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `FK-mana-year`
  FOREIGN KEY (`yearID`)
  REFERENCES `lahman2017raw`.`Teams` (`yearID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;


ALTER TABLE `lahman2017raw`.`Fielding` 
ADD CONSTRAINT `FK-field-player`
  FOREIGN KEY (`playerID`)
  REFERENCES `lahman2017raw`.`people` (`playerID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `FK-field-year`
  FOREIGN KEY (`yearID`)
  REFERENCES `lahman2017raw`.`Teams` (`yearID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `FK-field-team`
  FOREIGN KEY (`teamID`)
  REFERENCES `lahman2017raw`.`Teams` (`teamID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;