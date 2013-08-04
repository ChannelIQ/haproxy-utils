import os
import fileinput
import traceback
from urlparse import urlparse
from collections import defaultdict
from datetime import datetime


DEFAULT_LOG_FILE = '/var/log/haproxy_1.log'

class HAProxyLog:
    def __init__(self, log_str):
        split_line = log_str.split()
        self.pid = int(split_line[4].replace('haproxy[', '').replace(']:', ''))
        split_ip_port = split_line[5].split(':')
        self.client_ip = split_ip_port[0]
        self.client_port = int(split_ip_port[1])
        self.accept_date = datetime.strptime(split_line[6].replace('[', '').replace(']', ''), '%d/%b/%Y:%H:%M:%S.%f')
        self.frontend_name = split_line[7]
        split_backend_server = split_line[8].split('/')
        self.backend_name = split_backend_server[0]
        self.server_name = split_backend_server[1]
        self.timings = split_line[9]
        split_timings = self.timings.split('/')
        self.tq = int(split_timings[0])
        self.tw = int(split_timings[1])
        self.tc = int(split_timings[2])
        self.tr = int(split_timings[3])
        self.tt = int(split_timings[4])
        self.status_code = split_line[10]
        self.num_bytes = split_line[11]
        self.captured_request_cookie = split_line[12]
        self.captured_response_cookie = split_line[13]
        self.termination_state = split_line[14]
        self.connections = split_line[15]
        split_connections = self.connections.split('/')
        self.actconn = split_connections[0]
        self.feconn = split_connections[1]
        self.beconn = split_connections[2]
        self.srv_conn = split_connections[3]
        self.retries = split_connections[4]
        self.queues = split_line[16]
        split_queues = self.queues.split('/')
        self.srv_queue = split_queues[0]
        self.backend_queue = split_queues[1]
        self.request_type = split_line[17].replace('"', '')
        self.url = split_line[18]
        if 'http' in self.url:
            self.domain = urlparse(self.url).hostname
        else:
            self.domain = self.url
        self.http_version = split_line[19].split('/')[1].replace('"', '')


def get_logs(num_logs=10000, log_file=DEFAULT_LOG_FILE):
    logs = []
    for line in fileinput.input():
#    print os.popen('tail -n {num_logs} {log_file}'.format(**locals())).read()[0]
    #print _tail(file(log_file), num_logs)
    #exit()
#    for line in _tail(file(log_file), num_logs).split('\n'):
        try:
#            if 'server' in line:
            logs.append(HAProxyLog(line))
        except Exception, e:
            print line.strip() + "excluded from analysis"
            print len(logs)
            print e
            traceback.print_exc()
        #    exit()
    print logs[0]
    return logs

def getAverageResponseTime(logs, aggregate_by=''):
    averages = {}
    for log in logs:
        if getattr(log, aggregate_by) in averages:
            averages[getattr(log, aggregate_by)]['tr'].append(log.tr)
            averages[getattr(log, aggregate_by)]['tt'].append(log.tt)
        else:
            averages[getattr(log, aggregate_by)] = {'tr': [log.tr], 'tt': [log.tt]}

    for item in averages:
        length = float(len(averages[item]['tr']))
        averages[item]['tr_average'] = sum(averages[item]['tr']) / length
        averages[item]['tt_average'] = sum(averages[item]['tt']) / length
        print item, averages[item]['tr_average'], averages[item]['tt_average'], length

# http://stackoverflow.com/questions/136168/get-last-n-lines-of-a-file-with-python-similar-to-tail
def _tail(f, window=20):
    BUFSIZ = 1024
    f.seek(0, 2)
    bytes = f.tell()
    size = window
    block = -1
    data = []
    while size > 0 and bytes > 0:
        if (bytes - BUFSIZ > 0):
            # Seek back one whole BUFSIZ
            f.seek(block*BUFSIZ, 2)
            # read BUFFER
            data.append(f.read(BUFSIZ))
        else:
            # file too small, start from begining
            f.seek(0,0)
            # only read what was not read
            data.append(f.read(bytes))
        linesFound = data[-1].count('\n')
        size -= linesFound
        bytes -= BUFSIZ
        block -= 1
    return '\n'.join(''.join(data).splitlines()[-window:])

logs = get_logs()
getAverageResponseTime(logs, aggregate_by='server_name')

