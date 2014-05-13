__author__ = 'lenk'

import sys

def readFASTA(fileName):
    rna = ''
    with open(fileName, 'r') as fin:
        fin.readline()
        for line in fin:
            rna += line.strip()
    return rna

def getTandemRepeat(seq):
    for lenLETRepeat in range(len(seq) / 2, 0, -1):
        match = 0
        for i in range(len(seq) - lenLETRepeat):
            if seq[i] == seq[i + lenLETRepeat]:
                match += 1
                if match == lenLETRepeat:
                    return seq[i + 1:i + lenLETRepeat + 1]
            else:
                match = 0
    return ''

def main():
    rna = readFASTA(sys.argv[1])
    letRepeat = getTandemRepeat(rna)
    with open('outputLETR.fasta', 'w') as fout:
        fout.write('>repeat\r\n' + letRepeat + '\r\n')

main()