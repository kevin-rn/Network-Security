import re

"""
get_ciphers: Returns ciphertexts copied from otp_ciphertexts.txt
"""
def get_ciphers():
    # Get ciphertext strings from file
    # ciphers = [cipher.strip() for cipher in open("otp_ciphertexts.txt", 'r')]

    # Alternative: hardcode ciphertext strings in array
    ciphers = [
	0c30960245dcb09dafae94b43ac421685213a4a5
        "252d246d2b3f26692e35383970262b2d20763122723226372a75203c2a3f692220292221373c3174",
        "6323382963373d2723743524353264263c22782b3d613a3a6227253d23342c243a67243972292e347968",
       "222c326d0ae2818339693521232e7008642b3238e2818138722336740f342e362874",
        "252d246d0a7a3f272923712a3c2d643b3c242c3f722e3574363d253d232b",
        "222c326d30323165663b396a70322c2d733d3623253273273736247325783f353b3e65213b3c3634276970",
        "6300333e2a3e313a6a74222335e281983768203e3d6072203d30621ce281953e64116570",
        "6323382963e2818e74262e74352e313368683b392f6c2234292e2e3c223464313d70282b296d3b3b6378",
        "222c326de281977a3b216630342a226d64203c21783c273b29382b3b2b732d2c6931252b6524216962",
        "0f27226d2e3f743a23316b6b362e313a73223121373273322b2329732d2b69243e22293b3768",
        "222c326d2535213b662038263532643b36203d22722820e281802d3d6c3721393b71",
        "630b763e2b3b3825663a343d3533642f362278383d612723273b382a64393d703d2f2439723a232c276970",
        "630a393a262c313b6a7425233561093d3f22313c3e283035363c233d640c2832252265293d26e2819b2c623b392e3d25253c7c71",
        "2f27226a307a203b3f74162e3f263629233e21",
        "0f2d38292c3474203574252335612729233f2c2d3e613c3262133e322a3b2c",
        "222c326d1135392c663d226b242921683037282526203f742d336c0a2b2a2223212e3728",
        "222c326d133b262035747c6b3f29642c36372a6d7225363530746c",
        "630b7620362920692e35272e7023212d3d763b24332f343126752a3c36780f3c26352023312d63"
        ]
    
    # As each cipherstring has been encrypted using the same key, we can shorten it to the shortest ciphertext length
    min_len = len(min(ciphers, key=len))
    ciphers = [str[:min_len] for str in ciphers]
    return ciphers

"""
xor_str: Performs xor operation between two strings
"""
def xor_str(str1, str2):
    xorred_string = hex(int(str1, 16) ^ int(str2, 16))
    return "".join(xorred_string)[2:] # remove 0x part with [2:]

"""
hex_str: Converts plain text string to hexadecimal format.
"""
def hex_str(text):
    return text.encode("utf-8").hex()

"""
hex_to_plain: Converts hexadecimal format to plain text.
"""
def hex_to_plain(text):
    return bytes.fromhex(text).decode("ASCII")

def guess_key_based_on_space():
    """
    ATTEMPT 1:
    Space character ' ' --> hex: 0x20, binary 0100 0000 where xorring only flips one bit

    Take cipher texts of same length:
    Cipher 1:       63 0b 76 20 36 29 20 69 2e 35 27 2e 70
    Cipher 2:       22 2c 32 6d 0a e2 81 83 39 69 35 21 23
    Cipher 3:       0f 27 22 6d 2e 3f 74 3a 23 31 6b 6b 36
    
    Xor them:
    1 ^ 2:	        41 27 44 4D 3C CB A1 EA 17 5C 12 0F 53
    1 ^ 3:	        6C 2C 54 4D 18 16 54 53 0D 04 4C 45 46
    2 ^ 3:	        2D 0B 10 00 24 DD F5 B9 1A 58 5E 4A 15

    Check for each column if the hexadecimal number is an alphanum ascii character
    1. for example 41 is A, 6C is I and 2D is not a printable character.
    So this means that xorring with cipher 1 will result in printable character so cipher 1 is a space.
    2. for example we see two times 4D and 00 which means that space was used for the ciphers resulting in 4D (cipher 1 & 2)

    Plain text 1:    _  ?? ??  _ ?? ?? ?? ?? ?? ?? ?? ??  _
    Plain text 2:   A  ??  D  _ ?? ?? ?? ?? ?? ?? ?? ??  S
    Plain text 3:   I  ??  T  M ?? ?? ?? ?? ?? ?? ?? ??  F

    Guess the key based on previous observations
    1. For the key we can now xor the cipher 1 '0x63' with hexadecimal character of space '0x20' to get '0x43'
    2. 4D was twice encountered so we can xor the original hexadecimal of the cipher '0x6d' with '0x20' to get '0x4d'
    Key:            43 ?? 56 4d ?? ?? ?? ?? ?? ?? ?? ?? 50
    """

    def check_format(text):
        check_str = hex_to_plain(text)
        match_format = re.match("^[a-zA-Z0-9_]+$", check_str)
        return bool(match_format)

    ciphers = get_ciphers()[:3]
    xor1_2 = xor_str(ciphers[0], ciphers[1])
    xor1_3 = xor_str(ciphers[0], ciphers[2])
    xor2_3 = xor_str(ciphers[1], ciphers[2])
    
    possible_key = []
    # Every cipher is the same length so we can just loop over the length of one of them.
    for idx in range(len(xor1_2)):
        temp = []
        temp.append(check_format(xor1_2[idx]))
        temp.append(check_format(xor1_3[idx]))
        temp.append(check_format(xor2_3[idx]))

        #TODO: check condition for non-printable character with other two printable

        char_to_xor = None
        possible_key.append(xor_str(char_to_xor, "20"))

    return "".join(possible_key)

"""
ATTEMPT 2:
crib_drag: Performs crib dragging on all ciphertexts given a string.
"""
def crib_drag(input_str):
    crib_str = hex_str(input_str)
    ciphers = get_ciphers()
    for cipher in ciphers:
        for idx in range(len(ciphers)-len(crib_str)):
            key = xor_str(cipher[idx:], crib_str)
            for cipher2 in ciphers:
                text = xor_str(cipher2, crib_str)
                print("For cipher: {}, possible text: {}, key: {}".format(cipher, text, hex_str(key)))

if __name__ == "__main__":
    # crib_drag(" the ")

<<<<<<< HEAD
    key =    "4342564d435a54494654514b504144485356584c5241535442554c534458"
    ciphers = get_ciphers()
    for c in ciphers:
        mess = hex_to_plain(xor_str(c[:len(key)], key[:len(c)]))
        print(mess)

    message = "222c326d2535213b662038263532643b3a2e78252161273c2b2738362136"
    xorred = xor_str(message, key)
    decrypt_message = hex_to_plain(xorred)
    print(decrypt_message)
