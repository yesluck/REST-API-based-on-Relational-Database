select E.nameLast, E.nameFirst, E.playerid, E.teamid, E.yearid, E.g_all, E.hits, E.abs, cast(sum(F.A) as signed) attempts, cast(sum(F.E) as signed) `errors` from(
	(select C.nameLast, C.nameFirst, C.playerid, C.teamid, C.yearid, C.g_all, D.H as hits, D.AB as abs from(
		(select B.nameLast, B.nameFirst, B.playerid, A.teamid, A.yearid, A.g_all from(
			(select yearid, teamid, playerid, g_all from appearances where teamid='BOS' and yearid='2004') as A
			join
			(select nameFirst, nameLast, playerid from people) as B
			on A.playerid=B.playerid
			)) as C
		left join
		(select playerid, yearid, teamid, H, AB from batting) as D
		on C.playerid=D.playerid and C.yearid=D.yearid and C.teamid=D.teamid
		)) as E
	join
    (select playerid, yearid, teamid, A, E from fielding) as F
	on E.playerid=F.playerid and E.yearid=F.yearid and E.teamid=F.teamid)
group by E.playerid,E.hits,E.g_all,E.abs