import sys
import ipaddress
import random
from datetime import datetime

MAX_IPV4 = ipaddress.IPv4Address._ALL_ONES  # 2 ** 32 - 1
MAX_IPV6 = ipaddress.IPv6Address._ALL_ONES  # 2 ** 128 - 1

PATH_TO_LOG = "/var/log/apache2/access.log"


def random_ipv4() -> str:
    return ipaddress.IPv4Address._string_from_ip_int(random.randint(0, MAX_IPV4))


def random_ipv6() -> str:
    return ipaddress.IPv6Address._string_from_ip_int(random.randint(0, MAX_IPV6))


def generate_log_line(rand_ip: str) -> str:
    curr_date = datetime.now().isoformat()
    prior = "INFO"
    category = "joomlafailure"
    msg = "Username and password do not match or you do not have an account yet."
    return f"{curr_date}    {prior} {rand_ip}    {category}  {msg}\n"


def get_rand_int(_from, _to):
    return random.randint(_from, _to)


def append_to_joomla_log(log_str: str):
    global PATH_TO_LOG
    with open(PATH_TO_LOG, "a") as f:
        f.write(log_str)


if __name__ == "__main__":
    request_threshold_per_ip = int(sys.argv[1])
    amount_to_append_per_ip = int(sys.argv[2])

    for _ in range(amount_to_append_per_ip):
        ip = random_ipv4() if get_rand_int(0, 2) <= 1 else random_ipv6()
        diff_ips = True if get_rand_int(0, 2) <= 1 else False
        if diff_ips:
            for _ in range(request_threshold_per_ip):
                append_to_joomla_log(generate_log_line(ip))
                ip = random_ipv4() if get_rand_int(0, 2) <= 1 else random_ipv6()
        else:
            for _ in range(request_threshold_per_ip):
                append_to_joomla_log(generate_log_line(ip))
