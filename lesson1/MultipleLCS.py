__author__ = 'lenk'

import sys

back = {}

def listsInit(seq0, seq1, seq2, seq3, SM, GP):
    s = []
    for i in range(len(seq0)):
        s.append([])
        for j in range(len(seq1)):
            s[i].append([])
            for k in range(len(seq2)):
                s[i][j].append([])
                for l in range(len(seq3)):
                    s[i][j][k].append(0)

    # j, k, l = 0
    for i in range(1, len(seq0)):
        s[i][0][0][0] = s[i - 1][0][0][0] - 6 * GP

    # i, k, l = 0
    for j in range(1, len(seq1)):
        s[0][j][0][0] = s[0][j - 1][0][0] - 6 * GP

    # i, j, l = 0
    for k in range(1, len(seq2)):
        s[0][0][k][0] = s[0][0][k - 1][0] - 6 * GP

    # i, j, k = 0
    for l in range(1, len(seq3)):
        s[0][0][0][l] = s[0][0][0][l - 1] - 6 * GP

    # i, j = 0
    for k in range(1, len(seq2)):
        for l in range(1, len(seq3)):
            s[0][0][k][l] = \
                max(s[0][0][k - 1][l] - 6 * GP,
                    s[0][0][k][l - 1] - 6 * GP,

                    s[0][0][k - 1][l - 1] - 5 * GP - SM[seq2[k], seq3[l]])

    # i, k = 0
    for j in range(1, len(seq1)):
        for l in range(1, len(seq3)):
            s[0][j][0][l] = \
                max(s[0][j - 1][0][l] - 6 * GP,
                    s[0][j][0][l - 1] - 6 * GP,

                    s[0][j - 1][0][l - 1] - 5 * GP - SM[seq1[j], seq3[l]])

    # i, l = 0
    for j in range(1, len(seq1)):
        for k in range(1, len(seq2)):
            s[0][j][k][0] = \
                max(s[0][j - 1][k][0] - 6 * GP,
                    s[0][j][k - 1][0] - 6 * GP,

                    s[0][j - 1][k - 1][0] - 5 * GP - SM[seq1[j], seq2[k]])
    # j, k = 0
    for i in range(1, len(seq0)):
        for l in range(1, len(seq3)):
            s[i][0][0][l] = \
                max(s[i - 1][0][0][l] - 6 * GP,
                    s[i][0][0][l - 1] - 6 * GP,

                    s[i - 1][0][0][l - 1] - 5 * GP - SM[seq0[i], seq3[l]])

    # j, l = 0
    for i in range(1, len(seq0)):
        for k in range(1, len(seq2)):
                s[i][0][k][0] = \
                    max(s[i - 1][0][k][0] - 6 * GP,
                        s[i][0][k - 1][0] - 6 * GP,

                        s[i - 1][0][k - 1][0] - 5 * GP - SM[seq0[i], seq2[k]])

    # k, l = 0
    for i in range(1, len(seq0)):
        for j in range(1, len(seq1)):
            s[i][j][0][0] = \
                max(s[i - 1][j][0][0] - 6 * GP,
                    s[i][j - 1][0][0] - 6 * GP,

                    s[i - 1][j - 1][0][0] - 5 * GP - SM[seq0[i], seq1[j]])

    # i = 0
    for j in range(1, len(seq1)):
        for k in range(1, len(seq2)):
            for l in range(1, len(seq3)):
                s[0][j][k][l] = \
                    max(s[0][j - 1][k][l] - 6 * GP,
                        s[0][j][k - 1][l] - 6 * GP,
                        s[0][j][k][l - 1] - 6 * GP,

                        s[0][j - 1][k - 1][l] - 5 * GP - SM[seq1[j], seq2[k]],
                        s[0][j - 1][k][l - 1] - 5 * GP - SM[seq1[j], seq3[l]],
                        s[0][j][k - 1][l - 1] - 5 * GP - SM[seq2[k], seq3[l]],

                        s[0][j - 1][k - 1][l - 1] - 3 * GP - SM[seq1[j], seq2[k]] - SM[seq1[j], seq3[l]] -
                            SM[seq2[k], seq3[l]])

    # j = 0
    for i in range(1, len(seq0)):
        for k in range(1, len(seq2)):
            for l in range(1, len(seq3)):
                s[i][0][k][l] = \
                    max(s[i - 1][0][k][l] - 6 * GP,
                        s[i][0][k - 1][l] - 6 * GP,
                        s[i][0][k][l - 1] - 6 * GP,

                        s[i - 1][0][k - 1][l] - 5 * GP - SM[seq0[i], seq2[k]],
                        s[i - 1][0][k][l - 1] - 5 * GP - SM[seq0[i], seq3[l]],
                        s[i][0][k - 1][l - 1] - 5 * GP - SM[seq2[k], seq3[l]],

                        s[i - 1][0][k - 1][l - 1] - 3 * GP - SM[seq0[i], seq2[k]] - SM[seq0[i], seq3[l]] -
                            SM[seq2[k], seq3[l]])

    # k = 0
    for i in range(1, len(seq0)):
        for j in range(1, len(seq1)):
            for l in range(1, len(seq3)):
                s[i][j][0][l] = \
                    max(s[i - 1][j][0][l] - 6 * GP,
                        s[i][j - 1][0][l] - 6 * GP,
                        s[i][j][0][l - 1] - 6 * GP,

                        s[i - 1][j - 1][0][l] - 5 * GP - SM[seq0[i], seq1[j]],
                        s[i - 1][j][0][l - 1] - 5 * GP - SM[seq0[i], seq3[l]],
                        s[i][j - 1][0][l - 1] - 5 * GP - SM[seq1[j], seq3[l]],

                        s[i - 1][j - 1][0][l - 1] - 3 * GP - SM[seq0[i], seq1[j]] - SM[seq0[i], seq3[l]] -
                            SM[seq1[j], seq3[l]])

    # l = 0
    for i in range(1, len(seq0)):
        for j in range(1, len(seq1)):
            for k in range(1, len(seq2)):
                s[i][j][k][0] = \
                    max(s[i - 1][j][k][0] - 6 * GP,
                        s[i][j - 1][k][0] - 6 * GP,
                        s[i][j][k - 1][0] - 6 * GP,

                        s[i - 1][j - 1][k][0] - 5 * GP - SM[seq0[i], seq1[j]],
                        s[i - 1][j][k - 1][0] - 5 * GP - SM[seq1[j], seq2[k]],
                        s[i][j - 1][k - 1][0] - 5 * GP - SM[seq1[j], seq2[k]],

                        s[i - 1][j - 1][k - 1][0] - 3 * GP - SM[seq0[i], seq1[j]] - SM[seq0[i], seq2[k]] -
                            SM[seq1[j], seq2[k]])

    return s

