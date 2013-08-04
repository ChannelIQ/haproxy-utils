from haproxyutils import control, log

conn = control.HAProxyStatsConnection()

print conn.get_weight('all-proxies-non-sticky', 'ninjaproxy_106')

print conn.set_weight('all-proxies-non-sticky', 'ninjaproxy_106', 200)

print conn.get_weight('all-proxies-non-sticky', 'ninjaproxy_106')

print conn.clear_counters()

print conn.clear_counters_all()

print conn.disable_server('all-proxies-non-sticky', 'ninjaproxy_106')

print conn.enable_server('all-proxies-non-sticky', 'ninjaproxy_106')

print conn.help()

print conn.show_errors()

print conn.show_info()

print conn.show_sess()

print conn.show_stat()

print len(log.get_logs())
