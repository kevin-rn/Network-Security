import datetime
from scapy.all import *
from time import sleep


# Mar 31 16:16:38 nsproject sshd[9297]: Failed password for user from 192.168.0.106 port 57766 ssh2

MAX_TRY = int(sys.argv[1])
NR_IPS_TOBAN = int(sys.argv[2])



LOG = "/var/log/auth.log"

print("start ssh", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])
with open(LOG, 'a') as f:
    for i in range(NR_IPS_TOBAN):
        ip = RandIP()._fix()
        for i in range(MAX_TRY):
            d = datetime.now()
            timestamp = d.strftime("%b %d %H:%M:%S")
            tmp = "\n{} nsproject sshd[9297]: Failed password for user from {} port 57766 ssh2".format(timestamp, ip)
            f.write(tmp)
            sleep(0.01)

print("end ssh", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])




# import sys
# import ipaddress
# import random
# from datetime import datetime, timedelta

# MAX_IPV4 = ipaddress.IPv4Address._ALL_ONES  # 2 ** 32 - 1
# MAX_IPV6 = ipaddress.IPv6Address._ALL_ONES  # 2 ** 128 - 1

# PATH_TO_LOG = "/var/log/auth.log"


# def random_ipv4():
#     return ipaddress.IPv4Address._string_from_ip_int(random.randint(0, MAX_IPV4))


# def random_ipv6():
#     return ipaddress.IPv6Address._string_from_ip_int(random.randint(0, MAX_IPV6))


# def generate_log_line(rand_ip: str, date: datetime) -> str:
#         timestamp = date.strftime("%b %d %H:%M:%S")
#         return "{} nsproject sshd[9297]: Failed password for user from {} port 57766 ssh2\n".format(timestamp, rand_ip)


# def get_rand_int(_from, _to):
#     return random.randint(_from, _to)


# def append_to_joomla_log(log_str: str):
#     global PATH_TO_LOG
#     with open(PATH_TO_LOG, "a") as f:
#         f.write(log_str)


# if __name__ == "__main__":
#     request_threshold_per_ip = int(sys.argv[1])
#     amount_to_append_per_ip = int(sys.argv[2])
#     date_now = datetime.now()

#     for _ in range(amount_to_append_per_ip):
#         ip = random_ipv4() if get_rand_int(0, 2) <= 1 else random_ipv6()
#         diff_ips = True if get_rand_int(0, 2) <= 1 else False
#         if diff_ips:
#             for _ in range(request_threshold_per_ip):
#                 append_to_joomla_log(generate_log_line(ip, date_now))
#                 date_now = date_now + timedelta(seconds=1)
#                 ip = random_ipv4() if get_rand_int(0, 2) <= 1 else random_ipv6()
#         else:
#             for _ in range(request_threshold_per_ip):
#                 append_to_joomla_log(generate_log_line(ip, date_now))
#                 date_now = date_now + timedelta(seconds=1)
