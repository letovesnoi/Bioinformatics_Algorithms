__author__ = 'lenk'

import sys

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

def reverseComplement(s):
    n = len(s)
    i = n - 1
    rcs = ''
    while i != -1:
        if s[i] == 'A':
            rcs += 'T'
        if s[i] == 'C':
            rcs += 'G'
        if s[i] == 'G':
            rcs += 'C'
        if s[i] == 'T':
            rcs += 'A'
        i -= 1
    return rcs

def getInt(si):
    intsi= 0
    if si == 'A':
        intsi = 0
    elif si == 'C':
        intsi = 1
    elif si == 'G':
        intsi = 2
    elif si == 'T':
        intsi = 3
    return intsi

def beforeCount(subs, p, m):
    before = 0
    for i in range(len(subs)):
        before = (before * p + getInt(subs[i])) % m
    return before

def getPower(p, m, N):
    power = []
    power.append(1)
    for i in range(1, N):
        power.append((power[-1] * p) % m)
    return power

def getKey(before, p, power, m, n, sB, sE):
    key = ((before - power[n - 1] * getInt(sB)) * p + getInt(sE)) % m
    return key

def findPattern(DNA, rcDNA, n, p, m, power):
    ans = {}
    hash = {}
    before = beforeCount(DNA[:n], p, m)
    if before not in hash:
        hash[before] = []
    hash[before].append(0)
    for i in range(1, len(DNA) - n + 1):
        key = getKey(before, p, power, m, n, DNA[i - 1], DNA[i - 1 + n])
        before = key
        if key not in hash:
            hash[key] = []
        hash[key].append(i)

    before = beforeCount(rcDNA[:n], p, m)
    if before not in hash:
        hash[before] = []
    hash[before].append(0)
    for i in range(1, len(rcDNA) - n + 1):
        key = getKey(before, p, power, m, n, rcDNA[i - 1], rcDNA[i - 1 + n])
        before = key
        ircDNA = len(DNA) - i - n
        if key in hash:
            for iDNA in hash[key]:
                if DNA[iDNA:iDNA + n] == rcDNA[i:i + n]:
                    if ircDNA + n <= iDNA or ircDNA >= iDNA + n:
                        ans['iDNA'] = iDNA
                        ans['bool'] = True
                        return ans
    ans['bool'] = False
    return ans

def main():
    p = 10
    m = 10000007
    DNA = readFASTA(sys.argv[1])
    rcDNA = reverseComplement(DNA)
    #print DNA, rcDNA

    power = getPower(p, m, len(DNA))

    first = 0
    last = len(DNA)
    temp = ''
    while first < last:
        middle = first + (last - first) / 2
        find = findPattern(DNA, rcDNA, middle, p, m, power)
        if find['bool'] == True:
            first = middle + 1
            temp = DNA[find['iDNA']:find['iDNA'] + middle]
        else:
            last = middle
    print temp

main()
