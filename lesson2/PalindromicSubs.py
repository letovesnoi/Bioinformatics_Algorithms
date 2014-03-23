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

def readIntervals(fileName):
    intervals = []
    with open(fileName, 'r') as fin:
        n = int(fin.readline())
        for i in range(n):
            temp = fin.readline().split(' ')
            temp[1] = temp[-1][:-1]
            intervals.append(temp)
    return intervals

def getSymmetric(s):
    sS = []
    if s == '':
        sS.extend(['|', '|'])
        return sS
    for i in range(0, len(s) * 2, 2):
      sS.append('|')
      sS.append(s[i / 2])
    sS.append('|')
    return sS

def getP(s):
    if s == '':
        return 0
    sS = getSymmetric(s)
    maxLP = []
    c = 0
    r = 0
    right = 0
    maxLP.append(0)
    for i in range(1, len(sS)):
        if i > r:
            maxLP.append(0)
            left = i - 1
            right = i + 1
        else:
            i2 = c * 2 - i
            if maxLP[i2] < r - i:
                maxLP.append(maxLP[i2])
                left = -1
            else:
                maxLP.append(r - i)
                right = r + 1
                left = i * 2 - right
        while left >= 0 and right < len(sS) and sS[left] == sS[right]:
            maxLP[i] += 1
            left -= 1
            right += 1
        if i + maxLP[i] > r:
            c = i
            r = i + maxLP[i]
    return maxLP

def getCountPS(interval, maxLP):
    left = int(interval[0]) * 2 + 1 - 1
    right = int(interval[1]) * 2 + 1 + 1
    countPS = 0
    for current in range(left + 1, right, 1):
        countPS += min((right - current) / 2 + current % 2, (current - left) / 2 + current % 2,
                       maxLP[current] / 2 + current % 2)
    return countPS

def main():
    s = readFASTA(sys.argv[1])
    maxLP = getP(s)
    #print maxLP
    intervals = readIntervals(sys.argv[2])
    #print intervals
    countsPS = []
    for interval in intervals:
        countsPS.append(getCountPS(interval, maxLP))
    for countPS in countsPS:
        print countPS

main()