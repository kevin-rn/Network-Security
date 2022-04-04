import nftables
import json
from threading import Timer
import datetime
from core.src.db.crud.crud_log_record import delete_log_record_by_colnames

NFT = nftables.Nftables()
NFT.set_json_output(True)
OUTPUT_ON = True

if False:
    print("hello there")

INIT = """{
  "nftables": [
    {
      "add": {
        "table": {
          "family": "inet",
          "name": "succeed2ban",
          "handle": 1
        }
      }
    },
    {
      "add": {
        "set": {
          "family": "inet",
          "name": "blackhole",
          "table": "succeed2ban",
          "type": "ipv4_addr",
          "handle": 1
        }
      }
    },
    {
      "add": {
        "chain": {
          "family": "inet",
          "table": "succeed2ban",
          "name": "s2b",
          "type": "filter",
          "hook": "input",
          "prio": 0,
          "policy": "accept"
        }
      }
    },
    {
      "add": {
        "rule": {
          "family": "inet",
          "table": "succeed2ban",
          "chain": "s2b",
          "expr": [
            {
              "match": {
                "op": "==",
                "left": {
                  "payload": {
                    "protocol": "ip",
                    "field": "saddr"
                  }
                },
                "right": "@blackhole"
              }
            },
            {
              "drop": null
            }
          ]
        }
      }
    }
  ]
}"""

CLEAN = """{
    "nftables": [
        {
            "delete": {
                "chain": {
                    "family": "inet",
                    "table": "succeed2ban",
                    "name": "s2b"
                }
            }
        },
        {
            "delete": {
                "table": {
                    "family": "inet",
                    "name": "succeed2ban"
                }
            }
        }
    ]
}
"""

BAN_IP = """{{
    "nftables": [
        {{
            "add": {{
                "element": {{
                    "family": "inet",
                    "table": "succeed2ban",
                    "name": "blackhole",
                    "elem": [
                        "{ip}"
                    ]
                }}
            }}
        }}
    ]
}}
"""

UNBAN_IP = """{{
    "nftables": [
        {{
            "delete": {{
                "element": {{
                    "family": "inet",
                    "table": "succeed2ban",
                    "name": "blackhole",
                    "elem": [
                        "{ip}"
                    ]
                }}
            }}
        }}
    ]
}}
"""

class BanEntry:
    def __init__(self, ip, service, timestamp, duration):
        self.ip = ip
        self.service = service
        self.timestamp = timestamp
        self.duration = duration


_banned = {}

def _run_cmd(cmd):
    json_cmd = json.loads(cmd)
    status, output, error = NFT.json_cmd(json_cmd)
    if status != 0:
        print(f"NFT error executing \"{cmd}\": {error}")
    if OUTPUT_ON and output:
        print(f"NFT \"{cmd}\": {output}")

def _run_cmd_suppressed(cmd):
    json_cmd = json.loads(cmd)
    NFT.json_cmd(json_cmd)

def init():
    _run_cmd(INIT)

def clean():
    _run_cmd_suppressed(CLEAN)

def ban_ip(ip):
    """ban an ip address

    Args:
        ip: ip address to ban
    """
    _run_cmd(BAN_IP.format(ip=ip))

def unban_ip(ip):
    """unban an ip address

    Args:
        ip: ip address to unban
    """
    delete_log_record_by_colnames(ip=ip)
    if ip in _banned:
        _run_cmd(UNBAN_IP.format(ip=ip))
        del _banned[ip]

def _unban_ip_with_check(ip, timestamp):
    if ip in _banned:
        t2 = _banned[ip].timestamp
        if timestamp == t2:
            delete_log_record_by_colnames(ip=ip)
            _run_cmd(UNBAN_IP.format(ip=ip))
            del _banned[ip]
        else:
            print("Bug prevented")

def get_banned_ips():
    return _banned.values()


def create_ban_thread(ip, timeout, service="unspecified"):
    """ban an ip for <timeout> minutes for the specified services
    Args:
        ip: banned ip
        timeout: ban time in minutes
        services: banned services. Defaults to "all" to ban all.
    """
    if ip in _banned:
        return
    timestamp = datetime.datetime.now()
    _banned[ip] = BanEntry(ip, service, timestamp, timeout)
    ban_ip(ip)
    Timer(timeout * 60, _unban_ip_with_check, (ip, timestamp)).start()


if __name__ == "__main__":
    clean()
    init()
    # create_ban_thread("10.87.2.46", .2)
