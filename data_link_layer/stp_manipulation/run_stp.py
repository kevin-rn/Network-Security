import sys

if __name__ == "__main__":
    # Check if all arguments are provided.
    if len(sys.argv) != 5:
       print("Incorrect number of arguments provided")
       exit(1)

    fst_interface = str(sys.argv[1])
    snd_interface = str(sys.argv[2])
    bridge_id = str(sys.argv[3])
    bridge_priority = int(sys.argv[4])
	
    # Check if bridge ID matches MAC address format.
    regex_mac = "(?:[0-9a-fA-F]:?){12}"
    if not re.match(regex_mac, mac_address.lower()):
        print("Provided bridge ID ", mac_address," is in incorrect format")
        exit(1)
        
