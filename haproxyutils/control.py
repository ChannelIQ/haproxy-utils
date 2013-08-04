#from haproxy import haproxy
import logging
import socket
import select
import sys
import string

from time import time
from traceback import format_exc

DEFAULT_SOCKET_LOCATION = '/tmp/haproxy_socket'

#logger = logging.getLogger(__name__)

class TimeoutException(Exception):
    pass

class HAProxyStatsConnection():

    def __init__(self, socket_name=DEFAULT_SOCKET_LOCATION):
        self.socket_name = socket_name

    def execute(self, command, timeout=200):
        buffer = ""
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(self.socket_name)
        client.send(command + "\n")

        lines = []
        running = True
        while(running):
            r, w, e = select.select([client,],[],[], timeout)
            if not (r or w or e):
                raise TimeoutException()
            for s in r:
                if (s is client):
                    buffer = buffer + client.recv(4096).decode('utf-8')
                    running = (len(buffer)==0)
                    lines.extend(buffer.split('\n'))
                    buffer = lines.pop()
        client.close()
        return lines

    def run(fn):
        def _fn(self, *args, **kwargs):
            return self.execute(fn(self, *args, **kwargs))
        return _fn

    @run
    def get_weight(self, backend, server):
        return 'get weight {0}/{1}'.format(backend, server)

    @run
    def set_weight(self, backend, server, weight):
        return 'set weight {0}/{1} {2}'.format(backend, server, weight)

    @run
    def disable_server(self, backend, server):
        return 'disable server {0}/{1}'.format(backend, server)

    @run
    def enable_server(self, backend, server):
        return 'enable server {0}/{1}'.format(backend, server)

    @run
    def clear_counters(self):
        return 'clear counters'

    @run
    def clear_counters_all(self):
        return 'clear all counters'

    @run
    def help(self):
        return 'help'

    @run
    def show_errors(self, iid=''):
        return 'show errors {0}'.format(iid)

    @run
    def show_info(self):
        return 'show info'

    @run
    def show_sess(self, id=''):
        return 'show sess {0}'.format(id)

    @run
    def show_stat(self, iid='', type='', sid=''):
        return 'show stat {0} {1} {2}'.format(iid, type, sid)
