__author__ = 'lenk'

import sys

def readFASTA(fileName):
    rna = ''
    with open(fileName, 'r') as fin:
        fin.readline()
        for line in fin:
            rna += line.strip()
    return rna

def LongestRepeatWith1Mismath(seq):
    repeats = []
    ans = {'i': 0, 'j': 0, 'l': 0}
    for shift in range(1, len(seq)):
        start = 0
        stop = len(seq) - shift
        errors = 0
        current = start
        for i in range(start, stop, 1):
            while current < stop and (errors < 1 or seq[current] == seq[current + shift]):
                if seq[current] != seq[current + shift]:
                    errors += 1
                current += 1
            if current - i > ans['l'] and i != i + shift and i + current - i - 1 < i + shift:
                ans['i'] = i
                ans['j'] = i + shift
                ans['l'] = current - i
            if seq[i] != seq[i + shift]:
                errors -= 1
    repeats.append(seq[ans['i']:ans['i'] + ans['l']])
    repeats.append(seq[ans['j']:ans['j'] + ans['l']])
    return repeats

def main():
    seq = readFASTA(sys.argv[1])
    repeats = LongestRepeatWith1Mismath(seq)
    with open('outputLRW1M.txt', 'w') as fout:
        fout.write('>repeat1\r\n' + repeats[0] + '\r\n>repeat2\r\n' + repeats[1])

main()
