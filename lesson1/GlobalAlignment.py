__author__ = 'lenk'

def GA(v, w, maxDist):
    if len(w) - 1 + maxDist <= len(v) - 1:
        return -1
    s = {}
    s[0, 0] = 0
    for i in range(1, min(maxDist + 1, len(v))):
        s[i, 0] = s[i - 1, 0] - 1
    for j in range(1, min(maxDist + 1, len(w))):
        s[0, j] = s[0, j - 1] - 1
    for j in range(1, len(w)):
        for i in range(max(1, j - maxDist), min(len(v), j + maxDist + 1)):
            if i != j + maxDist and i != j - maxDist:
                s[i, j] = max(s[i - 1, j] - 1, s[i, j - 1] - 1)
                if v[i] == w[j]:
                    s[i, j] = max(s[i, j], s[i - 1, j - 1])
                else:
                    s[i, j] = max(s[i, j], s[i - 1, j - 1] - 1)
            elif i == j + maxDist:
                if v[i] == w[j]:
                    s[i, j] = max(s[i - 1, j] - 1, s[i - 1, j - 1])
                else:
                    s[i, j] = max(s[i - 1, j] - 1, s[i - 1, j - 1] - 1)
            elif i == j - maxDist:
                if v[i] == w[j]:
                    s[i, j] = max(s[i, j - 1] - 1, s[i - 1, j - 1])
                else:
                    s[i, j] = max(s[i, j - 1] - 1, s[i - 1, j - 1] - 1)
    return s

def OUTPUTLCS(v, w, i, j, s):
    str1 = ''
    str2 = ''
    while not (i == 0 and j == 0):
        if (i, j - 1) in s:
            if s[i, j] == s[i, j - 1] - 1:
                str1 += '-'
                str2 += w[j]
                j -= 1
                continue
        if (i - 1, j) in s:
            if s[i, j] == s[i - 1, j] - 1:
                str1 += v[i]
                str2 += '-'
                i -= 1
                continue
        if (i - 1, j - 1) in s:
            if (s[i, j] == s[i - 1, j - 1] - 1 and v[i] != w[j]) or \
                    (s[i, j] == s[i - 1, j - 1] and v[i] == w[j]):
                str1 += v[i]
                str2 += w[j]
                i -= 1
                j -= 1

    alignment1 = ''
    for i in range(len(str1) - 1, -1, -1):
        alignment1 += str1[i]
    alignment2 = ''
    for i in range(len(str2) - 1, -1, -1):
        alignment2 += str2[i]

    alignment = {}
    alignment['str1'] = alignment1
    alignment['str2'] = alignment2

    return alignment

def readFASTA(fileName):
    seq = {}
    with open(fileName, 'r') as fin:
        fin.readline()
        v = '0'
        while v[-5:] != '>seq2':
            v += fin.readline()[:-2]
        v = v[:-5]
        w = '9'
        while fin:
            temp = fin.readline()[:-2]
            w += temp
            if temp == '':
                break
    seq['v'] = v
    seq['w'] = w
    return seq

def main():
    maxDist = 500

    seq = readFASTA('inputGA.txt')

    v = seq['v']
    w = seq['w']
    if len(v) < len(w):
        temp = v
        v = w
        w = temp

    s = GA(v, w, maxDist)
    score = -s[len(v) - 1, len(w) - 1]

    if score == -1 or score > maxDist:
        score = -1
        print(score)
        with open('outputGA.txt', 'w') as fout:
            fout.write(str(score) + '\r\n')
    else:
        print score
        alignment = OUTPUTLCS(v, w, len(v) - 1, len(w) - 1, s)
        with open('outputGA.txt', 'w') as fout:
            fout.write(str(score) + '\r\n')
            fout.write(alignment['str1'] + '\r\n')
            fout.write(alignment['str2'])

main()