import numpy as np
from scipy.optimize import curve_fit
import sys

"""
computeNumberOfStrings: Computes number of permutations possible from alphabet size and ciphertext length
"""
def computeNumberOfStrings(n, lngth):
    return pow(n, lngth)


"""
fitCurve: 
"""
def fitCurve(x, y):
    def func(x, c, d):
        return c * np.exp(d * x)

    params, _ = curve_fit(func, x, y, p0=(1., 1.))

    return params.tolist()


"""
exactParams:
"""
def exactParams(n):
    # compute/return the exact params c and d
    c = 1
    d = 2

    return [c, d]


if __name__ == "__main__":
    # try-except in case arguments are missing/incorrect format
    try:
        func_name = str(sys.argv[1])

        if func_name == 'computeNumberOfStrings':
            arg1 = int(sys.argv[2])
            arg2 = int(sys.argv[3])
            result = computeNumberOfStrings(arg1, arg2)
            print(result)

        elif func_name == 'fitCurve':
            arg1 = str(sys.argv[2]).split(",")
            arg2 = str(sys.argv[3]).split(",")

            x = [int(i) for i in arg1]
            y = [int(i) for i in arg2]
            arr = ",".join(str(i) for i in fitCurve(x, y))
            print(arr)

        elif func_name == 'exactParams':
            arg1 = sys.argv[2]
            arr = ",".join(exactParams(arg1))
            print(arr)

    except:
        print("ERROR")