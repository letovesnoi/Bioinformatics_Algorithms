__author__ = 'lenk'

import sys

import random

def readFASTA(fileName):
    seq = ''
    with open(fileName, 'r') as fin:
        fin.readline()[:-1]
        while True:
            temp = fin.readline()[:-1]
            seq += temp
            if temp == '':
                break
    return seq

def readSubs(fileName):
    ans = {}
    subs = []
    with open(fileName, 'r') as fin:
        k = int(fin.readline())
        for line in fin:
            subs.append(line[:-1])
    ans['subs'] = subs
    ans['k'] = k
    return ans

def getInt(si):
    intsi = si
    symbols = {'a': 0, 'c': 1, 'g': 2, 't': 3}
    if si in symbols:
        intsi = symbols[si]
    return intsi

def beforeCount(sub, d, m):
    xBefore = 0
    for i in range(len(sub)):
        xBefore = (xBefore * d + getInt(sub[i])) % m
    return xBefore

def getPower(d, m, k):
    power = []
    power.append(1)
    for i in range(1, k):
        power.append((power[-1] * d) % m)
    return power

def getX(before, d, power, m, k, sB, sE):
    x = ((before - power[k - 1] * getInt(sB)) * d + getInt(sE)) % m
    return x

def addInBloom(x, m, p, a, b, bloom):
    for i in range(len(a)):
        bloom[((a[i] * x + b[i]) % p) % m] = 1
    return bloom

def getBloom(DNA, k, d, m, power, p, a, b):
    bloom = []
    for i in range(m):
        bloom.append(0)
    xBefore = beforeCount(DNA[:k], d, m)
    bloom = addInBloom(xBefore, m, p, a, b, bloom)
    for i in range(1, len(DNA) - k + 1):
        x = getX(xBefore, d, power, m, k, DNA[i - 1], DNA[i - 1 + k])
        xBefore = x
        bloom = addInBloom(x, m, p, a, b, bloom)
    return bloom

def getoccurrence(x, m, bloom, a, b, p):
    for i in range(len(a)):
        if bloom[((a[i] * x + b[i]) % p) % m] != 1:
            return 0
    return 1

def intToSeq(i, k):
    symbols = {0: 'a', 1: 'c', 2: 'g', 3: 't'}
    seq = ''
    while i / 4 != 0:
        seq += (str(i % 4))
        i = i / 4
    seq += (str(i % 4))
    intSeq = ''
    for i in range(k - len(seq)):
        intSeq += symbols[0]
    for i in range(len(seq)):
        intSeq += symbols[int(seq[len(seq) - 1 - i])]
    return intSeq

def getFP(DNA, k, d, m, bloom, a, b, p):
    FP = 0.0
    TN = 0.0
    for i in range(4 ** k):
        sub = intToSeq(i, k)
        x = beforeCount(sub, d, m)
        if getoccurrence(x, m, bloom, a, b, p) == 1 and (sub not in DNA):
            FP += 1
        if getoccurrence(x, m, bloom, a, b, p) == 0 and (sub not in DNA):
            TN += 1
    FP = FP / (FP + TN) * 100
    return FP

def main():
    DNA = readFASTA(sys.argv[1])
    temp = readSubs(sys.argv[2])
    k = temp['k']
    subs = temp['subs']

    d = 10
    p = 883
    m = 16
    countH = 3
    a = []
    b = []
    for i in range(countH):
        a.append(random.randint(1, p - 1))
        b.append(random.randint(0, p - 1))

    power = getPower(d, m, k)
    bloom = getBloom(DNA, k, d, m, power, p, a, b)

    with open('outputBF.txt', 'w') as fout:
        for sub in subs:
            x = beforeCount(sub, d, m)
            fout.write(str(getoccurrence(x, m, bloom, a, b, p)) + '\r\n')
        fout.write(str(getFP(DNA, k, d, m, bloom, a, b, p)) + ' %')

main()