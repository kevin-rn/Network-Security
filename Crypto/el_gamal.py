import sys
import re

from numpy import diff

"""
Encryption following the ELGamal encryption algorithm.
"""
def elGamalEncrypt(h, g, n, r, t):
    # Calculate c1
    c1 = pow(g, r, n)
    power = pow(h, r)

    # Convert every character of plain text t to binary format
    message = []
    for character in t:
        binary_format = format(ord(character), 'b')
        diff = 8 - len(binary_format)
        binary_format = ('0' * diff) + binary_format
        message.append(binary_format)

    # Convert message to decimal format
    decimal_message = int("".join(message), 2)
    c2 = (decimal_message * power) % n

    return c1, c2

"""
Decryption following the ELGamal encryption algorithm.
"""
def elGamalDecrypt(n, a, c1, c2):
    # Perform calculation to retrieve plain text t
    K = pow(c1, a, n)
    t = (c2 * pow(K, -1, n)) % n

    # Convert decimal format back to plain text
    bin_message = format(t, 'b')
    # Do some padding if needed
    diff = 8 - (len(bin_message) % 8)
    if diff != 0:
        bin_message = "0" * diff + bin_message

    bin_message = re.findall('.{1,8}', bin_message)
    character_format = [chr(int(i, 2)) for i in bin_message]
    message = "".join(character_format)

    return message

# Check input arguments and calls correct function.
if __name__ == "__main__":
    func_name = str(sys.argv[1])

    try:
        if func_name == 'elGamalEncrypt':
                h = int(sys.argv[2])
                g = int(sys.argv[3])
                n = int(sys.argv[4])
                r = int(sys.argv[5])
                t = str(sys.argv[6])
                c1, c2 = elGamalEncrypt(h, g, n, r, t)
                print("{}, {}".format(c1, c2))

        elif func_name == 'elGamalDecrypt':
                n  = int(sys.argv[2])
                a  = int(sys.argv[3])
                c1 = int(sys.argv[4])
                c2 = int(sys.argv[5])
                message = elGamalDecrypt(n, a, c1, c2)
                print(message)
        else:
            print("ERROR")
    # In case casting to int failed or incorrect number of arguments.
    except:
        print("ERROR")
        sys.exit()
