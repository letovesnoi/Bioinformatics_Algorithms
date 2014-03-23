__author__ = 'lenk'

import sys

def readFASTA(fileName):
    seq = []
    with open(fileName, 'r') as fin:
        temp = fin.readline()
        while temp != '':
            temp = fin.readline()[:-1]
            seq.append('')
            while '>' not in temp:
                seq[-1] += temp
                if temp == '':
                    break
                temp = fin.readline()[:-1]
    return seq

def getScore(v, w):
    s = {}
    s[0, 0] = 0
    for i in range(1, len(v)):
        s[i, 0] = s[i - 1, 0] + 1
    for j in range(1, len(w)):
        s[0, j] = s[0, j - 1] + 1
    for j in range(1, len(w)):
        for i in range(1, len(v)):
                s[i, j] = min(s[i - 1, j] + 1, s[i, j - 1] + 1)
                if v[i] == w[j]:
                    s[i, j] = min(s[i, j], s[i - 1, j - 1])
                else:
                    s[i, j] = min(s[i, j], s[i - 1, j - 1] + 1)
    return s[len(v) - 1, len(w) - 1]

def constructEDM(seq):
    EDM = {}
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            EDM[seq[i], seq[j]] = getScore('i' + seq[i], 'j' + seq[j])
    return EDM

def getMin(EDM):
    min = {}
    min['value'] = EDM[EDM.keys()[0]]
    min['key'] = EDM.keys()[0]
    for pair in EDM:
        if min['value'] > EDM[pair]:
            min['value'] = EDM[pair]
            min['key'] = pair
    return min

def getPAGT(EDM, set):
    while len(EDM) != 1:
        temp = updateEDM(EDM, set)
        EDM = temp['EDM']
        set = temp['set']
    PAGT = '(' + str(EDM.keys()[0][0]) + ':' + str(EDM[EDM.keys()[0]]) + ':' + str(EDM.keys()[0][1]) + ')'
    return PAGT

def updateEDM(EDM, set):
    ans = {}
    newEDM = {}
    min = getMin(EDM)
    newKey = '(' + min['key'][0] + ':' + str(min['value']) + ':' + min['key'][1] + ')'

    set.remove(min['key'][0])
    set.remove(min['key'][1])

    for i in range(len(set)):
        for j in range(i + 1, len(set)):
            if (set[i], set[j]) in EDM:
                newEDM[set[i], set[j]] = EDM[set[i], set[j]]
            else:
                newEDM[set[i], set[j]] = EDM[set[j], set[i]]

    for s in set:
        if (min['key'][0], s) in EDM:
            newEDM[newKey, s] = EDM[min['key'][0], s]
        else:
            newEDM[newKey, s] = EDM[s, min['key'][0]]
        if (min['key'][1], s) in EDM:
            newEDM[newKey, s] += EDM[min['key'][1], s]
        else:
            newEDM[newKey, s] += EDM[s, min['key'][1]]
        newEDM[newKey, s] /= 2
    set.append(newKey)

    ans['EDM'] = newEDM
    ans['set'] = set

    return ans

def main():
    seq = readFASTA(sys.argv[1])
    EDM = constructEDM(seq)
    PAGT = getPAGT(EDM, seq)

    with open('outputPAGT.txt', 'w') as fout:
        fout.write(PAGT)
    print PAGT

main()