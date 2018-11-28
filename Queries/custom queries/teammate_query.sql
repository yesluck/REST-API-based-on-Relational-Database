select ori as player, playerid, min(yearid) as firstYear, max(yearid) as lastYear, count(yearid) as countOfSeason from
(select B.playerID as ori, C.yearid, C.teamid, C.playerid from
	(select yearid, teamid, playerid from appearances where playerid = 'willite01') as B
	join
	(select yearid, teamid, playerid from appearances where teamid in (select teamid from (select * from appearances where playerid = 'willite01') as A)) as C
    on B.yearID = C.yearID ) as D
group by playerid