def GA(seq0, seq1, seq2, seq3, SM, GP):

    s = listsInit(seq0, seq1, seq2, seq3, SM, GP)

    for i in range(1, len(seq0)):
        for j in range(1, len(seq1)):
            for k in range(1, len(seq2)):
                for l in range(1, len(seq3)):
                    s[i][j][k][l] = \
                        max(s[i - 1][j][k][l] - 6 * GP,
                            s[i][j - 1][k][l] - 6 * GP,
                            s[i][j][k - 1][l] - 6 * GP,
                            s[i][j][k][l - 1] - 6 * GP,

                            s[i - 1][j - 1][k][l] - 5 * GP - SM[seq0[i], seq1[j]],
                            s[i - 1][j][k - 1][l] - 5 * GP - SM[seq0[i], seq2[k]],
                            s[i - 1][j][k][l - 1] - 5 * GP - SM[seq0[i], seq3[l]],
                            s[i][j - 1][k - 1][l] - 5 * GP - SM[seq1[j], seq2[k]],
                            s[i][j - 1][k][l - 1] - 5 * GP - SM[seq1[j], seq3[l]],
                            s[i][j][k - 1][l - 1] - 5 * GP - SM[seq2[k], seq3[l]],

                            s[i - 1][j - 1][k - 1][l] - 3 * GP - SM[seq0[i], seq1[j]] - SM[seq0[i], seq2[k]] -
                                SM[seq1[j], seq2[k]],
                            s[i - 1][j - 1][k][l - 1] - 3 * GP - SM[seq0[i], seq1[j]] - SM[seq0[i], seq3[l]] -
                                SM[seq1[j], seq3[l]],
                            s[i - 1][j][k - 1][l - 1] - 3 * GP - SM[seq0[i], seq2[k]] - SM[seq0[i], seq3[l]] -
                                SM[seq2[k], seq3[l]],
                            s[i][j - 1][k - 1][l - 1] - 3 * GP - SM[seq1[j], seq2[k]] - SM[seq1[j], seq3[l]] -
                                SM[seq2[k], seq3[l]],

                            s[i - 1][j - 1][k - 1][l - 1] - SM[seq0[i], seq1[j]] - SM[seq0[i], seq2[k]] -
                            SM[seq0[i], seq3[l]] - SM[seq1[j], seq2[k]] - SM[seq1[j], seq3[l]] - SM[seq2[k], seq3[l]])

    return s

