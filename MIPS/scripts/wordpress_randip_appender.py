import sys
import ipaddress
import random
from datetime import datetime, timedelta

MAX_IPV4 = ipaddress.IPv4Address._ALL_ONES  # 2 ** 32 - 1
MAX_IPV6 = ipaddress.IPv6Address._ALL_ONES  # 2 ** 128 - 1

PATH_TO_LOG = "/var/log/apache2/access.log"


def random_ipv4():
    return ipaddress.IPv4Address._string_from_ip_int(random.randint(0, MAX_IPV4))


def random_ipv6():
    return ipaddress.IPv6Address._string_from_ip_int(random.randint(0, MAX_IPV6))


def generate_log_line(rand_ip: str, date: datetime) -> str:
    curr_date = date.strftime("%d/%b/%Y:%H:%M:%S")
    return f'{rand_ip} - - [{curr_date} +0200] "GET /phpmyadmin/phpmyadmin.css.php?nocache=4755212520ltr&server=1 HTTP/1.1" 200 21500 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0"\n'


def get_rand_int(_from, _to):
    return random.randint(_from, _to)


def append_to_joomla_log(log_str: str):
    global PATH_TO_LOG
    with open(PATH_TO_LOG, "a") as f:
        f.write(log_str)


if __name__ == "__main__":
    request_threshold_per_ip = int(sys.argv[1])
    amount_to_append_per_ip = int(sys.argv[2])
    date_now = datetime.now()

    for _ in range(amount_to_append_per_ip):
        ip = random_ipv4() if get_rand_int(0, 2) <= 1 else random_ipv6()
        diff_ips = True if get_rand_int(0, 2) <= 1 else False
        if diff_ips:
            for _ in range(request_threshold_per_ip):
                append_to_joomla_log(generate_log_line(ip, date_now))
                date_now = date_now + timedelta(seconds=1)
                ip = random_ipv4() if get_rand_int(0, 2) <= 1 else random_ipv6()
        else:
            for _ in range(request_threshold_per_ip):
                append_to_joomla_log(generate_log_line(ip, date_now))
                date_now = date_now + timedelta(seconds=1)
