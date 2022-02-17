import sys
import re
import platform
import subprocess

if __name__ == "__main__":
    # Check if all arguments are provided.
    if len(sys.argv) != 3:
       print("Incorrect number of arguments provided")
       exit(1)

    # sys.argv[0] takes the name of the script.
    interface_name = str(sys.argv[1])
    mac_address = str(sys.argv[2])

    # Check if MAC address is of the correct format by comparing it to a regex.
    regex_mac = "(?:[0-9a-fA-F]:?){12}"
    if not re.match(regex_mac, mac_address.lower()):
        print("Provided Mac adress ", mac_address," is in incorrect format")
        exit(1)

    # Spoof MAC adress
    subprocess.call(["ip", "link", "set", "dev",  interface_name, "down"])
    subprocess.call(["ip", "link", "set", "dev", interface_name, "address", mac_address]) 
    subprocess.call(["ip", "link", "set", "dev", interface_name, "up"])
    
    # Setup for the ping command
    ping_cmd = ["ping", "-c", "1", "192.168.124.20"]
    if platform.system().lower() == "windows":
       ping_cmd[1] = "-n"
    
    # Ping target address a total of 4 times.
    for i in range(1, 5):
        process = subprocess.Popen(ping_cmd, stdout=subprocess.PIPE)
        stdout, _ = process.communicate()
        if process.returncode == 0:
           print("Got ICMP-reply to ICMP-echo - ", i)
        else:
           print("Ping failed: ", stdout.decode("ASCII"))
    
