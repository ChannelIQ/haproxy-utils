from flask import request, Flask, Response, jsonify
from haproxyutils import admin

import json

app = Flask(__name__)

@app.route('/backend/<backend>/')
def backend(backend):
    """List all servers within a given backend"""
    return _responsify(admin.get_backend(backend))

@app.route('/backends/')
def backends():
    """ List all backends as well as its servers"""
    return _responsify(admin.get_backends())

@app.route('/frontends/')
def frontends():
    """Lists all frontends."""
    return _responsify(admin.get_frontends())

@app.route('/servers/')
def servers():
    """Lists all servers"""
    return _responsify(admin.get_servers())

@app.route('/enable_server/<backend>/<server>/')
def enable_server(backend, server):
    """Enable a server on a backend"""
    return _responsify(admin.enable_server(backend, server))

@app.route('/disable_server/<backend>/<server>/')
def disable_server(backend, server):
    """Disable a server on a backend"""
    return _responsify(admin.disable_server(backend, server))

@app.route('/set_weight/<backend>/<server>/<weight>/')
def set_weight(backend, server, weight):
    """Set the weight on a server in a backend"""
    return _responsify(admin.set_weight(backend, server, weight))

@app.route('/get_weight/<backend>/<server>/')
def get_weight(backend, server):
    """Get the weight on a server in a backend"""
    return _responsify(admin.get_weight(backend, server))

@app.route('/')
def api():
    """Print API"""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(func_list)


def _responsify(obj):
    return Response(json.dumps(obj, default=lambda o: o.__dict__, indent=2), mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
