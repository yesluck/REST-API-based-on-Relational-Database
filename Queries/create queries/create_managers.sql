CREATE TABLE `Managers` (
  `playerID` varchar(12) NOT NULL,
  `yearID` varchar(4) NOT NULL,
  `teamID` varchar(3) NOT NULL,
  `lgID` text,
  `inseason` varchar(1) NOT NULL,
  `G` text,
  `W` text,
  `L` text,
  `rank` text,
  `plyrMgr` text,
  PRIMARY KEY (`playerID`,`yearID`,`teamID`,`inseason`),
  KEY `FK-mana-team` (`teamID`),
  KEY `FK-mana-year` (`yearID`),
  CONSTRAINT `FK-mana-player` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerid`),
  CONSTRAINT `FK-mana-team` FOREIGN KEY (`teamID`) REFERENCES `teams` (`teamid`),
  CONSTRAINT `FK-mana-year` FOREIGN KEY (`yearID`) REFERENCES `teams` (`yearid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
