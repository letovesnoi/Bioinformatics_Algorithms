__author__ = 'lenk'

import sys

rootTree = ''
hammD = 0
internalSeq = {}

def getTree(treeLine):
    global rootTree
    tree = {}
    leaves = []
    countChild = []
    i = 0
    current = ''
    while i < len(treeLine):
        if treeLine[i] == ';':
            rootTree = current
            tree[rootTree] = {}
            tree[rootTree]['child'] = []
            for j in xrange(countChild[-1] + 1):
                tree[rootTree]['child'].append(leaves[-1])
                leaves.pop()
            countChild.pop()
            break
        elif treeLine[i] == '(':
            countChild.append(0)
        elif treeLine[i] == ',':
            leaves.append(current)
            current = ''
            root = ''
            countChild[-1] = countChild[-1] + 1
        elif treeLine[i] == ')':
            leaves.append(current)
            i += 1
            while treeLine[i] != ',' and treeLine[i] != ';':
                root = ''
                while treeLine[i] != ')' and treeLine[i] != ',' and treeLine[i] != ';':
                    root += treeLine[i]
                    i += 1
                current = ''
                tree[root] = {}
                tree[root]['child'] = []
                for j in xrange(countChild[-1] + 1):
                    tree[root]['child'].append(leaves[-1])
                    leaves.pop()
                countChild.pop()
                leaves.append(root)
                if treeLine[i] != ',' and treeLine[i] != ';':
                    countChild[-1] = countChild[-1] + 1
                    i += 1
        else:
            while treeLine[i] != ')' and treeLine[i] != ',' and treeLine[i] != ';':
                current += treeLine[i]
                i += 1
            i -= 1
        i += 1
    rootTree = root
    return tree

def getVertexSet(tree, seq, i):
    global rootTree
    query = []
    setL = {}
    reverseTree = {}
    for vertex in tree:
        for child in tree[vertex]['child']:
            reverseTree[child] = vertex
    for leave in seq:
        query.append(leave)
        setL[leave] = set(seq[leave][i])
    while query != []:
        current = query[0]
        if current == rootTree:
            break
        temp = set()
        if len(tree[reverseTree[current]]['child']) == 2:
            temp = setL[tree[reverseTree[current]]['child'][0]] & setL[tree[reverseTree[current]]['child'][1]]
        else:
            temp = setL[tree[reverseTree[current]]['child'][0]]
        if len(temp) == 0:
            for child in tree[reverseTree[current]]['child']:
                temp = temp | setL[child]
        setL[reverseTree[current]] = temp
        for child in tree[reverseTree[current]]['child']:
            query.remove(child)
        query.append(reverseTree[current])
    #print setL
    #print reverseTree
    return setL

def getVertexSeq(tree, set, current, seq, i):
    global rootTree
    global hammD
    global internalSeq
    for child in tree[current]['child']:
        if child in seq:
            if seq[child][i] != internalSeq[current][i]:
                hammD += 1
        else:
            if child not in internalSeq:
                internalSeq[child] = ''
            if internalSeq[current][i] in set[child]:
                internalSeq[child] += internalSeq[current][i]
            else:
                listL = list(set[child])
                internalSeq[child] += listL[0]
                hammD += 1
            getVertexSeq(tree, set, child, seq, i)
    return internalSeq

def main():
    global rootTree
    global hammD
    global internalSeq
    seq = {}
    with open('inputF.txt', 'r') as fin:
        treeLine = fin.readline()[:-1]
        #print treeLine
        while True:
            temp = fin.readline()[1:-1]
            if temp == '':
                break
            seq[temp] = fin.readline()[:-1]
    tree = getTree(treeLine)
    print tree
    n = len(seq.values()[0])
    internalSeq[rootTree] = ''
    for i in range(n):
        setL = getVertexSet(tree, seq, i)
        listL = list(setL[rootTree])
        internalSeq[rootTree] += listL[0]
        internalSeq = getVertexSeq(tree, setL, rootTree, seq, i)
    #print seq
    #print internalSeq, hammD

    with open('outputF.txt', 'w') as fout:
        fout.write(str(hammD) + '\r\n')
        for name in internalSeq:
            fout.write('>' + name + '\r\n' + internalSeq[name] + '\r\n')
main()