"""
get_ciphers: Returns ciphertexts copied from otp_ciphertexts.txt
"""
def get_ciphers(paired = False):
    # ciphers = [cipher.strip() for cipher in open("otp_ciphertexts.txt", 'r')]
    ciphers = [
        "0ae2819b76206329213b2374186be281892c64263c22780d36207f74313d29733739203469", 
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
        "63363e2c377d276927383d6b27332b2634",
        "0a653b6d203f263d273d3f6a70",
        "630b7620362920692e35272e7023212d3d763b24332f343126752a3c36780f3c26352023312d63"
        ]

    if paired:
        same_length_pairs = []
        for i in range(len(ciphers)-1):
            for j in range(len(ciphers)):
                if i < j and len(ciphers[i]) == len(ciphers[j]):
                    same_length_pairs.append([ciphers[i], ciphers[j]])
        return same_length_pairs
    else:
        return ciphers
"""
xor_str: Performs xor operation between two strings
"""
def xor_str(str1, str2):
    xor_pairs = [chr(ord(a) ^ ord(b)) for a, b in zip(str1, str2)]
    return "".join(xor_pairs)

"""
hex_str: Converts plain text string to hexadecimal format.
"""
def hex_str(str):
    return str.encode("utf-8").hex()

"""
crib_drag_start: Performs the crib dragging with an initial guess word to see other possible texts.
"""
def crib_drag_start():
    initial = " cake "
    pairs = get_ciphers(True)
    for p in pairs:
        for cipher in p:
            for index in range(len(cipher)-len(hex_str(initial))):
                key = xor_str(cipher[index:], initial)
                for p2 in p:
                    possible_text = xor_str(p2[index:], key)
                    print("For cipher: {}, possible text: {}, key: {}".format(hex_str(cipher), possible_text, hex_str(key)))

"""
crib_drag: Performs crib dragging on all ciphertexts given a string.
"""
def crib_drag(str):
    ciphers = get_ciphers()
    for cipher in ciphers:
        key = xor_str(cipher, str)
        for cipher2 in ciphers:
            if cipher != cipher2:
                for index in range(len(ciphers)-len(hex_str(str))):
                    possible_text = xor_str(cipher2[index:], key)
                    print("For cipher: {}, possible text: {}, key: {}".format(hex_str(cipher), possible_text, hex_str(key)))

if __name__ == "__main__":
    # crib_drag_start()
    message = "222c326d2535213b662038263532643b3a2e78252161273c2b2738362136"
    key = crib_drag(" secret ")
    # print(xor_str(message, key))