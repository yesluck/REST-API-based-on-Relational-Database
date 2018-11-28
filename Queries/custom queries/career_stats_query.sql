select C.playerid, C.teamid, C.yearid, C.g_all, C.hits, C.ABs, D.A as Assists, D.E as `errors` from (
	(select A.playerid as playerid, A.teamid as teamid, A.yearid as yearid, A.g_all as g_all, B.H as hits, B.AB as ABs from(
			(select yearid, teamid, playerid, g_all from appearances where playerid = 'willite01') as A
			left join
			(select playerid, yearid, H, AB from batting where playerid = 'willite01') as B
			on A.playerid=b.playerid and A.yearid=B.yearid)) as C
	left join
    (select * from fielding) as D
    on C.playerid=D.playerid and C.yearid=D.yearid)