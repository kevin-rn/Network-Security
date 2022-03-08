import sys

if __name__ == "__main__":
    # try/except in case of missing arguments or incorrect format
    try:
        h = int(sys.argv[1])
        g = int(sys.argv[2])
        n = int(sys.argv[3])

        g_inv = pow(g, -1, n)
        dlp_add = (h * g_inv) % n
        print(dlp_add)

    except:
        print("ERROR")
        exit()
