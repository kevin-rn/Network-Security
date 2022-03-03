import sys
import math


def solveContinuousLog(h, g):
    return math.log(h, g)

if __name__ == "__main__":
    # Catch exception if arguments are not integers or missing
    try:
        h = float(sys.argv[1])
        g = float(sys.argv[2])
        x = solveContinuousLog(h, g)

        # check if solution has been found
        if x == -1:
            print("ERROR")
        else:
            print(x)
    except:
        print("ERROR")
        exit()




