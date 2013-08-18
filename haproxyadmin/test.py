import json
import inspect
from flask import request, Flask, Response, jsonify

from haproxyutils import admin

def _get_function_names():
    functions = []
    for function in dir(admin):
        if not '__' in function[0:2] and \
           not '__' in function[-2:]:
            functions.append(function)
    return functions

def _generate_url_pattern(function_name):
    method = getattr(admin, function)
    pattern = '/' + function_name +'/'
    for arg in inspect.getargspec(method)[0]:
        pattern += '<' + arg + '>/'
    return pattern

def _generate_view_function(function_name):
    return _responsify(getattr(admin, function_name), function_name)

def _responsify(obj, function_name):
    response = Response(json.dumps(obj, default=lambda o: o.__dict__, indent=2), mimetype='application/json')
    response.__name__ = function_name
    return response

app = Flask(__name__)

for function in _get_function_names():
    try:
        app.add_url_rule(_generate_url_pattern(function), view_func=_generate_view_function(function))
#        app.add_url_rule(_generate_url_pattern(function), view_func=_generate_view_function(function))
#        app.add_url_rule(_generate_url_pattern(function), view_func=_generate_view_function(function).as_view(function))
    except Exception as e:
        print function, e

#@app.route("/site-map")
#def site_map():
#    rules = []
#    for rule in app.url_map.iter_rules():
#        # Filter out rules we can't navigate to in a browser
#        # and rules that require parameters
##        if "GET" in rule.methods and len(rule.defaults) >= len(rule.arguments):
##        url = url_for(rule.endpoint)
##        links.append((url, rule.endpoint))
#        rules.append(rule)
#    return _responsify(rules)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


