__author__ = 'lenk'

import sys

def readFASTA(fileName):
    rna = ''
    with open(fileName, 'r') as fin:
        fin.readline()
        for line in fin:
            rna += line[:-1]
    return rna

def complement(basePair):
    if 'A' in basePair and 'U' in basePair:
        return True
    if 'C' in basePair and 'G' in basePair:
        return True
    #elif 'G' in basePair and 'U' in basePair:
    #    return True
    return False

def getCost(rna, i, j):
    cost = 0
    if complement((rna[i], rna[j])) and j - i >= 5:
        cost = 1
        if complement((rna[i + 1], rna[j - 1])):
            #if i - 1 >= 0 and j + 1 < len(rna):
            #    if complement((rna[i - 1], rna[j + 1])):
            cost += 0.1
    return cost

def getS(rna):
    s = {}
    #flag = False
    for i in range(1, len(rna)):
        s[i, i - 1] = 0
    for i in range(0, len(rna)):
        s[i, i] = 0
    for l in range(1, len(rna)):
        for i in range(len(rna) - l):
            j = i + l
            #basePair = [rna[i], rna[j]]
            cost = getCost(rna, i, j)
            sK = 0
            for k in range(i + 1, j):
                if s[i, k] + s[k + 1, j] > sK:
                    sK = s[i, k] + s[k + 1, j]
            s[i, j] = max(s[i + 1, j - 1] + cost, s[i + 1, j], s[i, j - 1], sK)
            '''if s[i, j] == s[i + 1, j - 1] + cost and complement(basePair) and not flag:
                flag = True
            elif s[i, j] == s[i + 1, j - 1] + cost and complement(basePair) and flag:
                s[i, j] += 0.01
            else:
                flag = False'''

    return s

flag = False
interval = []
trace = []

def getStringPairs(rna, pi, pj):
    global interval
    global flag
    interval.append((pi, pj))
    s = str(interval[0][0]) + ',' + rna[interval[0][0]:interval[1][0] + 1] + '-' \
        + str(interval[1][1]) + ',' + rna[interval[1][1]:interval[0][1] + 1]
    flag = False
    interval = []
    return s

def traceback(s, rna, i, j, pi, pj):
    global flag
    global interval
    global trace
    trace.append((i, j))
    cost = getCost(rna, i, j)
    if j <= i:
        if flag:
            print getStringPairs(rna, pi, pj)
        return
    if s[i, j] > s[i + 1, j - 1] and cost >= 1:
        #print(rna[i], rna[j])
        if not flag:
            interval.append((i, j))
            flag = True
        traceback(s, rna, i + 1, j - 1, i, j)
        return
    elif s[i, j] == s[i + 1, j - 1] and cost == 0:
        if flag:
            print getStringPairs(rna, pi, pj)
        traceback(s, rna, i + 1, j - 1, i, j)
        return
    elif s[i, j] == s[i, j - 1]:
        if flag:
            print getStringPairs(rna, pi, pj)
        traceback(s, rna, i, j - 1, i, j)
        return
    elif s[i, j] == s[i + 1, j]:
        if flag:
            print getStringPairs(rna, pi, pj)
        traceback(s, rna, i + 1, j, i, j)
        return
    else:
        if flag:
            print getStringPairs(rna, pi, pj)
        for k in range(i + 1, j):
            if s[i, j] == s[i, k] + s[k + 1, j]:
                traceback(s, rna, i, k, i, j)
                traceback(s, rna, k + 1, j, i, j)
                return

def main():
    global trace
    rna = readFASTA(sys.argv[1])
    s = getS(rna)
    for i in range(len(rna)):
        for j in range(len(rna)):
            if (i, j) not in s:
                s[i, j] = 0
    '''with open('s.txt', 'w') as fout:
        for i in range(len(rna)):
            for j in range(len(rna)):
                fout.write(str(s[i, j]) + ' ')
            fout.write('\r\n')'''
    traceback(s, rna, 0, len(rna) - 1, 0, len(rna) - 1)
    #print trace

main()