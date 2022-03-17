import sys

if __name__ == "__main__":
    # try/except in case of missing arguments or incorrect format
    try: 
        input_str = str(sys.argv[1])
        # Should not be longer than 50 characters and contains only ascii characters.
        if len(input_str) > 50 or not input_str.isascii():
            print("ERROR")
        else:
            # Capital characters used as the key.
            one_time_chars = ['B', 'H', 'Z', 'A', 'P', 'S', 'I', 'E', 'Z', 'S', 
            'L', 'A', 'G', 'V', 'C', 'E', 'X', 'L', 'E', 'U', 'F', 'X', 'X', 'X', 
            'G', 'O', 'F', 'J', 'L', 'D', 'H', 'S', 'O', 'S', 'C', 'O', 'Q', 'O', 
            'J', 'G', 'X', 'W', 'W', 'P', 'R', 'Z', 'X', 'D', 'M', 'M']

            otp = ""
            for index in range(len(input_str)):
                # perform XOR operation (modulo 2 addition)
                mod_add = ord(one_time_chars[index]) ^ ord(input_str[index])
                
                # remove 0x from string and add 0 in case of single digit hex
                hex_str = hex(mod_add).replace('0x', '')
                if len(hex_str) == 1:
                    otp += "0" + hex_str
                else:
                    otp += hex_str
            print(otp)
    except:
        print("ERROR")