__author__ = 'lenk'

import sys

def readFASTA(fileName):
    rna = ''
    with open(fileName, 'r') as fin:
        fin.readline()
        for line in fin:
            rna += line.strip()
    return rna

def complement(basePair):
    if 'A' in basePair and 'U' in basePair:
        return True
    elif 'C' in basePair and 'G' in basePair:
        return True
    elif 'G' in basePair and 'U' in basePair:
        return True
    return False

def main():
    a = 1

    ebiIL = {1: 1000, 2: 4.1, 3: 5.1, 4: 4.9, 5: 5.3, 10: 6.3, 15: 6.7, 20: 7.0, 25: 7.2, 30: 7.4}

    ebiB = {1: 1000, 2: 3.1, 3: 3.5, 4: 4.2, 5: 4.8, 10: 5.5, 15: 6.0, 20: 6.3, 25: 6.5, 30: 6.7}

    eh = {1: 1000, 2: 1000, 3: 4.1, 4: 4.9, 5: 4.4, 10: 5.3, 15: 5.8, 20: 6.1, 25: 6.3, 30: 6.5}

    for i in range(6, 30):
        if i % 5 != 0:
            j = i - i % 5
            ebiIL[i] = ebiIL[j]
            ebiB[i] = ebiB[j]
            eh[i] = eh[j]

    es = {('A', 'U'): {('A', 'U'): -0.9, ('C', 'G'): -1.8, ('G', 'C'): -2.3, ('U', 'A'): -1.1, ('G', 'U'): -1.1, ('U', 'G'): -0.8},
          ('C', 'G'): {('A', 'U'): -1.7, ('C', 'G'): -2.9, ('G', 'C'): -3.4, ('U', 'A'): -2.3, ('G', 'U'): -2.1, ('U', 'G'): -1.4},
          ('G', 'C'): {('A', 'U'): -2.1, ('C', 'G'): -2.0, ('G', 'C'): -2.9, ('U', 'A'): -1.8, ('G', 'U'): -1.9, ('U', 'G'): -1.2},
          ('U', 'A'): {('A', 'U'): -0.9, ('C', 'G'): -1.7, ('G', 'C'): -2.1, ('U', 'A'): -0.9, ('G', 'U'): -1.0, ('U', 'G'): -0.5},
          ('G', 'U'): {('A', 'U'): -0.5, ('C', 'G'): -1.2, ('G', 'C'): -1.4, ('U', 'A'): -0.8, ('G', 'U'): -0.4, ('U', 'G'): -0.2},
          ('U', 'G'): {('A', 'U'): -1.0, ('C', 'G'): -1.9, ('G', 'C'): -2.1, ('U', 'A'): -1.1, ('G', 'U'): -1.5, ('U', 'G'): -0.4}}


    rna = readFASTA(sys.argv[1])

    W, V = zuker(rna, ebiIL, ebiB, eh, es, a)

    trace = traceback(rna, W, V, ebiIL, ebiB, eh, es, a)

    if trace != []:
        getFoldings(trace, rna)

def hairpin(rna, i, j, eh):
    if complement((rna[i - 1], rna[j - 1])) and j - i - 1 > 0 and j - i - 1 <= 30:
            return eh[j - i - 1]
    return 1000

def stackPair(rna, i, j, es):
    if complement((rna[i - 1], rna[j - 1])) and complement((rna[i], rna[j - 2])):
        return es[(rna[i - 1], rna[j - 1])][(rna[i], rna[j - 2])]
    return 1000

def bulgeOrInternalLoop(rna, i, j, ih, jh, ebiB, ebiIL):
    if (complement((rna[i - 1], rna[j - 1])) and complement((rna[ih - 1], rna[jh - 1]))
        and ih - i + j - jh - 2 > 0 and ih - i + j - jh - 2 <= 30):
        return min(ebiIL[ih - i + j - jh - 2], ebiB[ih - i + j - jh - 2])
    return 1000

