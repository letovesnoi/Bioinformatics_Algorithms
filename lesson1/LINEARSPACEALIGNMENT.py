__author__ = 'lenk'

edge = []
maxDist = 5

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

def LINEARSPACEALIGNMENT(v, w, top, bottom, left, right):
    global edge
    if top == bottom:
        temp = top
        temp1 = left
        for i in range(abs(right - left)):
            edge.append((temp, temp1))
            temp1 += 1
        if top == len(v) - 1:
            edge.append((len(v) - 1, len(w) - 1))
        return

    ans = middleEdge(v, w, top, bottom, left, right)
    ansB = ans['begin']
    iB = ansB['middle']
    jB = ansB['maxj']

    ansE = ans['end']
    iE = ansE['middle']
    jE = ansE['maxj']

    LINEARSPACEALIGNMENT(v, w, top, iB, left, jB)
    edge.append((iB, jB))

    newiB = iB
    newjB = jB

    if (jB == jE and iB + 1 == iE) or (jB + 1 == jE and iB + 1 == iE):
        newiB += 1
    if (jB + 1 == jE and iB == iE) or (jB + 1 == jE and iB + 1 == iE):
        newjB += 1
    iB = newiB
    jB = newjB

    LINEARSPACEALIGNMENT(v, w, iB, bottom, jB, right)

def middleEdge(v, w, top, bottom, left, right):
    ans = {}
    ansB = {}

    middle = (top + bottom) / 2

    fromSource = FromSource(v, w, middle, top, bottom, left, right, 0)

    fromSource1 = fromSource['middle']
    fromSource2 = fromSource['middle+1']

    sdv = len(w) - len(v) - maxDist
    toSink = ToSink(v, w, middle, top, bottom, left, right, 0)

    toSink1 = toSink['middle']
    toSink2 = toSink['middle+1']

    maxj1 = maxLength(fromSource1, toSink1)
    maxj2 = maxLength(fromSource2, toSink2)

    ansB['fromSource'] = fromSource1
    ansB['toSink'] = toSink1
    ansB['maxj'] = maxj1
    ansB['middle'] = middle

    ansE = {}
    maxjTemp = ansB['maxj'] + 1
    middle2 = middle + 1

    while maxj2 != ansB['maxj'] + 1 and maxj2 != ansB['maxj']:
        del fromSource2[maxj2]
        del toSink2[maxj2]
        maxj2 = maxLength(fromSource2, toSink2)
    if maxjTemp in ansB['fromSource']:
        if ansB['fromSource'][maxjTemp] + ansB['toSink'][maxjTemp] > fromSource2[maxj2] + toSink2[maxj2]:
            maxj2 = maxjTemp
            middle2 = ansB['middle']

    ansE['fromSource'] = fromSource2
    ansE['toSink'] = toSink2
    ansE['maxj'] = maxj2
    ansE['middle'] = middle2

    ans['begin'] = ansB
    ans['end'] = ansE

    return ans

def FromSource(v, w, middle, top, bottom, left, right, sdv):
    global maxDist
    ans = {}
    ans1 = {}
    ans2 = {}
    s = {}

    s[top, left] = 0
    for i in range(max(top + 1, left - maxDist), min(middle + 2, left + maxDist + 1), 1):
        s[i, left] = s[i - 1, left] - 1
    for j in range(max(left + 1, top - maxDist), min(right + 1, top + maxDist + 1), 1):
        s[top, j] = s[top, j - 1] - 1
    for i in range(top + 1, middle + 2, 1):
        for j in range(max(left + 1, i - maxDist), min(right + 1, i + maxDist + 1), 1):
            if v[i] == w[j]:
                if j != i - maxDist and j != i + maxDist:
                    s[i, j] = max(s[i - 1, j] - 1, s[i, j - 1] - 1, s[i - 1, j - 1])
                elif j == i - maxDist:
                    s[i, j] = max(s[i - 1, j] - 1, s[i - 1, j - 1])
                elif j == i + maxDist:
                    s[i, j] = max(s[i, j - 1] - 1, s[i - 1, j - 1])
            elif v[i] != w[j]:
                if j != i - maxDist and j != i + maxDist:
                    s[i, j] = max(s[i - 1, j] - 1, s[i, j - 1] - 1, s[i - 1, j - 1] - 1)
                elif j == i - maxDist:
                    s[i, j] = max(s[i - 1, j] - 1, s[i - 1, j - 1] - 1)
                elif j == i + maxDist:
                    s[i, j] = max(s[i, j - 1] - 1, s[i - 1, j - 1] - 1)

        if i != middle + 1:
            for j in range(max(left + 1, i - 1 - maxDist), min(right + 1, i - 1 + maxDist + 1), 1):
                del s[i - 1, j]

    for pair in s:
        if pair[0] == middle:
            ans1[pair[1]] = s[pair[0], pair[1]]
        if pair[0] == middle + 1:
            ans2[pair[1]] = s[pair[0], pair[1]]

    ans['middle'] = ans1
    ans['middle+1'] = ans2
    return ans

