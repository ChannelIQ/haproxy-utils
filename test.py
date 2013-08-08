from haproxyutils import control
from haproxyutils import log
from haproxyutils import admin

conn = control.HAProxyStatsConnection()

#conn.set_weight('all-proxies-non-sticky', 'ninjaproxy_106', 200)

#print conn.get_weight('all-proxies-non-sticky', 'ninjaproxy_106')

#conn.clear_counters()

#conn.clear_counters_all()

#conn.disable_server('all-proxies-non-sticky', 'ninjaproxy_106')

#conn.enable_server('all-proxies-non-sticky', 'ninjaproxy_106')

#print conn.help()

#conn.set_timeout_cli(10)

#print conn.show_errors()

#print conn.show_info()

#print conn.show_sess()

#print conn.show_stat()

#logs = log.get_logs()
#for average in log.getAverageResponseTime(logs, aggregate_by='backend_server_combo', sort_by='tt', sort_order='descending'):
#    print average

#print len(logs)

#backends = admin.get_backends()
#for backend in backends:
#    print backend, len(backends[backend])
#    for stat in backends[backend]:
#        print stat.backend, stat.server_name

#print admin.get_frontends()

admin.reset_weights()

#admin.set_weights(2, backend='all-proxies-non-sticky')
