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
            self.execute(fn(self, *args, **kwargs))
        return _fn

    def get_weight(self, backend, server):
        return map(int, self.execute('get weight {0}/{1}'.format(backend, server))[0].replace(')','').split('(initial'))

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
        return 'clear counters all'

    def help(self):
        return ''.join(self.execute('help'))

    @run
    def set_timeout_cli(self, delay):
        return 'set timeout cli {0}'.format(delay)

    # will test and update once my haproxy actually has errors, lolz
    def show_errors(self, iid=''):
        return ''.join(self.execute('show errors {0}'.format(iid)))

    # need to update this and parse out/cast appropriately
    def show_info(self):
        return ''.join(self.execute('show info'))

    def show_sess(self, id=''):
        return ''.join(self.execute('show sess {0}'.format(id))).split()

    @run
    def show_stat(self, iid='', type='', sid=''):
        return 'show stat {0} {1} {2}'.format(iid, type, sid)
