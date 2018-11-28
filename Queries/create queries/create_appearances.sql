CREATE TABLE `Appearances` (
  `yearID` varchar(4) NOT NULL,
  `teamID` varchar(3) NOT NULL,
  `lgID` text,
  `playerID` varchar(12) NOT NULL,
  `G_all` text,
  `GS` text,
  `G_batting` text,
  `G_defense` text,
  `G_p` text,
  `G_c` text,
  `G_1b` text,
  `G_2b` text,
  `G_3b` text,
  `G_ss` text,
  `G_lf` text,
  `G_cf` text,
  `G_rf` text,
  `G_of` text,
  `G_dh` text,
  `G_ph` text,
  `G_pr` text,
  PRIMARY KEY (`playerID`,`yearID`,`teamID`),
  KEY `FK-team` (`teamID`),
  KEY `FK-year` (`yearID`),
  CONSTRAINT `FK-player` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerid`),
  CONSTRAINT `FK-team` FOREIGN KEY (`teamID`) REFERENCES `teams` (`teamid`),
  CONSTRAINT `FK-year` FOREIGN KEY (`yearID`) REFERENCES `teams` (`yearid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;