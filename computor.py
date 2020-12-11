import matplotlib.pyplot as plt
from fractions import Fraction
import argparse
import numpy as np
import re
import sys

### Parsing function ###
def formating(arr):
    sign = ""
    deg0 = np.array([], dtype=object)
    deg1 = np.array([], dtype=object)
    deg2 = np.array([], dtype=object)
    for elem in arr:
        if elem == "+" or elem =="-":
            if not sign == "":
                print("Man, you need only one operator")
                sys.exit(-1)
            sign = elem
        else:
            if sign == "+": sign = ""
            if ("X^2" in elem or "x^2" in elem) and elem[-2] == "^":
                nbr = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", (sign + elem))
                if len(nbr) == 2: deg2 = np.append(deg2, nbr[0])
                else: deg2 = np.append(deg2, float(sign + '1'))
            elif "X" == elem[-1] or "x" == elem[-1] or (("X^1" in elem or "x^1" in elem)  and "^" == elem[-2]):
                nbr = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", (sign + elem))
                if len(nbr) == 2 or (("X" == elem[-1] or "x" == elem[-1]) and len(nbr) > 0): deg1 = np.append(deg1, nbr[0])
                else: deg1 = np.append(deg1, float(sign + '1'))
            elif not ("X" in elem or "x" in elem) or "X^0" in elem or "x^0" in elem:
                nbr = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", (sign + elem))
                if len(nbr) == 2 or not ("X" in elem or "x" in elem): deg0 = np.append(deg0, nbr[0])
                else: deg0 = np.append(deg0, float(sign + '1'))
            else:
                print(("Nah, that degree is too high for me ! Degree found: " + elem[-1]) if elem[-1].isnumeric() and (elem[-2] == "^") else ("One of your x is wrongly formated !"))
                sys.exit(-1)
            sign = ""
    return deg0, deg1, deg2

### Function which add all elements to get only one number per degree ###
def addf(arr):
    result = 0.0
    fnum = 1
    for element in arr:
        if str(element)[::-1].find('.') > fnum: fnum = str(element)[::-1].find('.')
        result += float(element)
        result = round(result, fnum)
    if result.is_integer(): result = int(result)
    return result

### Function which add all element of the same degree in the same array and return a single array ###
def allInOne(arr):
    for deg in arr:
        for elem in deg[1]:
            deg[0] = np.append(deg[0], str(float(elem) * -1))
    return [addf(arr[0][0]), addf(arr[1][0]), addf(arr[2][0])]

