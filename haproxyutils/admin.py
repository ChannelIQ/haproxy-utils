from haproxyutils import control
from settings import DEFAULT_SOCKET_LOCATION

class HAProxy():
    def __init__(self):
        self.frontends, self.backends = _parse_stats()

class Stat():
    def __init__(self, stat_str):
        split_stat = stat_str.split(',')
        self.pxname = split_stat[0]
        self.svname = split_stat[1]
        self.qcur = split_stat[2]
        self.qmax = split_stat[3]
        self.scur = split_stat[4]
        self.smax = split_stat[5]
        self.slim = split_stat[6]
        self.stot = split_stat[7]
        self.bin = split_stat[8]
        self.bout = split_stat[9]
        self.dreq = split_stat[10]
        self.dresp = split_stat[11]
        self.ereq = split_stat[12]
        self.econ = split_stat[13]
        self.eresp = split_stat[14]
        self.wretr = split_stat[15]
        self.wredis = split_stat[16]
        self.status = split_stat[17]
        self.weight = split_stat[18]
        self.act = split_stat[19]
        self.bck = split_stat[20]
        self.chkfail = split_stat[21]
        self.chkdown = split_stat[22]
        self.lastchg = split_stat[23]
        self.downtime = split_stat[24]
        self.qlimit = split_stat[25]
        self.pid = split_stat[26]
        self.iid = split_stat[27]
        self.sid = split_stat[28]
        self.throttle = split_stat[29]
        self.lbtot = split_stat[30]
        self.tracked = split_stat[31]
        self.type = split_stat[32]
        self.rate = split_stat[33]
        self.rate_lim = split_stat[34]
        self.rate_max = split_stat[35]

def disable_server(backend, server):
    try:
        conn = control.HAProxyStatsConnection()
        conn.disable_server(backend, server)
    except Exception, e:
        return False
    return True

def enable_server(backend, server):
    try:
        conn = control.HAProxyStatsConnection()
        conn.enable_server(backend, server)
    except Exception, e:
        return False
    return True

def set_weight(backend, server, weight):
    conn = control.HAProxyStatsConnection()
    return conn.set_weight(backend, server, weight)

def get_weight(backend, server):
    conn = control.HAProxyStatsConnection()
    return conn.get_weight(backend, server)

def get_backends():
    return HAProxy().backends

def get_backend(backend):
    return HAProxy().backends[backend]

def get_frontends():
    return HAProxy().frontends

def get_servers():
    servers = {}
    backends = HAProxy().backends
    for backend in backends:
        for stat in backends[backend]:
            if stat.svname in servers:
                servers[stat.svname].append(backend)
            else:
                servers[stat.svname] = [backend]
    return servers

def reset_weights(backend=None):
    """ Takes the name of a backend and resets weights on it.
        Without a name, every backend will have its weights reset"""
    set_weights(1, backend=backend)

def set_weights(weight=1, backend=None):
    hap = HAProxy()
    conn = control.HAProxyStatsConnection()
    if backend is None:
        for backend in hap.backends:
            for stat in hap.backends[backend]:
                conn.set_weight(backend, stat.svname, weight)
    else:
        for stat in hap.backends[backend]:
            conn.set_weight(backend, stat.svname, weight)

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
                if stat.pxname in backends:
                    backends[stat.pxname].append(stat)
                else:
                    backends[stat.pxname] = [stat]
        except:
            print line
    return frontends, backends
