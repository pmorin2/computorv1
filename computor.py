import argparse
import numpy as np
import re
import sys

def formating(arr):
    sign = ""
    deg0 = np.array([])
    deg1 = np.array([])
    deg2 = np.array([])
    for elem in arr:
        if elem == "+" or elem =="-":
            if not sign == "":
                print("Man, you need only one operator")
                sys.exit(-1)
            sign = elem
        else:
            if sign == "+": sign = ""
            if "X^2" in elem or "x^2" in elem:
                nbr = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", (sign + elem))
                if len(nbr) == 2: deg2 = np.append(deg2, nbr[0])
                else: deg2 = np.append(deg2, float(sign + '1'))
            elif "X" == elem[-1] or "x" == elem[-1] or "X^1" in elem or "x^1" in elem:
                nbr = re.findall(r"[-+]?\d*\.\d+|\d+", (sign + elem))
                if len(nbr) == 2 or (("X" == elem[-1] or "x" == elem[-1]) and len(nbr) > 0): deg1 = np.append(deg1, nbr[0])
                else: deg1 = np.append(deg1, float(sign + '1'))
            elif not ("X" in elem or "x" in elem) or "X^0" in elem or "x^0" in elem:
                nbr = re.findall(r"[-+]?\d*\.\d+|\d+", (sign + elem))
                if len(nbr) == 2 or not ("X" in elem or "x" in elem): deg0 = np.append(deg0, nbr[0])
                else: deg0 = np.append(deg0, float(sign + '1'))
            sign = ""
    return deg0, deg1, deg2

def addf(arr):
    result = 0.0
    fnum = 1
    for element in arr:
        if element[::-1].find('.') > fnum: fnum = element[::-1].find('.')
        result += float(element)
        result = round(result, fnum)
        print(result)
    return result

def allInOne(arr):
    for deg in arr:
        for elem in deg[1]:
            deg[0] = np.append(deg[0], float(elem) * -1)
    return [addf(arr[0][0]), addf(arr[1][0]), addf(arr[2][0])]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("polynome", type=str, help="mixing sequence")
    #parser.add_argument('-f', "--french", help="french human undertandable moves", action="store_true")
    args = parser.parse_args()
    if not "=" in args.polynome:
        print("WTF's wrong with you ? You forgot the \"=\" !")
        sys.exit(-1)
    polynome = args.polynome.split("=")
    print(polynome[0])
    print(polynome[1])
    first = list(map(str.strip, (re.split("(\+|\-)", polynome[0]))))
    second = list(map(str.strip, (re.split("(\+|\-)", polynome[1]))))
    fdeg0, fdeg1, fdeg2 = formating(first)
    sdeg0, sdeg1, sdeg2 = formating(second)
    print (fdeg0, sdeg0)
    print (fdeg1, sdeg1)
    print (fdeg2, sdeg2)
    Arr = allInOne(np.array([[fdeg0, sdeg0], [fdeg1, sdeg1], [fdeg2, sdeg2]], dtype=object))
    print (Arr)