def zuker(rna, ebiIL, ebiB, eh, es, a):
    W = [[1000 for i in range(len(rna) + 1)] for j in range(len(rna) + 1)]
    V = [[1000 for i in range(len(rna) + 1)] for j in range(len(rna) + 1)]
    VBI = [[0 for i in range(len(rna) + 1)] for j in range(len(rna) + 1)]
    VM = [[0 for i in range(len(rna) + 1)] for j in range(len(rna) + 1)]
    for l in range(2, len(rna) + 1):
        for i in range(len(rna) - l + 1, 0, -1):
            j = i + l - 1

            sK = 1000
            for ih in range(i + 1, j):
                for jh in range(ih + 1, j):
                    if ih - i + j - jh > 2:
                        sK = min(sK, bulgeOrInternalLoop(rna, i, j, ih, jh, ebiB, ebiIL) + V[ih][jh])
            VBI[i][j] = sK

            sK = 1000
            for k in range(i + 1, j - 1):
                sK = min(sK, W[i + 1][k] + W[k + 1][j - 1])
            VM[i][j] = sK + a

            V[i][j] = min(hairpin(rna, i, j, eh), stackPair(rna, i, j, es) + V[i + 1][j - 1], VBI[i][j], VM[i][j])

            sK = 1000
            for k in range(i + 1, j):
                sK = min(sK, W[i][k] + W[k + 1][j])
            W[i][j] = min(W[i + 1][j], W[i][j - 1], V[i][j], sK)

    return W, V

def traceback(rna, W, V, ebiIL, ebiB, eh, es, a):
    trace = []
    stack = []
    stack.append((1, len(rna), 0))
    while stack != []:
        i, j, mat = stack.pop()
        if i >= j:
            continue
        if mat == 0:
            if W[i][j] == W[i + 1][j]:
                stack.append((i + 1, j, 0))
            elif W[i][j] == W[i][j - 1]:
                stack.append((i, j - 1, 0))
            elif W[i][j] == V[i][j]:
                stack.append((i, j, 1))
            else:
                for k in range(i + 1, j):
                    if W[i][j] == W[i][k] + W[k + 1][j]:
                        stack.append((i, k, 0))
                        stack.append((k + 1, j, 0))
                        break
        elif mat == 1:
            if V[i][j] == hairpin(rna, i, j, eh):
                trace.append((i, j))
            elif V[i][j] == V[i + 1][j - 1] + stackPair(rna, i, j, es):
                trace.append((i, j))
                trace.append((i + 1, j - 1))
                stack.append((i + 1, j - 1, 1))
            else:
                isFindBorIL = False
                for ih in range(i + 1, j):
                    for jh in range(ih + 1, j):
                        if ih - i + j - jh > 2:
                            if V[i][j] == bulgeOrInternalLoop(rna, i, j, ih, jh, ebiB, ebiIL) + V[ih][jh]:
                                trace.append((i, j))
                                trace.append((ih, jh))
                                stack.append((ih, jh, 1))
                                isFindBorIL = True
                                break
                    if isFindBorIL:
                        break
                    else:
                        for k in range(i + 1, j - 1):
                            if V[i][j] == W[i + 1][k] + W[k + 1][j - 1] + a:
                                stack.append((i + 1, k, 0))
                                stack.append((k + 1, j - 1, 0))
                                break
    #print trace
    return trace

def getFoldings(trace, rna):
    from collections import OrderedDict
    if len(trace) != 0:
        trace = list(OrderedDict.fromkeys(trace))
        folds = []
        iS, jS = trace[0]
        iE, jE = trace[0]
        for i in range(1, len(trace)):
            if not (trace[i][0] - 1 == trace[i - 1][0] and trace[i][1] + 1 == trace[i-1][1]):
                folds.append((iS - 1, iE - 1, jS - 1, jE - 1))
                iS, jS = trace[i]
            iE, jE = trace[i]
        folds.append([iS - 1, iE - 1, jS - 1, jE - 1])
        for fold in folds:
            print str(fold[0]) + "," + rna[fold[0]:fold[1] + 1] + "-" + str(fold[3]) + "," + rna[fold[3]:fold[2] + 1]

main()