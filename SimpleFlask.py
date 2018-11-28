# Lahman.py

# Convert to/from web native JSON and Python/RDB types.
import json

# Include Flask packages
from flask import Flask
from flask import request
import copy

import SimpleBO
import Query

# The main program that executes. This call creates an instance of a
# class and the constructor starts the runtime.
app = Flask(__name__)

def parse_and_print_args():

    fields = None
    offset = None
    limit = None
    in_args = None
    if request.args is not None:
        in_args = dict(copy.copy(request.args))
        fields = copy.copy(in_args.get('fields', None))
        offset = copy.copy(in_args.get('offset', None))
        limit = copy.copy(in_args.get('limit', None))
        if fields:
            del(in_args['fields'])
        if offset:
            del(in_args['offset'])
        if limit:
            del(in_args['limit'])

    try:
        if request.data:
            body = json.loads(request.data)
        else:
            body = None
    except Exception as e:
        print("Got exception = ", e)
        body = None

    print("Request.args : ", json.dumps(in_args))
    return in_args, fields, body, offset, limit


@app.route('/api/<resource>', methods=['GET', 'POST'])
def get_resource(resource):

    in_args, fields, body, offset, limit = parse_and_print_args()
    if request.method == 'GET':
        if resource == "roster":
            result = Query.roster(in_args, offset, limit)
        else:
            result = SimpleBO.find_by_template(resource, in_args, fields, offset, limit)
        return json.dumps(result), 200, {"content-type": "application/json; charset: utf-8"}
    elif request.method == 'POST':
        SimpleBO.insert(resource, body[0] if isinstance(body, list) else body)
        return "Insert successfully!"
    else:
        return "Method " + request.method + " on resource " + resource + " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}

@app.route('/api/<resource>/<primary_key>', methods=['GET', 'PUT', 'DELETE'])
def get_specific_resource(resource, primary_key):

    in_args, fields, body, offset, limit = parse_and_print_args()
    pk = primary_key.split('_')
    if request.method == 'GET':
        if resource == "teammates":
            result = Query.teammates(pk, offset, limit)
        else:
            result = SimpleBO.find_by_primary_key(resource, pk, fields, offset, limit)
        return json.dumps(result), 200, {"content-type": "application/json; charset: utf-8"}
    elif request.method == 'PUT':
        SimpleBO.update(resource, pk, body[0] if isinstance(body, list) else body)
        return "Update successfully!"
    elif request.method == 'DELETE':
        SimpleBO.delete(resource, pk)
        return "Delete successfully!"
    else:
        return "Method " + request.method + " on resource " + resource + \
               " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}

@app.route('/api/<resource>/<primary_key>/<related_source>', methods=['GET', 'POST', 'DELETE'])
def get_dependent_resource(resource, primary_key, related_source):
    in_args, fields, body, offset, limit = parse_and_print_args()
    pk = primary_key.split('_')
    if request.method == 'GET':
        if related_source == "career_stats":
            result = Query.career_stats(pk, offset, limit)
        else:
            result = SimpleBO.related_get(resource, pk, related_source, in_args, fields, offset, limit)
        return json.dumps(result), 200, {"content-type": "application/json; charset: utf-8"}
    elif request.method == 'POST':
        SimpleBO.related_post(resource, pk, related_source, body[0] if isinstance(body, list) else body)
        return "Insert successfully!"
    else:
        return "Method " + request.method + " on resource " + resource + \
               " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}


if __name__ == '__main__':
    app.run()

