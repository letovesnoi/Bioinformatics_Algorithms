__author__ = 'lenk'

from collections import defaultdict
import sys

def readFASTA(fileName):
    s = ''
    with open(fileName, 'r') as fin:
        fin.readline()
        for line in fin:
            s += line.strip()
    return s

def readFASTAPatterns(fileName):
    Patterns = []
    with open(fileName, 'r') as fin:
        line = fin.readline()
        while line != '':
            line = fin.readline().strip()
            Patterns.append('')
            while '>' not in line and line != '':
                Patterns[-1] += line.strip()
                line = fin.readline().strip()
    return Patterns

def sort_bucket(str, bucket, order):
    d = defaultdict(list)
    for i in bucket:
        key = str[i:i + order]
        d[key].append(i)
    result = []
    for k, v in sorted(d.iteritems()):
        if len(v) > 1:
            result += sort_bucket(str, v, order * 2)
        else:
            result.append(v[0])
    return result

def FirstOccurrence(FirstColumn):
    firstOccurence = {}
    symbols = ['$', 'A', 'C', 'G', 'T']
    for symbol in symbols:
        firstOccurence[symbol] = FirstColumn.find(symbol)
    return firstOccurence

def Count(LastColumn, C):
    symbols = ['$', 'A', 'C', 'G', 'T']
    count = {'$':[0], 'A':[0], 'C':[0], 'G':[0], 'T':[0]}
    for symbol in symbols:
        tempCount = 0
        for i in range(1, len(LastColumn) + 1):
            j = LastColumn[i - 1]
            if j == symbol:
                tempCount += 1
            if (i) % C == 0:
                count[symbol].append(tempCount)
    return count

def checkPoint(index, symbol, LasTColumn, C):
    addCount = 0
    currentNI = index / C + 1
    begin = (currentNI - 1) * C
    end = index
    for i in range(begin, end, 1):
        if LasTColumn[i] == symbol:
            addCount += 1
    return addCount

'''def BWTC(s):
    cyclicRotation = []
    for i in range(1, len(s) + 1):
        cyclicRotation.append(s[-i:] + s[:-i])
    cyclicRotation.sort()
    BWT = ''
    for string in cyclicRotation:
        BWT += string[-1]
    return BWT'''

def BWMATCHING(LastColumn, Pattern, FirstOccurrence, Count, C):
        top = 0
        bottom = len(LastColumn) - 1
        while top <= bottom:
            if Pattern != '':
                symbol = Pattern[-1:]
                Pattern = Pattern[:-1]
                if symbol in LastColumn[top:bottom + 1]:
                    temptop = top
                    tempbottom = bottom
                    top = FirstOccurrence[symbol] + Count[symbol][temptop / C]
                    addCount = checkPoint(temptop, symbol, LastColumn, C)
                    top += addCount
                    bottom = FirstOccurrence[symbol] + Count[symbol][(tempbottom + 1) / C] - 1
                    addCount = checkPoint(tempbottom + 1, symbol, LastColumn, C)
                    bottom += addCount
                else:
                    return 0
            else:
                return [top, bottom]

def main():
    C = 100
    Text = readFASTA(sys.argv[1]) + '$'
    Patterns = readFASTAPatterns(sys.argv[2])

    #LastColumn = BWTC(Text)
    suffixArray = sort_bucket(Text, (i for i in range(len(Text))), 1)
    LastColumn = ''
    for i in range(len(suffixArray)):
        LastColumn += Text[suffixArray[i] - 1]

    FirstColumnList = []
    for i in range(len(LastColumn)):
        FirstColumnList.append(LastColumn[i])
    FirstColumnList.sort()
    FirstColumn=''
    for i in range(len(FirstColumnList)):
        FirstColumn += FirstColumnList[i]

    firstOccurence = FirstOccurrence(FirstColumn)
    count = Count(LastColumn, C)
    suffixArray = sort_bucket(Text, (i for i in range(len(Text))), 1)

    ans = {}
    for i in range(len(Patterns)):
        pair = BWMATCHING(LastColumn, Patterns[i], firstOccurence, count, C)
        if pair != 0:
            ans[Patterns[i]] = suffixArray[pair[0]:pair[1] + 1]
            ans[Patterns[i]].sort()

    with open('outputMPM.txt', 'w') as fout:
        for pattern in Patterns:
            fout.write('>' + pattern + ': ')
            if pattern in ans:
                for i in range(len(ans[pattern])):
                    fout.write(str(ans[pattern][i]) + ' ')
                fout.write('\r\n')
            else:
                fout.write('no occurrences\r\n')

main()