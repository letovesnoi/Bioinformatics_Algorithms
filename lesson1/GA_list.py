__author__ = 'lenk'

def GA(v, w, maxDist):
    if len(w) - 1 + maxDist < len(v) - 1:
        return -1
    s = []
    s.append([0])
    for j in range(1, len(w)):
        s.append([])
    for j in range(1, min(maxDist + 1, len(w))):
        s[j].append(s[j - 1][0] - 1)
    for i in range(1, min(maxDist + 1, len(v))):
        s[0].append(s[0][-1] - 1)
    for j in range(1, len(w)):
        sdv = 0
        if j - maxDist > 0:
            sdv = 1
        for i in range(max(1, j - maxDist), min(len(v), j + maxDist + 1)):
            if i != j + maxDist and i != j - maxDist:
                s[j].append(max(s[j][-1] - 1, s[j - 1][sdv + len(s[j])] - 1))
                if v[i] == w[j]:
                    s[j][-1] = max(s[j][-1], s[j - 1][sdv + len(s[j]) - 1 - 1])
                else:
                    s[j][-1] = max(s[j][-1], s[j - 1][sdv + len(s[j]) - 1 - 1] - 1)
            elif i == j + maxDist:
                if v[i] == w[j]:
                    s[j].append(max(s[j][-1] - 1, s[j - 1][-1]))
                elif v[i] != w[j]:
                    s[j].append(max(s[j][-1] - 1, s[j - 1][-1] - 1))
            elif i == j - maxDist:
                if v[i] == w[j]:
                    s[j].append(max(s[j - 1][1] - 1, s[j - 1][0]))
                elif v[i] != w[j]:
                    s[j].append(max(s[j - 1][1] - 1, s[j - 1][0] - 1))
    return s

def OUTPUTLCS(v, w, s, maxDist):
    str1 = ''
    str2 = ''
    j = len(s) - 1
    i = len(s[j]) - 1
    while not (i == 0 and j == 0):
        sds = 0
        sdv = j - maxDist
        if j - maxDist > 0:
            sds = 1
        else:
            sdv = 0
        if s[j][i] == s[j - 1][i + sds] - 1:
                str1 += '-'
                str2 += w[j]
                j -= 1
                i += sds
        elif s[j][i] == s[j][i - 1] - 1:
                str1 += v[i + sdv]
                str2 += '-'
                i -= 1
        elif (s[j][i] == s[j - 1][i - 1 + sds] - 1 and v[i + sdv] != w[j]) or \
                    (s[j][i] == s[j - 1][i - 1 + sds] and v[i + sdv] == w[j]):
                str1 += v[i + sdv]
                str2 += w[j]
                i -= 1
                j -= 1
                i += sds
        print (i, j)

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
            v += fin.readline()[:-1]
        v = v[:-5]
        w = '9'
        while fin:
            temp = fin.readline()[:-1]
            w += temp
            if temp == '':
                break
    seq['v'] = v
    seq['w'] = w
    return seq

def main():
    maxDist = 404

    seq = readFASTA('inputGA.fasta')

    v = seq['v']
    w = seq['w']
    if len(v) < len(w):
        temp = v
        v = w
        w = temp

    s = GA(v, w, maxDist)
    if s != -1:
        score = -s[-1][-1]
    else:
        score = -1

    if score == -1 or score > maxDist:
        score = -1
        print(score)
        with open('outputGA.txt', 'w') as fout:
            fout.write(str(score) + '\r\n')
    else:
        print score
        alignment = OUTPUTLCS(v, w, s, maxDist)
        with open('outputGA.txt', 'w') as fout:
            fout.write(str(score) + '\r\n')
            fout.write(alignment['str1'] + '\r\n')
            fout.write(alignment['str2'])

main()