### Main program ###
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("polynome", type=str, help="mixing sequence")
    parser.add_argument('-g', "--graph", help="print graph of the given valid polynomial", action="store_true")
    args = parser.parse_args()
    authorizedStr = "0123456789 =+-*xX^."
    for x in args.polynome:
        if not x in authorizedStr:
            print("Why did you use you use an unauthorized character ?")
            sys.exit(-1)
    if not "=" in args.polynome:
        print("WTF's wrong with you ? You forgot the \"=\" !")
        sys.exit(-1)
    elif args.polynome.find("=") != args.polynome.rfind("="):
        print("WTF's wrong with you ? You put 2 \"=\" !")
        sys.exit(-1)
    polynome = args.polynome.split("=")
    polynome = list(map(str.strip, polynome))
    first = list(map(str.strip, (re.split("(\+|\-)", polynome[0]))))
    second = list(map(str.strip, (re.split("(\+|\-)", polynome[1]))))
    first = [x for x in first if x]
    second = [x for x in second if x]
    for elem in first:
        if elem.find("X") != elem.rfind("X") or elem.find("x") != elem.rfind("x") or elem.find("^") != elem.rfind("^") or ("x" in elem and "X" in elem):
            print("That's a wrongly formated input man")
            sys.exit(-1)
    fdeg0, fdeg1, fdeg2 = formating(first)
    sdeg0, sdeg1, sdeg2 = formating(second)
    fdeg0 = np.append(fdeg0, str(float(0)))
    Arr = allInOne(np.array([[fdeg0, sdeg0], [fdeg1, sdeg1], [fdeg2, sdeg2]], dtype=object))
    print("Reduced form: \033[1m" + (((str(Arr[0]) if Arr[0] >= 0 else ("- " + str(Arr[0] * -1))) + " * X^0" if Arr[0] != 0 else "")
            + (((" + " if Arr[0] != 0 else "") + str(Arr[1]) if Arr[1] > 0 else (" - " + str(Arr[1] * -1))) + " * X^1" if Arr[1] != 0 else "")
            + (((" + " if (Arr[1] != 0 or Arr[0] != 0) else "") + str(Arr[2]) if Arr[2] > 0 else (" - " + str(Arr[2] * -1))) + " * X^2" if Arr[2] != 0 else "")
            if not (Arr[0] == 0 and Arr[1] == 0 and Arr[2] == 0) else "0") + " = 0\033[0m")
    print("diferent style: \033[1m" + (((str(Arr[0]) if Arr[0] >= 0 else ("- " + str(Arr[0] * -1))) if Arr[0] != 0 else "")
            + (((" + " if Arr[0] != 0 else "") + str(Arr[1]) if Arr[1] > 0 else (" - " + str(Arr[1] * -1))) + "x" if Arr[1] != 0 else "")
            + (((" + " if (Arr[1] != 0 or Arr[0] != 0) else "") + str(Arr[2]) if Arr[2] > 0 else (" - " + str(Arr[2] * -1))) + "x^2" if Arr[2] != 0 else "")
            if not (Arr[0] == 0 and Arr[1] == 0 and Arr[2] == 0) else "0") + " = 0\033[0m")
    print("Polynomial degree: " + "\033[1m" + "\033[91m" + ("2" if (Arr[2] != 0) else ("1" if (Arr[1] != 0) else "0")) + "\033[0m")
    Arr = list(map(float, Arr))
    
    ### Case 0 = 0 ###
    if Arr[0] == 0 and Arr[1] == 0 and Arr[2] == 0:
        print("\033[1mAll numbers are solution !")
    
    ### Case number = 0 ###
    elif Arr[1] == 0 and Arr[2] == 0:
        print("\033[1mThere is no solution !")
    
    ### Case degree 1 like number + number * x = 0 ###
    elif Arr[2] == 0:
        print("The only solution is \033[1mx = "
                + (str(Fraction((-1 * int(Arr[0])), int(Arr[1]))) if Arr[0].is_integer() and Arr[1].is_integer()
                else (str(-1 * Arr[0]) + "/" + str(Arr[1]))))
    
    ### Case degree 2 like number + number * x + number * x^2 = 0 ###
    elif Arr[2] != 0:
        delta = Arr[1]**2 - 4 * Arr[2] * Arr[0]
        delta = round(delta, 10)
        if delta.is_integer(): delta = int(delta)
        print("The discriminant is strickly "
                + "\033[1m" + "\033[91m" + ("positive" if delta > 0 else ("negative" if delta < 0 else "equal to zero")) + "\033[0m")
        if delta != 0: print("\033[1m\033[91mΔ = " + str(delta) + "\033[0m")
        if delta == 0:
            print("The only solution is \033[1mx = "
                    + (str(Fraction((-1 * int(Arr[1])), int(2 * Arr[2]))) if Arr[1].is_integer() and (2 * Arr[2]).is_integer()
                    else (str(-1 * Arr[1]) + "/" + str(2 * Arr[2]))))
        
        elif delta > 0:
             print("The two solutions are:\033[1m"
                        + "\nx = " + (str(Fraction((-1 * int(Arr[1]) - int(np.sqrt(delta))), int(2 * Arr[2]))) if np.sqrt(delta).is_integer() and Arr[1].is_integer() and ( 2 * Arr[2]).is_integer() else ("(" + str(-1 * Arr[1]) + " - √" + str(delta) + ") / " + str(2 * Arr[2]) + " or approximately " + str("{:.4f}".format((-1 * Arr[1] - np.sqrt(delta)) / (2 * Arr[2])))))
                        + "\nx = " + (str(Fraction((-1 * int(Arr[1]) + int(np.sqrt(delta))), int(2 * Arr[2]))) if np.sqrt(delta).is_integer() and Arr[1].is_integer() and ( 2 * Arr[2]).is_integer() else ("(" + str(-1 * Arr[1]) + " + √" + str(delta) + ") / " + str(2 * Arr[2]) + " or approximately " + str("{:.4f}".format((-1 * Arr[1] + np.sqrt(delta)) / (2 * Arr[2]))))))
        
        elif delta < 0:
            delta = -delta
            print("The two complex solutions are:\033[1m"
                + "\nx = " + (str(Fraction(int(-1 * Arr[1]),int(2 * Arr[2])))  if Arr[1].is_integer() and (2 * Arr[2]).is_integer() else (str(-1 * Arr[1]) + "/" + (str(int(2 * Arr[2])) if (2 * Arr[2]).is_integer() else str(2 * Arr[2]))))
                + " - (" +(str(Fraction((int(np.sqrt(delta))),int(2 * Arr[2]))) if np.sqrt(delta).is_integer() and (2 * Arr[2]).is_integer() else ("√" + str(delta) + " / " + (str(int(2 * Arr[2])) if (2 * Arr[2]).is_integer() else str(2 * Arr[2])))) + ")i"
                + "\nx = " + (str(Fraction(int(-1 * Arr[1]),int(2 * Arr[2])))  if Arr[1].is_integer() and (2 * Arr[2]).is_integer() else (str(-1 * Arr[1]) + "/" + (str(int(2 * Arr[2])) if (2 * Arr[2]).is_integer() else str(2 * Arr[2]))))
                + " + (" +(str(Fraction((int(np.sqrt(delta))),int(2 * Arr[2]))) if np.sqrt(delta).is_integer() and (2 * Arr[2]).is_integer() else ("√" + str(delta) + " / " + (str(int(2 * Arr[2])) if (2 * Arr[2]).is_integer() else str(2 * Arr[2])))) + ")i")
    
    ###Optional graph###        
    if args.graph and (Arr[1] != 0 or Arr[2] != 0):
        xgraph = np.linspace(-10,10,num=100)
        fx = []
        for i in range(len(xgraph)):
            fx.append(Arr[2]*xgraph[i]**2 + Arr[1]*xgraph[i] + Arr[0])
        plt.plot(xgraph,fx)
        plt.grid()
        plt.axvline()
        plt.axhline()
        plt.show()
