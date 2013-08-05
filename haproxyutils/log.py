import os
import fileinput
import traceback
import time
import subprocess
import select
import operator
from math import sqrt
from urlparse import urlparse
from collections import defaultdict
from datetime import datetime


DEFAULT_LOG_FILE = '/var/log/haproxy_1.log'

class HAProxyLog:
    def __init__(self, log_str, offset=0):
        split_line = log_str.split()
        self.pid = int(split_line[offset + 4].replace('haproxy[', '').replace(']:', ''))
        split_ip_port = split_line[offset + 5].split(':')
        self.client_ip = split_ip_port[0]
        self.client_port = int(split_ip_port[1])
        self.accept_date = datetime.strptime(split_line[offset + 6].replace('[', '').replace(']', ''), '%d/%b/%Y:%H:%M:%S.%f')
        self.frontend_name = split_line[offset + 7]
        split_backend_server = split_line[offset + 8].split('/')
        self.backend_name = split_backend_server[0]
        self.server_name = split_backend_server[1]
        self.timings = split_line[offset + 9]
        split_timings = self.timings.split('/')
        self.tq = int(split_timings[0])
        self.tw = int(split_timings[1])
        self.tc = int(split_timings[2])
        self.tr = int(split_timings[3])
        self.tt = int(split_timings[4])
        self.status_code = split_line[offset + 10]
        self.num_bytes = split_line[offset + 11]
        self.captured_request_cookie = split_line[offset + 12]
        self.captured_response_cookie = split_line[offset + 13]
        self.termination_state = split_line[offset + 14]
        self.connections = split_line[offset + 15]
        split_connections = self.connections.split('/')
        self.actconn = split_connections[0]
        self.feconn = split_connections[1]
        self.beconn = split_connections[2]
        self.srv_conn = split_connections[3]
        self.retries = split_connections[4]
        self.queues = split_line[offset + 16]
        split_queues = self.queues.split('/')
        self.srv_queue = split_queues[0]
        self.backend_queue = split_queues[1]
        self.request_type = split_line[offset + 17].replace('"', '')
        self.url = split_line[offset + 18]
        if 'http' in self.url:
            self.domain = urlparse(self.url).hostname
        else:
            self.domain = self.url
        self.http_version = split_line[offset + 19].split('/')[1].replace('"', '')


def get_logs(log_file=DEFAULT_LOG_FILE, num_lines=10000):
    logs = []
    for line in _tail(log_file, num_lines, blocking=True):
        try:
            if not 'UP' in line and \
               not 'DOWN' in line and \
               not ' stopped ' in line and \
               not '<BADREQ>' in line and \
               not ' Pausing ' in line and \
               not ' started.' in line and \
               not ' Stopping ' in line:
                 logs.append(HAProxyLog(line))
        except Exception, e:
            print line.strip() + " excluded from analysis"
            print len(logs)
            print e
            traceback.print_exc()
    return logs

def getAverageResponseTime(logs, aggregate_by='server_name', sort_by='tr', sort_order='ascending'):
    averages = {}
    for log in logs:
        if getattr(log, aggregate_by) in averages:
            averages[getattr(log, aggregate_by)]['tr'].append(log.tr)
            averages[getattr(log, aggregate_by)]['tt'].append(log.tt)
        else:
            averages[getattr(log, aggregate_by)] = {'tr': [log.tr], 'tt': [log.tt]}

    for item in averages:
        length = len(averages[item]['tr'])
        averages[item]['tr_count'] = length
        averages[item]['tr_average'] = sum(averages[item]['tr']) / float(length)
        averages[item]['tr_std'] = sqrt(sum((x - averages[item]['tr_average'])**2 for x in averages[item]['tr']) / float(length))
        averages[item]['tt_count'] = length
        averages[item]['tt_average'] = sum(averages[item]['tt']) / float(length)
        averages[item]['tt_std'] = sqrt(sum((x - averages[item]['tt_average'])**2 for x in averages[item]['tt']) / float(length))
        del averages[item]['tr']
        del averages[item]['tt']

    if 'ascending' in sort_order:
        return sorted(averages.iteritems(), key=lambda x: x[1][sort_by + '_average'])
    elif 'descending' in sort_order:
        return sorted(averages.iteritems(), key=lambda x: x[1][sort_by + '_average'], reverse=True)

def _tail(filename, num_lines, blocking=False):
    log_lines = []
    tail_command = ['tail', '-n', str(num_lines), filename]
    if blocking:
        f = subprocess.Popen(tail_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            line = f.stdout.readline()
            if not line:
                break
            log_lines.append(line)
    else:
        # Doesnt work yet...
        f = subprocess.Popen(tail_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p = select.poll()
        p.register(f.stdout)
        while True:
            if p.poll(1):
                line = f.stdout.readline()
                if not line:
                    break
                log_lines.append(line)
            time.sleep(1)
    return log_lines
