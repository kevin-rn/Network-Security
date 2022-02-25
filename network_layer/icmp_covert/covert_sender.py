import sys
from scapy.all import *
from cryptography.fernet import Fernet
import base64

if __name__ == "__main__":
	# Store arguments in variables
        ip_receiver = str(sys.argv[1])
        payload = str(sys.argv[2])

	# Use hardcoded string as key for encryption of the message
        hardcoded_key = "xThisxisxaxsharedxhardcodedxkeyx".encode("ascii")
        covert_key = base64.urlsafe_b64encode(hardcoded_key)
        fernet = Fernet(covert_key)

	# Encrypt message and send
        message =  fernet.encrypt(str.encode(payload))
        send(IP(dst=ip_receiver) / ICMP(type=1) / message, verbose=False)