def ToSink(v, w, middle, top, bottom, left, right, sdv):
    ans = {}
    newV = ''
    newW = ''
    for i in range(len(v)):
        newV += v[-i]
    for i in range(len(w)):
        newW += w[-i]
    right1 = len(w) - 1 - left
    left1 = right1 - right + left
    bottom1 = len(v) - 1 - top
    top1 = bottom1 - bottom + top
    middle1 = (top1 + bottom1) / 2
    if (top + bottom) % 2 == 0:
        middle1 -= 1
    temp = FromSource(newV, newW, middle1, top1, bottom1, left1, right1, sdv)
    ans1 = temp['middle']
    ans2 = temp['middle+1']
    newAns1 = {}
    newAns2 = {}
    for i in ans1:
        newAns1[len(w) - i - 1] = ans1[i]
    for i in ans2:
        newAns2[len(w) - i - 1] = ans2[i]
    ans['middle'] = newAns2
    ans['middle+1'] = newAns1
    return ans

def maxLength(fromSource, toSink):
    length = {}
    max = fromSource[fromSource.keys()[0]] + toSink[toSink.keys()[0]]
    maxj = fromSource.keys()[0]
    for j in fromSource:
        length[j] = fromSource[j] + toSink[j]
        if length[j] > max:
            max = length[j]
            maxj = j
    return maxj

def OUTPUTLCS(v, w, edge):
    global str1
    global str2
    global maxScore
    str1 = ''
    str2 = ''
    maxScore = 0
    for i in range(len(edge) - 1):
        if edge[i][1] + 1 == edge[i + 1][1] and edge[i][0] == edge[i + 1][0]:
            str1 += w[edge[i + 1][1]]
            str2 += '-'
            maxScore -= 1
        if edge[i][1] + 1 == edge[i + 1][1] and edge[i][0] + 1 == edge[i + 1][0]:
            str1 += w[edge[i + 1][1]]
            str2 += v[edge[i][0] + 1]
            if w[edge[i + 1][1]] != v[edge[i][0] + 1]:
                maxScore -= 1
        if edge[i][1] == edge[i + 1][1] and edge[i][0] + 1 == edge[i + 1][0]:
            str1 += '-'
            str2 += v[edge[i + 1][0]]
            maxScore -= 1

def main():
    global edge
    global str1
    global str2
    global maxScore
    global maxDist
    seq = readFASTA('test.fasta')
    v = seq['v']
    w = seq['w']
    LINEARSPACEALIGNMENT(v, w, 0, len(v) - 1, 0, len(w) - 1)
    OUTPUTLCS(v, w, edge)
    if -maxScore > maxDist:
        print(str(-1))
        with open('outputLSA.txt', 'w') as fout:
            fout.write(str(-1))
        return 0
    print(-maxScore)
    with open('outputLSA.txt', 'w') as fout:
        fout.write(str(-maxScore) + '\r\n')
        fout.write(str1 + '\r\n' + str2)
    #print edge

main()