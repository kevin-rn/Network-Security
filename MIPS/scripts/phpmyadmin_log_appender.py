import datetime
from scapy.all import *
from time import sleep

# Mar 31 16:16:38 nsproject sshd[9297]: Failed password for user from 192.168.0.106 port 57766 ssh2

MAX_TRY = int(sys.argv[1])
NR_IPS_TOBAN = int(sys.argv[2])



LOG = "/var/log/auth.log"

print("start phpmyadmin", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])
with open(LOG, 'a') as f:
    for i in range(NR_IPS_TOBAN):
        ip = RandIP()._fix()
        for i in range(MAX_TRY):
            d = datetime.now()
            timestamp = d.strftime("%b %d %H:%M:%S")
            tmp = "\n{} nsproject phpMyAdmin[2826]: user denied: root (mysql-denied) from {}".format(timestamp, ip)
            f.write(tmp)
            sleep(0.01)

print("end phpmyadmin", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])
