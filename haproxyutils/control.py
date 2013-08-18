import socket
import select
import sys
import string

from settings import DEFAULT_SOCKET_LOCATION
from traceback import format_exc

class HAProxyStatsConnection():

    def __init__(self, socket_name=DEFAULT_SOCKET_LOCATION):
        self.socket_name = socket_name

    def execute(self, command):
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(self.socket_name)
        client.send(command + "\n")

        lines = ''
        buffer = client.recv(4096)
        while buffer:
            lines += buffer
            buffer = client.recv(4096)
        running = False
        client.close()
        return lines

    def run(fn):
        def _fn(self, *args, **kwargs):
            return self.execute(fn(self, *args, **kwargs))
        return _fn

    def get_weight(self, backend, server):
        return map(int, self.execute('get weight {0}/{1}'.format(backend, server)).replace(')','').split('(initial'))

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

    @run
    def help(self):
        return 'help'

    @run
    def set_timeout_cli(self, delay):
        return 'set timeout cli {0}'.format(delay)

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
