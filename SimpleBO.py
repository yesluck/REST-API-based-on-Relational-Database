import pymysql
import json

cnx = pymysql.connect(host='localhost',
                              user='root',
                              password='database',
                              db='lahman2017raw',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)


## This function checks whether the keys of the “template” and “fields” are the rows in the table. If not, it will raise an error.
def check(resource, template=None, fields=None):
    try:
        cursor = cnx.cursor()
        if template:
            keySet = list(template.keys())
        elif fields:
            keySet = fields[0].split(',')
        for key in keySet:
            cursor.execute(
                "select count(*) from information_schema.columns where table_name = '" + resource + "' and column_name = '" + key + "'")
            data = cursor.fetchall()[0]['count(*)']
            if data == 0:
                if template:
                    raise NameError('The template/row contains a column/attribute name not in the file!')
                elif fields:
                    raise NameError('The field contains a column/attribute name not in the file!')
    except Exception as e:
        print("Exception  in insert, e = ", e)
        raise Exception("Boom! Original = ", e)


def fieldsToSelectClause(resource, fields):
    if not fields:
        return "*"
    check(resource, fields=fields)
    s = ""
    for f in fields:
        if s != "":
            s += ", "
        s += f
    return s


def find_by_primary_key(resource, values, fields=None, offset=None, limit=None):
    try:
        cursor = cnx.cursor()
        cursor.execute("SHOW KEYS FROM " + resource + " WHERE Key_name = 'PRIMARY'")
        data = [i["Column_name"] for i in cursor.fetchall()]
        t = {}
        for i, k in enumerate(data):
            ls = []
            ls.append(values[i])
            t[k] = ls
        return find_by_template(resource, t, fields, pagi=False)
    except Exception as e:
        print("Exception  in insert, e = ", e)
        raise Exception("Boom! Original = ", e)


def templateToWhereClause(t):
    s = ""
    for (k, v) in t.items():
        if s != "":
            s += " AND "
        s += k + "='" + v[0] + "'"
    if s != "":
        s = "WHERE " + s
    return s


# This function is used to generate pagination links and structures. Particularly, if we are in the first page of the results,
# it will not show “previous” url; if we are in the next page of the results, it will not show “next” url; if we are
# calling find_by_primary_key() function, all links will not be shown, since find_by_primary_key() will definitely show 0 or 1
# result, which will definitely be shown in one page.
def generate_pagination(resource, t, fields, length, offset, limit):
    links = []
    previous = {}
    current = {}
    next = {}
    if limit:
        limit_int = int(limit[0])
    else:
        limit_int = None
    prefix = "/api/" + resource + "?"
    if t:
        for tmp in t:
            prefix += tmp + "=" + t[tmp][0] + "&"
    if fields:
        prefix += "fields="
        for i, fld in enumerate(fields):
            prefix += fields[i]
            if i < len(fields) - 1:
                prefix += ","
        prefix += "&"
    if offset == None or offset == ['0']:
        previous_q = None
        current_q = prefix + "offset=0&limit="
        if length > 10:
            next_q = prefix + "offset=10&limit="
        else:
            next_q = None
    else:
        previous_q = prefix + "offset=" + str(max(0, int(offset[0]) - (10 if limit == None else limit_int))) + "&limit="
        current_q = prefix + "offset=" + offset[0] + "&limit="
        if int(offset[0]) + limit_int < length:
            next_q = prefix + "offset=" + str(int(offset[0]) + (10 if limit == None else limit_int)) + "&limit="
        else:
            next_q = None
    if limit == None:
        if previous_q:
            previous_q += "10"
        current_q += "10"
        if next_q:
            next_q += "10"
    else:
        if previous_q:
            previous_q += str(limit_int)
        current_q += "10"
        if next_q:
            next_q += str(limit_int)
    if previous_q:
        previous["previous"] = previous_q
        links.append(previous)
    current["current"] = current_q
    links.append(current)
    if next_q:
        next["next"] = next_q
        links.append(next)
    return links


def find_by_template(resource, t, fields=None, offset=None, limit=None, pagi=True):
    try:
        check(resource, template=t)
        res = {}
        cursor = cnx.cursor()
        q = "select " + fieldsToSelectClause(resource, fields) + " from " + resource + " " + templateToWhereClause(t)
        cursor.execute("select count(*) from " + resource + " " + templateToWhereClause(t))
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
            res["links"] = generate_pagination(resource, t, fields, length, offset, limit)
            return res
    except Exception as e:
        print("Exception  in insert, e = ", e)
        raise Exception("Boom! Original = ", e)


