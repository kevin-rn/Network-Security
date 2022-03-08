import sys
import math

"""
solveContinuousLog: Calculates x using logarithm following 'g^x = h' -> 'x = log_g(h)'
"""
def solveContinuousLog(h, g):
    return math.log(h, g)

if __name__ == "__main__":
    # try/except in case of missing arguments or incorrect format
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




