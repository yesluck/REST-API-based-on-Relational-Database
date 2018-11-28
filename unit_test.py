import json
import SimpleBO

def test1():
    t = {"nameLast": ["Williams"], "nameFirst": ["Ted"]}
    #print("WC = ", SimpleBO.template_to_where_clause(t))
    result = SimpleBO.find_by_template("people", t, fields=None)
    print("Result = ", json.dumps(result, indent=2))


test1()