def insert(resource, body):
    try:
        keys = body.keys()
        q = "INSERT into " + resource + " "
        s1 = list(body.keys())
        s1 = ",".join(s1)
        q += "(" + s1 + ") "
        v = ["%s"] * len(keys)
        v = ",".join(v)
        q += "values(" + v + ")"
        params = tuple(body.values())
        cursor = cnx.cursor()
        cursor.execute(q, params)
        # cnx.commit()
    except Exception as e:
        print("Exception  in insert, e = ", e)
        raise Exception("Boom! Original = ", e)


def delete(resource, values):
    try:
        cursor = cnx.cursor()
        cursor.execute("SHOW KEYS FROM " + resource + " WHERE Key_name = 'PRIMARY'")
        data = [i["Column_name"] for i in cursor.fetchall()]
        t = {}
        for i, k in enumerate(data):
            ls = []
            ls.append(values[i])
            t[k] = ls
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM " + resource + " " + templateToWhereClause(t))
        # cnx.commit()
    except Exception as e:
        print("Exception  in insert, e = ", e)
        raise Exception("Boom! Original = ", e)


def templateToSetClause(t):
    s = ""
    for (k, v) in t.items():
        if s != "":
            s += ", "
        s += k + "='" + v + "'"
    return s


def update(resource, values, body):
    try:
        cursor = cnx.cursor()
        cursor.execute("SHOW KEYS FROM " + resource + " WHERE Key_name = 'PRIMARY'")
        data = [i["Column_name"] for i in cursor.fetchall()]
        t = {}
        for i, k in enumerate(data):
            ls = []
            ls.append(values[i])
            t[k] = ls
        cursor.execute("UPDATE " + resource + " SET" + " " + templateToSetClause(body) + " " + templateToWhereClause(t))
        # cnx.commit()
    except Exception as e:
        print("Exception  in insert, e = ", e)
        raise Exception("Boom! Original = ", e)


def related_get(resource, values, related, rt, fields=None, offset=None, limit=None):
    try:
        cursor = cnx.cursor()
        cursor.execute("SHOW KEYS FROM " + resource + " WHERE Key_name = 'PRIMARY'")
        data = [i["Column_name"] for i in cursor.fetchall()]
        cursor = cnx.cursor()
        cursor.execute("select COLUMN_NAME from INFORMATION_SCHEMA.KEY_COLUMN_USAGE where REFERENCED_TABLE_NAME=\'"+ resource + "\' and table_name = \'" + related + "\'")
        cols = cursor.fetchall()
        cursor.execute("select COLUMN_NAME from INFORMATION_SCHEMA.KEY_COLUMN_USAGE where REFERENCED_TABLE_NAME=\'" + related + "\' and table_name = \'" + resource + "\'")
        cols_rev = cursor.fetchall()
        all_fks = ([] if len(cols) == 0 else cols) + ([] if len(cols_rev) == 0 else cols_rev)
        if len(all_fks) == 0:
            raise NameError("There are no foreign key constraints between the two tables!")
        t = {}
        for i, k in enumerate(data):
            ls = []
            ls.append(values[i])
            t[k] = ls
        s = ""
        for i, col in enumerate(all_fks):
            s += col['COLUMN_NAME']
            if i != len(all_fks) - 1:
                s += ","
        cursor.execute("select " + s + " from (select * from " + resource + " " + templateToWhereClause(t) + ") as A")
        rt1 = cursor.fetchone()
        if rt1:
            for k in rt1.keys():
                rt1[k] = [rt1[k]]
        else:
            return []
        return find_by_template(related, {**rt1, **rt}, fields)
    except Exception as e:
        print("Exception  in insert, e = ", e)
        raise Exception("Boom! Original = ", e)


def related_post(resource, values, related, body):
    try:
        cursor = cnx.cursor()
        cursor.execute("select column_name from information_schema.columns where table_name = '" + resource + "'")
        data = set(i["COLUMN_NAME"] for i in cursor.fetchall())
        cursor = cnx.cursor()
        cursor.execute("select column_name from information_schema.columns where table_name = '" + related + "'")
        data_rel = set(i["COLUMN_NAME"] for i in cursor.fetchall())
        resource_line = find_by_primary_key(resource, values)
        if len(resource_line) == 0:
            raise NameError("Wrong primary key!")
        t = {}
        for f in data.intersection(data_rel):
            t[f] = resource_line[0][f]
        insert(related, {**t, **body})
    except Exception as e:
        print("Exception  in insert, e = ", e)
        raise Exception("Boom! Original = ", e)

