import pymysql
import SimpleBO

cnx = pymysql.connect(host='localhost',
                              user='root',
                              password='database',
                              db='lahman2017raw',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)

def teammates(value, offset=None, limit=None, pagi=True):
    res = {}
    cursor = cnx.cursor()
    q = "select ori as player, playerid, min(yearid) as firstYear, max(yearid) as lastYear, count(yearid) as countOfSeason from\
            (select B.playerID as ori, C.yearid, C.teamid, C.playerid from\
                (select yearid, teamid, playerid from appearances where playerid = '" + value[0] + "') as B\
                join\
                (select yearid, teamid, playerid from appearances where teamid in (select teamid from (select * from appearances where playerid = 'willite01') as A)) as C\
                on B.yearID = C.yearID ) as D\
            group by playerid"
    q0 = "select count(*) from (" + q + ") as E"
    cursor.execute(q0)
    length = cursor.fetchone()["count(*)"]

    if pagi:
        q += " limit "
        q += limit[0] if limit else "10"
        q += " offset "
        q += offset[0] if limit else "0"
    cursor.execute(q)
    if not pagi:
        return cursor.fetchall()
    else:
        res["data"] = cursor.fetchall()
        res["links"] = SimpleBO.generate_pagination(resource="teammates/" + value[0], t=None, fields=None, length=length, offset=offset, limit=limit)
        return res

def career_stats(value, offset=None, limit=None, pagi=True):
    res = {}
    cursor = cnx.cursor()
    q = "select C.playerid, C.teamid, C.yearid, C.g_all, C.hits, C.ABs, D.A as Assists, D.E as `errors` from (\
            (select A.playerid as playerid, A.teamid as teamid, A.yearid as yearid, A.g_all as g_all, B.H as hits, B.AB as ABs from(\
                    (select yearid, teamid, playerid, g_all from appearances where playerid = '" + value[0] + "') as A\
                    left join\
                    (select playerid, yearid, H, AB from batting where playerid = '" + value[0] + "') as B\
                    on A.playerid=b.playerid and A.yearid=B.yearid)) as C\
            left join\
            (select * from fielding) as D\
            on C.playerid=D.playerid and C.yearid=D.yearid)"
    q0 = "select count(*) from (" + q + ") as E"
    cursor.execute(q0)
    length = cursor.fetchone()["count(*)"]

    if pagi:
        q += " limit "
        q += limit[0] if limit else "10"
        q += " offset "
        q += offset[0] if limit else "0"
    cursor.execute(q)
    if not pagi:
        return cursor.fetchall()
    else:
        res["data"] = cursor.fetchall()
        res["links"] = SimpleBO.generate_pagination(resource="people/" + value[0] + "/career_stats", t=None, fields=None,
                                                    length=length, offset=offset, limit=limit)
        return res

def roster(value, offset=None, limit=None, pagi=True):
    res = {}
    cursor = cnx.cursor()
    q = "select E.nameLast, E.nameFirst, E.playerid, E.teamid, E.yearid, E.g_all, E.hits, E.abs, cast(sum(F.A) as signed) attempts, cast(sum(F.E) as signed) `errors` from(\
            (select C.nameLast, C.nameFirst, C.playerid, C.teamid, C.yearid, C.g_all, D.H as hits, D.AB as abs from(\
                (select B.nameLast, B.nameFirst, B.playerid, A.teamid, A.yearid, A.g_all from(\
                    (select yearid, teamid, playerid, g_all from appearances where teamid='" + value['teamid'][0] + "' and yearid='" + value['yearid'][0] + "') as A\
                    join\
                    (select nameFirst, nameLast, playerid from people) as B\
                    on A.playerid=B.playerid\
                    )) as C\
                left join\
                (select playerid, yearid, teamid, H, AB from batting) as D\
                on C.playerid=D.playerid and C.yearid=D.yearid and C.teamid=D.teamid\
                )) as E\
            join\
            (select playerid, yearid, teamid, A, E from fielding) as F\
            on E.playerid=F.playerid and E.yearid=F.yearid and E.teamid=F.teamid)\
        group by E.playerid,E.hits,E.g_all,E.abs"
    q0 = "select count(*) from (" + q + ") as E"
    cursor.execute(q0)
    length = cursor.fetchone()["count(*)"]

    if pagi:
        q += " limit "
        q += limit[0] if limit else "10"
        q += " offset "
        q += offset[0] if limit else "0"
    cursor.execute(q)
    if not pagi:
        return cursor.fetchall()
    else:
        res["data"] = cursor.fetchall()
        res["links"] = SimpleBO.generate_pagination(resource="roster", t=value,
                                                    fields=None,
                                                    length=length, offset=offset, limit=limit)
        return res
