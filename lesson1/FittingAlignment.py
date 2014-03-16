__author__ = 'lenk'

import sys

def GA(v, w):
    s = []
    for i in range(len(v)):
        s.append([])
        for j in range(len(w)):
            s[i].append(0)
    for i in range(1, len(v)):
        s[i][0] = s[i - 1][0]
    for j in range(1, len(w)):
        s[0][j] = s[0][j - 1] - 1
    for i in range(1, len(v)):
        for j in range(1, len(w)):
            s[i][j] = max(s[i - 1][j] - 1, s[i][j - 1] - 1, s[i - 1][j - 1] - int(v[i] != w[j]))
    maxS = s[0][len(w) - 1]
    maxi = 0
    for i in range(1, len(v)):
        if s[i][len(w) - 1] > maxS:
            maxS = s[i][len(w) - 1]
            maxi = i
    ans = {}
    ans['s'] = s
    ans['score'] = s[maxi][len(w) - 1]
    ans['index'] = maxi
    return ans

def OUTPUTLCS(v, w, i, j, s):
    global back
    str1 = ''
    str2 = ''
    while j != 0:
        if s[i][j] == s[i][j - 1] - 1:
            str1 += '-'
            str2 += w[j]
            j -= 1
        elif s[i][j] == s[i - 1][j] - 1:
            str1 += v[i]
            str2 += '-'
            i -= 1
        elif s[i][j] == s[i - 1][j - 1] or s[i][j] == s[i - 1][j - 1] - 1:
            str1 += v[i]
            str2 += w[j]
            i -= 1
            j -= 1

    newStr1 = ''
    newStr2 = ''
    for i in range(len(str1)):
        newStr1 += str1[len(str1) - i - 1]
        newStr2 += str2[len(str2) - i - 1]
    ans = {}
    ans['str1'] = newStr1
    ans['str2'] = newStr2
    return ans

def readFASTA(fileName):
    countSeq = 2
    seq = {}
    with open(fileName, 'r') as fin:
        fin.readline()
        for i in range(countSeq):
            seq[str(i)] = str(i)
            temp = fin.readline()[:-1]
            while '>' not in temp:
                if '>' not in temp:
                    seq[str(i)] += temp
                if temp == '':
                    break
                temp = fin.readline()[:-1]
    return seq


def main():
    sequences = readFASTA(sys.argv[1])
    v = sequences['0']
    w = sequences['1']

    g = GA(v, w)
    s = g['s']
    score = g['score']
    ind = g['index']

    outstr = OUTPUTLCS(v, w, ind, len(w) - 1, s)

    str1 = outstr['str1']
    str2 = outstr['str2']

    with open('outputFA.txt', 'w') as fout:
        fout.write(str(score) + '\r\n' + str1 + '\r\n' + str2)

main()
