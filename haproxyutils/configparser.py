from settings import DEFAULT_CONFIG_LOCATION


def get_frontend_ports(config=None):
    if config is None:
        config = _parse_config()
    frontends = {}
    if 'frontends' in config:
        for frontend in config['frontends']:
            frontends[frontend] = config['frontends'][frontend]['bind'].split(':')[1]
    return frontends

def get_frontend_port(frontend):
    frontends = get_frontend_ports()
    if frontend in frontends:
        return frontends[frontend]
    return None

def get_listen_ports(config=None):
    if config is None:
        config = _parse_config()
    listeners = {}
    if 'listens' in config:
        for listener in config['listens']:
            listeners[listener] = config['listens'][listener]['bind'].split(':')[1]
    return listeners

def get_backend_server_addresses(backend, config=None):
    if config is None:
        config = _parse_config()
    servers = {}
    if backend in config['backends'] and 'servers' in config['backends'][backend]:
        for server in config['backends'][backend]['servers']:
            servers[server] = config['backends'][backend]['servers'][server]
    return servers

def get_server_addresses(server_name):
    config = _parse_config()
    addresses = {}
    for backend in config['backends']:
        servers = get_backend_server_addresses(backend, config)
        if server_name in servers:
            addresses[backend] = servers[server_name]
    return addresses

def get_server_names(server_address):
    print 'not done'

def get_all_listening_ports():
    config = _parse_config()
    return dict(
            get_frontend_ports(config=config).items() + \
            get_listen_ports(config=config).items()
    )

def get_config():
    return _parse_config()

def _parse_config():
    frontends = {}
    backends = {}
    listens = {}
    current_section_type = ''
    current_section_name = ''
    for line in open(DEFAULT_CONFIG_LOCATION):
        split_line = line.split()

        # If not a comment
        if len(split_line) and not '#' in split_line[0]:

            # Identify which section we are in
            if 'frontend ' in line and 'backend ' in line:
                raise Exception('Unknown section', 'The keywords present made parsing the config too ambiguious')

            elif 'frontend ' in line:
                current_section_type = 'frontend'
                current_section_name = split_line[1]
                frontends[current_section_name] = {}

            elif 'backend ' in line:
                current_section_type = 'backend'
                current_section_name = split_line[1]
                backends[current_section_name] = {}

            elif 'listen ' in line:
                current_section_type = 'listen'
                current_section_name = split_line[1]
                listens[current_section_name] = {}

            elif 'global' in line:
                current_section_type = 'global'
                current_section_name = ''

            elif 'defaults' in line:
                current_section_type = 'defaults'
                current_section_name = ''

            # Fill in the basic details for each section
            elif 'bind' in line and 'frontend' in current_section_type:
                frontends[current_section_name]['bind'] = split_line[1]

            elif 'default_backend' in line and 'frontend' in current_section_type:
                frontends[current_section_name]['default_backend'] = split_line[1]

            elif 'server ' in line and 'backend' in current_section_type:
                if 'servers' not in backends[current_section_name]:
                    backends[current_section_name]['servers'] = {}
                backends[current_section_name]['servers'][split_line[1]] = split_line[2]

            elif 'mode' in line and 'backend' in current_section_type:
                backends[current_section_name]['mode'] = split_line[1]

            elif 'balance' in line and 'backend' in current_section_type:
                backends[current_section_name]['balance'] = split_line[1]

            elif 'bind' in line and 'listen' in current_section_type:
                listens[current_section_name]['bind'] = split_line[1]


    return {'frontends': frontends, 'backends': backends, 'listens': listens}
