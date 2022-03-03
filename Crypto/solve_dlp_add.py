from re import I, X
import sys

if __name__ == "__main__":
    # Check if two arguments have been provided
    if len(sys.argv) != 4:
        print("ERROR")
        exit()

    h = sys.argv[1]
    g = sys.argv[2]
    n = sys.argv[3]

    try:
        h = int(h)
        g = int(g)
        n = int(n)

        dlp_add = (h * pow(g, -1, n)) % n
        print(dlp_add)

    except ValueError:
        print("ERROR")
        exit()
