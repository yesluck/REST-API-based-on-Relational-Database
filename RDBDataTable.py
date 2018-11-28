import pymysql.cursors
import os

class RDBDataTable:

    module_path = os.path.dirname(__file__)
    data_dir = module_path + "/../../Data/"

    # t_name: The "Name" of the collection.
    # t_file: The name of the CSV file. The class looks in the data_dir for the file.
    def __init__(self, t_name, t_file, key_columns, cnx):
        self.cnx = cnx
        if not isinstance(cnx, pymysql.connections.Connection):
            raise NameError('Please input the right connection!')

        if isinstance(t_name, str):
            self.name = t_name
        else:
            raise NameError("The input file name be a string, please double check your input!")
        if isinstance(t_file, str):
            self.file = self.data_dir + t_file
            cursor = self.cnx.cursor()
            cursor.execute("select * from " + self.name + " limit 100")
            self.rows = cursor.fetchall()
        elif isinstance(t_file, list):
            self.file = "(not from file)"
            self.rows = []
            if len(t_file) > 0:
                for line in t_file:
                    self.rows.append(line)
        else:
            raise NameError("The input file should be a string or dictionary list, please double check your input!")
        self.keyCol = key_columns
        if key_columns and not isinstance(self.keyCol, list):
            raise NameError('Key columns should be a list, please double check your input!')
        cursor = self.cnx.cursor()
        cursor.execute("SHOW KEYS FROM " + self.name + " WHERE Key_name = 'PRIMARY'")
        data = [i["Column_name"] for i in cursor.fetchall()]
        if set(data) != set(self.keyCol):
            print("Warning: The primary key defined in the main function is different from the real primary key!")
            self.keyCol = data

    # Pretty print the CSVTable and its attributes.
    def __str__(self):
        length = len(self.rows)
        if len(self.rows) == 1:
            if list(self.rows[0].values()) == ['' for _ in range(len(list(self.rows[0].values())))]:
                length = 0

        s = ""
        s += "Table Name: " + self.name + "; File Root: " + self.file
        s += "; Key columns: " + str(self.keyCol) + ".\n"
        s += "Column Names" + str(list(self.rows[0].keys())) + ".\n"
        s += "First " + str(min(100,length)) + " row(s):\n"
        col_lst = [i for i in self.rows[0]]
        row_format = "{:<20}" * (len(col_lst) + 1)
        s += row_format.format("", *col_lst) + "\n"
        s += "-" * 20 * (len(col_lst) + 1) + "\n"
        for i, r in enumerate(self.rows):
            if i == 100:
                break
            for item in r.keys():
                if r[item] == None:
                    r[item] = ''
            s += row_format.format("", *list(r.values())) + "\n"
        return s

    # loads the data from the file into the class instance data.
    # You decide how to store and represent the rows from the file.
    def load(self):
        pass

    # Obvious
    def save(self):
        pass

    def check(self, template=None, fields=None):
        cursor = self.cnx.cursor()
        if template:
            keySet = list(template.keys())
        elif fields:
            keySet = fields
        else:
            keySet = self.keyCol
        for key in keySet:
            cursor.execute("select count(*) from information_schema.columns where table_name = '" + self.name + "' and column_name = '" + key + "';")
            data = cursor.fetchall()[0]['count(*)']
            if data == 0:
                if template:
                    raise NameError('The template/row contains a column/attribute name not in the file!')
                elif fields:
                    raise NameError('The field contains a column/attribute name not in the file!')
                else:
                    raise NameError('The primary key contains a column/attribute name not in the file!')


    def fieldsToSelectClause(self, fields):
        if not fields:
            return "*"
        self.check(fields=fields)
        s = ""
        for f in fields:
            if s != "":
                s += ", "
            s += f
        return s

    def primaryKeyToWhereClause(self, values):
        s = ""
        for i, v in enumerate(values):
            if s != "":
                s += " AND "
            s += self.keyCol[i] + "='" + v + "'"
        if s != "":
            s = "WHERE " + s
        return s

    def find_by_primary_key(self, values, fields=None):
        if not isinstance(values, list):
            raise NameError('Primary keys should be a list, please double check your input!')
        if fields and not isinstance(fields, list):
            raise NameError('Field should be a list, please double check your input!')
        if len(self.keyCol) == 0:
            raise NameError("You don't have a primary key!")
        self.check()
        if len(self.keyCol) != len(values):
            raise NameError("The length of the string list is not equal to the supposedly full length of table's primary keys!")
        cursor = self.cnx.cursor()
        cursor.execute("select " + self.fieldsToSelectClause(fields) + " from " + self.name + " " + self.primaryKeyToWhereClause(values) +";")
        res = cursor.fetchall()
        if len(res) == 0:
            res = []
            cursor.execute("select column_name from information_schema.columns where table_name = '" + self.name + "';")
            res.append(dict.fromkeys(fields if fields else [list(i.values())[0] for i in cursor.fetchall()], ""))
        return RDBDataTable(self.name, res, self.keyCol, self.cnx)

    def templateToWhereClause(self, t):
        s = ""
        for (k, v) in t.items():
            if s != "":
                s += " AND "
            s += k + "='" + v + "'"
        if s != "":
            s = "WHERE " + s
        return s

    # The input is:
    # t: The template to match. The result is a list of rows
    # whose attribute/value pairs exactly match the template.
    # fields: A subset of the fields to include for each result.
    # Raises an exception if the template or list of fields contains
    # a column/attribute name not in the file.
    def find_by_template(self, t, fields=None):
        if not isinstance(t, dict):
            raise NameError('Template should be a dictionary, please double check your input!')
        if fields and not isinstance(fields, list):
            raise NameError('Field should be a list, please double check your input!')
        self.check()
        self.check(template=t)
        cursor = self.cnx.cursor()
        cursor.execute("select " + self.fieldsToSelectClause(fields) + " from " + self.name + " " + self.templateToWhereClause(t) + ";")
        res = cursor.fetchall()
        if len(res) == 0:
            res = []
            cursor.execute("select column_name from information_schema.columns where table_name = '" + self.name + "';")
            res.append(dict.fromkeys(fields if fields else [list(i.values())[0] for i in cursor.fetchall()], ""))
        return res

    def templateToIntoClause(self, t):
        s_into = "("
        s_values = "("
        for (k, v) in t.items():
            if s_into != "(":
                s_into += ", "
                s_values += ", "
            s_into += "`" + k + "`"
            s_values += "\'" + v + "\'"
        return s_into + ")", s_values + ")"



    # Inserts the row into the table.
    # Raises on duplicate key or invalid columns.
    def insert(self, r):
        self.check()
        self.check(template=r)
        for k in self.keyCol:
            if k not in r.keys():
                raise NameError('The row MUST contain a value for each primary key field!')
        cursor = self.cnx.cursor()
        cursor.execute("select column_name from information_schema.key_column_usage where table_name = '" + self.name + "';")
        primary_keys = list(cursor.fetchall()[0].values())
        template = {}
        for k in primary_keys:
            template[k] = r[k]
        findrow = self.find_by_template(template).rows[0]
        for k in self.keyCol:
            if findrow[k] == r[k]:
                raise NameError('There already is a row with those primary key values!')
        cursor = self.cnx.cursor()
        s_into, s_values = self.templateToIntoClause(r)
        cursor.execute("SET SQL_MODE = ''; ")
        cursor.execute("INSERT INTO `" + self.name + "` " + s_into + " VALUES " + s_values + ";")
        self.cnx.commit()

    # t: A template.
    # Deletes all rows matching the template.
    def delete(self, t):
        self.check()
        self.check(template=t)
        dt = self.find_by_template(t).rows
        if len(dt) == 1:
            if list(dt[0].values()) == ['' for _ in range(len(list(dt[0].values())))]:
                raise NameError('No row matches the deleting template!')
        cursor = self.cnx.cursor()
        cursor.execute("DELETE FROM " + self.name + " " + self.templateToWhereClause(t))
        self.cnx.commit()



if __name__ == "__main__":
    try:
        cxnx = pymysql.connect(host='localhost',
                              port=3306,
                              user='root',
                              password='database',
                              db='Lahman2017',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        people_rdbt = RDBDataTable("People", "", ["playerID"], cxnx)
        people_rdbt.load()
        print(people_rdbt)


        # t1 = {"playerID": "sullite01"}
        # print("Testing template ", t1, " on table", "People")

        # result = people_rdbt.find_by_template(t1)
        # print("Query result is ")
        # people_rdbt.__str__(result)

        # result2 = people_rdbt.find_by_primary_key(['willi2te01'])
        # print("Query result is ")
        # print(json.dumps(result2, indent=2))

        # print("select " + "*" + " from " + people_rdbt.name + " " + people_rdbt.templateToWhereClause({"playerID": "willite01"}) + ";")
        # result3 = people_rdbt.delete({"nameFirst": "add", "playerID": "willite021"})
        # t1 = {"nameFirst": "add"}
        # result = people_rdbt.find_by_template(t1)
        # result3 = people_rdbt.find_by_template({"nameFirst": "Ted", "nameLast": "Williams2"})
        # print("Query result is ")
    except Exception as e:
        print("Got exception = ", str(e))