def getAlignment(str0, str1, str2, str3):
    alignment0 = ''
    for i in range(len(str0) - 1, -1, -1):
        alignment0 += str0[i]
    alignment1 = ''
    for i in range(len(str1) - 1, -1, -1):
        alignment1 += str1[i]
    alignment2 = ''
    for i in range(len(str2) - 1, -1, -1):
        alignment2 += str2[i]
    alignment3 = ''
    for i in range(len(str3) - 1, -1, -1):
        alignment3 += str3[i]

    alignment = {}
    alignment['str0'] = alignment0
    alignment['str1'] = alignment1
    alignment['str2'] = alignment2
    alignment['str3'] = alignment3

    return alignment

def OUTPUTLCS(seq0, seq1, seq2, seq3, i, j, k, l, s, SM, GP):
    str0 = str1 = str2 = str3 = ''
    while not (i == 0 and j == 0 and k == 0 and l == 0):
        if i >= 1:
            if s[i][j][k][l] == s[i - 1][j][k][l] - 6 * GP:
                str0 += seq0[i]
                str1 += '-'
                str2 += '-'
                str3 += '-'
                i -= 1
                continue
        if j >= 1:
            if s[i][j][k][l] == s[i][j - 1][k][l] - 6 * GP:
                str0 += '-'
                str1 += seq1[j]
                str2 += '-'
                str3 += '-'
                j -= 1
                continue
        if k >= 1:
            if s[i][j][k][l] == s[i][j][k - 1][l] - 6 * GP:
                str0 += '-'
                str1 += '-'
                str2 += seq2[k]
                str3 += '-'
                k -= 1
                continue
        if l >= 1:
            if s[i][j][k][l] == s[i][j][k][l - 1] - 6 * GP:
                str0 += '-'
                str1 += '-'
                str2 += '-'
                str3 += seq3[l]
                l -= 1
                continue

        if i >= 1 and j >= 1:
            if s[i][j][k][l] == s[i - 1][j - 1][k][l] - 5 * GP - SM[seq0[i], seq1[j]]:
                str0 += seq0[i]
                str1 += seq1[j]
                str2 += '-'
                str3 += '-'
                i -= 1
                j -= 1
                continue
        if i >= 1 and k >= 1:
            if s[i][j][k][l] == s[i - 1][j][k - 1][l] - 5 * GP - SM[seq0[i], seq2[k]]:
                str0 += seq0[i]
                str1 += '-'
                str2 += seq1[k]
                str3 += '-'
                i -= 1
                k -= 1
                continue
        if i >= 1 and l >= 1:
            if s[i][j][k][l] == s[i - 1][j][k][l - 1] - 5 * GP - SM[seq0[i], seq3[l]]:
                str0 += seq0[i]
                str1 += '-'
                str2 += '-'
                str3 += seq3[l]
                i -= 1
                l -= 1
                continue
        if j >= 1 and k >= 1:
            if s[i][j][k][l] == s[i][j - 1][k - 1][l] - 5 * GP - SM[seq1[j], seq2[k]]:
                str0 += '-'
                str1 += seq1[j]
                str2 += seq2[k]
                str3 += '-'
                j -= 1
                k -= 1
                continue
        if j >= 1 and l >= 1:
            if s[i][j][k][l] == s[i][j - 1][k][l - 1] - 5 * GP - SM[seq1[j], seq3[l]]:
                str0 += '-'
                str1 += seq1[j]
                str2 += '-'
                str3 += seq3[l]
                j -= 1
                l -= 1
                continue
        if k >= 1 and l >= 1:
            if s[i][j][k][l] == s[i][j][k - 1][l - 1] - 5 * GP - SM[seq2[k], seq3[l]]:
                str0 += '-'
                str1 += '-'
                str2 += seq2[k]
                str3 += seq3[l]
                k -= 1
                l -= 1
                continue
        if i >= 1 and j >= 1 and k >= 1:
            if s[i][j][k][l] == s[i - 1][j - 1][k - 1][l] - 3 * GP - SM[seq0[i], seq1[j]] - SM[seq0[i], seq2[k]] - \
                    SM[seq1[j], seq2[k]]:
                str0 += seq0[i]
                str1 += seq1[j]
                str2 += seq2[k]
                str3 += '-'
                i -= 1
                j -= 1
                k -= 1
                continue
        if i >= 1 and j >= 1 and l >= 1:
            if s[i][j][k][l] == s[i - 1][j - 1][k][l - 1] - 3 * GP - SM[seq0[i], seq1[j]] - SM[seq0[i], seq3[l]] - \
                    SM[seq1[j], seq3[l]]:
                str0 += seq0[i]
                str1 += seq1[j]
                str2 += '-'
                str3 += seq3[l]
                i -= 1
                j -= 1
                l -= 1
                continue
        if i >= 1 and k >= 1 and l >= 1:
            if s[i][j][k][l] == s[i - 1][j][k - 1][l - 1] - 3 * GP - SM[seq0[i], seq2[k]] - SM[seq0[i], seq3[l]] - \
                                SM[seq2[k], seq3[l]]:
                str0 += seq0[i]
                str1 += '-'
                str2 += seq2[k]
                str3 += seq3[l]
                i -= 1
                k -= 1
                l -= 1
                continue
        if j >= 1 and k >= 1 and l >= 1:
            if s[i][j][k][l] == s[i][j - 1][k - 1][l - 1] - 3 * GP - SM[seq1[j], seq2[k]] - SM[seq1[j], seq3[l]] - \
                                SM[seq2[k], seq3[l]]:
                str0 += '-'
                str1 += seq1[j]
                str2 += seq2[k]
                str3 += seq3[l]
                j -= 1
                k -= 1
                l -= 1
                continue
        if i >= 1 and j >= 1 and k >= 1 and l >= 1:
            if s[i][j][k][l] == s[i - 1][j - 1][k - 1][l - 1] - SM[seq0[i], seq1[j]] - SM[seq0[i], seq2[k]] - \
                SM[seq0[i], seq3[l]] - SM[seq1[j], seq2[k]] - SM[seq1[j], seq3[l]] - SM[seq2[k], seq3[l]]:
                str0 += seq0[i]
                str1 += seq1[j]
                str2 += seq2[k]
                str3 += seq3[l]
                i -= 1
                j -= 1
                k -= 1
                l -= 1
                continue

    return getAlignment(str0, str1, str2, str3)

