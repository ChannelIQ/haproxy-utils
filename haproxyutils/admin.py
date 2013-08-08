from haproxyutils import control

DEFAULT_SOCKET_LOCATION = '/tmp/haproxy_socket'

class HAProxy():
    def __init__(self):
        self.frontends, self.backends = _parse_stats()

class Stat():
    def __init__(self, stat_str):
        split_stat = stat_str.split(',')
        self.backend = split_stat[0]
        self.server_name = split_stat[1]
        # more to come later...
        self.weight = split_stat[18]

def get_backends():
    return HAProxy().backends

def get_backend(backend):
    return HAProxy().backends[backend]

def get_frontends():
    return HAProxy().frontends

def reset_weights(backend=None):
    """ Takes the name of a backend and resets weights on it.
        Without a name, every backend will have its weights reset"""
    set_weights(1, backend=backend)

def set_weights(weight, backend=None):
    hap = HAProxy()
    conn = control.HAProxyStatsConnection()
    if backend is None:
        for backend in hap.backends:
            for stat in hap.backends[backend]:
                conn.set_weight(backend, stat.server_name, weight)
    else:
        for stat in hap.backends[backend]:
            conn.set_weight(backend, stat.server_name, weight)

def _parse_stats():
    conn = control.HAProxyStatsConnection()
    frontends = []
    backends = {}
    for line in ''.join(conn.show_stat()).split('\n')[1:-1]:
        try:
            if 'BACKEND' in line:
                pass
            elif 'FRONTEND' in line:
                frontends.append(line.split(',')[0])
            else:
                stat = Stat(line)
                if stat.backend in backends:
                    backends[stat.backend].append(stat)
                else:
                    backends[stat.backend] = [stat]
        except:
            print line
    return frontends, backends
