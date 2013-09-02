from flask import request, Flask, Response, jsonify, render_template
from haproxyutils import admin
from haproxyutils import configparser

import json

app = Flask(__name__)

#######
# API #
#######

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

@app.route('/get_frontend_ports/')
def get_frontend_ports():
    """Get the frontend ports"""
    return _responsify(configparser.get_frontend_ports())

@app.route('/get_frontend_port/<frontend>/')
def get_frontend_port(frontend):
    """Get the port of the supplied frontend"""
    return _responsify(configparser.get_frontend_port(frontend))

@app.route('/get_listen_ports/')
def get_listen_ports():
    """Get the ports that listen sections are listening on"""
    return _responsify(configparser.get_listen_ports())

@app.route('/get_backend_server_addresses/<backend>/')
def get_backend_server_addresses(backend):
    """Get a list of addresses for the given backend"""
    return _responsify(configparser.get_backend_server_addresses(backend))

@app.route('/get_server_addresses/<server_name>/')
def get_server_addresses(server_name):
    """Get any and all addresses of the server_name provided"""
    return _responsify(configparser.get_server_addresses(server_name))

@app.route('/get_all_listening_ports/')
def get_all_listening_ports():
    """Get all of listening ports, this includes backend and listen sections"""
    return _responsify(configparser.get_all_listening_ports())

@app.route('/')
def api():
    """Print API"""
    return jsonify(_get_api())

############
# Webadmin #
############

@app.route('/ui/')
def index():
    """Webui homepage"""
    return render_template('index.html')

@app.route('/api_ui/')
def api_ui():
    """Display API in html"""
    return render_template('api.html', api=_get_api())

@app.route('/frontends_ui/')
def frontends_ui():
    """List frontends in html"""
    return render_template('frontends.html', frontends=admin.get_frontends())

@app.route('/backends_ui/')
def backends_ui():
    """List backends in html"""
    return render_template('backends.html', backends=admin.get_backends())

@app.route('/backend_ui/<backend>/')
def backend_ui(backend):
    """Show details about a specific backend in html"""
    servers = admin.get_backend(backend)
#    headers = _get_attribute_names(servers[0])
    headers = ['Server', 'Status']
    return render_template('backend.html', backend_name=backend, servers=servers, headers=headers)

@app.route('/servers_ui/')
def servers_ui():
    """List all servers in html"""
    return render_template('servers.html')

####################
# Helper functions #
####################

def _responsify(obj):
    return Response(json.dumps(obj, default=lambda o: o.__dict__, indent=2), mimetype='application/json')

def _get_api():
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return func_list

def _get_attribute_names(obj):
    attributes = []
    for k in dir(obj):
        if not '__' in k[0:2] and \
           not '__' in k[-3:]:
            attributes.append(k)
    return attributes

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