def readFASTA(fileName):
    countSeq = 4
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

def readScore(fileName):
    with open(fileName, 'r') as fin:
        gapPenalty = -int(fin.readline()[:-1])
        nucl = ['A', 'C', 'G', 'T']
        weight = []
        scoringMatrix = {}
        while True:
            tempW = fin.readline().split(' ')
            if tempW[0] == '':
                break
            weight.append(tempW)
            temp = weight[-1][-1].split('\n')
            weight[-1][-1] = temp[0]
    for i in range(len(weight)):
        for j in range(len(weight[i])):
            scoringMatrix[nucl[i], nucl[j]] = -int(weight[i][j])
    score = {}
    score['SM'] = scoringMatrix
    score['GP'] = gapPenalty
    return score

def main():
    sequences = readFASTA(sys.argv[1])
    #print sequences

    score = readScore(sys.argv[2])
    scoringMatrix = score['SM']
    gapPenalty = score['GP']
    #print score

    s = GA(sequences['0'], sequences['1'], sequences['2'], sequences['3'], scoringMatrix, gapPenalty)
    ScoreA = s[len(sequences['0']) - 1][len(sequences['1']) - 1][len(sequences['2']) - 1][len(sequences['3']) - 1]
    #print ScoreA

    alignment = OUTPUTLCS(sequences['0'], sequences['1'], sequences['2'], sequences['3'], len(sequences['0']) - 1,
                          len(sequences['1']) - 1, len(sequences['2']) - 1, len(sequences['3']) - 1, s, scoringMatrix,
                          gapPenalty)

    with open('outputMLCS.txt', 'w') as fout:
        fout.write(alignment['str0'] + '\r\n')
        fout.write(alignment['str1'] + '\r\n')
        fout.write(alignment['str2'] + '\r\n')
        fout.write(alignment['str3'])

main()
