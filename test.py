from haproxyutils import control
from haproxyutils import log

conn = control.HAProxyStatsConnection()

print conn.set_weight('all-proxies-non-sticky', 'ninjaproxy_106', 200)

print conn.get_weight('all-proxies-non-sticky', 'ninjaproxy_106')

print conn.clear_counters()

print conn.clear_counters_all()

print conn.disable_server('all-proxies-non-sticky', 'ninjaproxy_106')

print conn.enable_server('all-proxies-non-sticky', 'ninjaproxy_106')

print conn.help()

print conn.set_timeout_cli(10)

print conn.show_errors()

print conn.show_info()

print conn.show_sess()

print conn.show_stat()

logs = log.get_logs()
for average in log.getAverageResponseTime(logs, aggregate_by='backend_server_combo', sort_by='tt', sort_order='descending'):
    print average

print len(logs)
