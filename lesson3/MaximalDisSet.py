__author__ = 'lenk'

import sys

I = {}
set = []

def getIndependentSet(u, tree):
    global I
    global set
    if u in I:
        return I[u]
    children_sum = 0
    grandchildren_sum = 0
    for child in tree[u]:
        children_sum += getIndependentSet(child, tree)
    for child in tree[u]:
        for grandChild in tree[child]:
            grandchildren_sum += getIndependentSet(grandChild, tree)
    I[u] = max(1 + grandchildren_sum, children_sum)
    if I[u] == 1 + grandchildren_sum and I[u] != children_sum:
        set.append(u)
    return I[u]

def main():
    global I
    global set
    tree = {}
    with open(sys.argv[1], 'r') as fin:
        n = int(fin.readline())
        for vertex in range(1, n + 1):
            tree[vertex] = []
        for line in fin:
            temp = line.split(' ')
            temp[1] = temp[1][:-1]
            tree[int(temp[0])].append(int(temp[1]))

    count = getIndependentSet(1, tree)
    set.sort()
    with open('outputMDS.txt', 'w') as fout:
        fout.write(str(count) + '\r\n')
        for vertex in set:
            fout.write(str(vertex) + ' ')

main()