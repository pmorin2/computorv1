from fractions import Fraction
import argparse
import numpy as np
import re
import sys

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
            if "X^2" in elem or "x^2" in elem:
                nbr = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", (sign + elem))
                if len(nbr) == 2: deg2 = np.append(deg2, nbr[0])
                else: deg2 = np.append(deg2, float(sign + '1'))
            elif "X" == elem[-1] or "x" == elem[-1] or "X^1" in elem or "x^1" in elem:
                nbr = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", (sign + elem))
                if len(nbr) == 2 or (("X" == elem[-1] or "x" == elem[-1]) and len(nbr) > 0): deg1 = np.append(deg1, nbr[0])
                else: deg1 = np.append(deg1, float(sign + '1'))
            elif not ("X" in elem or "x" in elem) or "X^0" in elem or "x^0" in elem:
                nbr = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", (sign + elem))
                if len(nbr) == 2 or not ("X" in elem or "x" in elem): deg0 = np.append(deg0, nbr[0])
                else: deg0 = np.append(deg0, float(sign + '1'))
            else:
                print("Nah, that degree is too high for me")
                sys.exit(-1)
            sign = ""
    return deg0, deg1, deg2

def addf(arr):
    result = 0.0
    fnum = 1
    for element in arr:
        if element[::-1].find('.') > fnum: fnum = element[::-1].find('.')
        result += float(element)
        result = round(result, fnum)
    if result.is_integer(): result = int(result)
    return result

def allInOne(arr):
    for deg in arr:
        for elem in deg[1]:
            deg[0] = np.append(deg[0], str(float(elem) * -1))
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
    polynome = list(map(str.strip, polynome))
    first = list(map(str.strip, (re.split("(\+|\-)", polynome[0]))))
    second = list(map(str.strip, (re.split("(\+|\-)", polynome[1]))))
    first = [x for x in first if x]
    second = [x for x in second if x]
    fdeg0, fdeg1, fdeg2 = formating(first)
    sdeg0, sdeg1, sdeg2 = formating(second)
    fdeg0 = np.append(fdeg0, str(float(0)))
    Arr = allInOne(np.array([[fdeg0, sdeg0], [fdeg1, sdeg1], [fdeg2, sdeg2]], dtype=object))
    print("Forme réduite: " + (((str(Arr[0]) if Arr[0] >= 0 else ("- " + str(Arr[0] * -1))) + " * X^0" if Arr[0] != 0 else "")
            + (((" + " if Arr[0] != 0 else "") + str(Arr[1]) if Arr[1] > 0 else (" - " + str(Arr[1] * -1))) + " * X^1" if Arr[1] != 0 else "")
            + (((" + " if (Arr[1] != 0 or Arr[0] != 0) else "") + str(Arr[2]) if Arr[2] > 0 else (" - " + str(Arr[2] * -1))) + " * X^2" if Arr[2] != 0 else "")
            if not (Arr[0] == 0 and Arr[1] == 0 and Arr[2] == 0) else "0") + " = 0")
    print("Autre écriture: " + (((str(Arr[0]) if Arr[0] >= 0 else ("- " + str(Arr[0] * -1))) if Arr[0] != 0 else "")
            + (((" + " if Arr[0] != 0 else "") + str(Arr[1]) if Arr[1] > 0 else (" - " + str(Arr[1] * -1))) + "x" if Arr[1] != 0 else "")
            + (((" + " if (Arr[1] != 0 or Arr[0] != 0) else "") + str(Arr[2]) if Arr[2] > 0 else (" - " + str(Arr[2] * -1))) + "x^2" if Arr[2] != 0 else "")
            if not (Arr[0] == 0 and Arr[1] == 0 and Arr[2] == 0) else "0") + " = 0")
    print("Degré du polynome: " + ("2" if (Arr[2] != 0) else ("1" if (Arr[1] != 0) else "0")))
    if Arr[0] == 0 and Arr[1] == 0 and Arr[2] == 0:
        print("Tout les nombres sont solutions !")
    elif Arr[1] == 0 and Arr[2] == 0:
        print("L'équation n'a pas de solution !")
    elif Arr[2] == 0:
        solution = Fraction((-1 * Arr[0]), Arr[1])
        print("l'unique solution est x = " + str(solution))
    elif Arr[2] != 0:
        delta = Arr[1]**2 - 4 * Arr[2] * Arr[0]
        print("Le discriminant est strictement "
                + ("positif" if delta > 0 else ("négatif" if delta < 0 else "egal à zéro")))
        if delta == 0:
            solution = Fraction((-1 * Arr[1]), (2 * Arr[2]))
            print("l'unique solution est x = " + str(solution))
        elif delta > 0:
            if np.sqrt(delta).is_integer():
                solution1 = Fraction((-1 * Arr[1] - int(np.sqrt(delta))),(2 * Arr[2]))
                solution2 = Fraction((-1 * Arr[1] + int(np.sqrt(delta))),(2 * Arr[2]))
                print("les deux solutions sont:\nx = " + str(solution1) + "\nx = " + str(solution2))
            else:
                print("les deux solutions sont:\nx = (" + str(-1 * Arr[1]) + " - √" + str(delta) + ") / " + str(2 * Arr[2]) + " soit environ " + str("{:.4f}".format((-1 * Arr[1] - np.sqrt(delta)) / (2 * Arr[2])))
                        + "\nx = (" + str(-1 * Arr[1]) + " + √" + str(delta) + ") / " + str(2 * Arr[2])  + " soit environ " + str("{:.4f}".format((-1 * Arr[1] + np.sqrt(delta)) / (2 * Arr[2]))))
        elif delta < 0:
            delta = -delta
            print("les deux solutions complexes sont:\nx = (" + str(-1 * Arr[1]) + " - √" + str(delta) + ") / " + str(2 * Arr[2])
                    + "\nx = (" + str(-1 * Arr[1]) + " + √" + str(delta) + ") / " + str(2 * Arr[2]))
