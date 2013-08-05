#Credits
*   socket interfacing code https://github.com/nl5887/python-haproxy

#Goals
*  provide simple python bindings for issuing commands to the haproxy stats socket
*  supplement statistics available through the stats socket with statistics from log files

#Limitations/Requirements
*  log parsing is not very robust at the moment thus the log format requirements are pretty rigid
*  for example:
```Aug  3 20:41:28 localhost haproxy[7466]: 10.80.111.24:65168 [03/Aug/2013:20:41:28.190] non-sticky all-proxies-non-sticky/ninjaproxy_106 0/0/68/195/349 200 6040 - - ---- 0/0/0/0/0 0/0 "GET http://ipogre.com/ HTTP/1.1"```

#Installation
*  With git
```bash
git clone https://github.com/ChannelIQ/haproxy-utils.git
cd haproxy-utils
sudo python setup.py install
```

*  Without git
```bash
cd /tmp
wget https://github.com/ChannelIQ/haproxy-utils/archive/master.zip -O haproxy-utils.zip
unzip haproxy-utils.zip
cd haproxy-utils-master
sudo python setup.py install
```

*  Automagically
```bash
bash <(curl -s https://raw.github.com/ChannelIQ/haproxy-utils/master/install)
```

#Examples
```python
from haproxyutils import control
from haproxyutils import log

conn = control.HAProxyStatsConnection()
conn.set_weight('all-proxies-non-sticky', 'ninjaproxy_106', 200)
```

#Todo
* rewrite log parsing class for robustness and conveinence
* Fix bugs in control.py (known incorrect commands)
* write a flask based api to expose the functions in the control file
* profit
