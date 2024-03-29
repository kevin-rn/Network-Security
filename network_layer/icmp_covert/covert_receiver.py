from scapy.all import *
from cryptography.fernet import Fernet
import base64

def print_pkt(pkt):
	# Use hardcoded string as key to decrypt message
        hardcoded_key = "xThisxisxaxsharedxhardcodedxkeyx".encode("ascii")
        covert_key = base64.urlsafe_b64encode(hardcoded_key)
        fernet = Fernet(covert_key)
	
	# Decrypt message from the sniffed packet
        message = fernet.decrypt(pkt.load)
        print(message.decode())

if __name__ == "__main__":
        sniff(prn=print_pkt, filter='icmp')

