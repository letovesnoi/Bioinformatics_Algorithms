__author__ = 'lenk'

import sys

rootTree = ''
hammD = 0
internalSeq = {}

def getElement(line, i):
    i0 = i
    while i < len(line) and line[i] not in [',', '(', ')']:
        i += 1
    return line[i0:i], i - 1

def getTree(treeLine, seq):
    global rootTree
    tree = {}
    nameStack = []
    countStack = []
    needsARoot = False
    i = 0
    while i < len(treeLine):
        if treeLine[i] == "(":
            countStack.append(0)
            needsARoot = False
        elif treeLine[i] == ",":
            countStack[-1] = countStack[-1] + 1
        elif treeLine[i] == ")":
            countStack[-1] = countStack[-1] + 1
            needsARoot = True
        else:
            name, i = getElement(treeLine, i)
            if needsARoot == True:
                needsARoot = False
                tmpList = []
                for j in range(countStack[-1]):
                    tmpList.append(nameStack[-1])
                    nameStack.pop()
                tree[name] = tmpList
                countStack.pop()
            nameStack.append(name)
        i += 1
    if needsARoot == True:
        if nameStack[0] in seq:
            rootTree = nameStack[1]
            tree[rootTree] = []
            tree[rootTree].append(nameStack[0])
        else:
            rootTree = nameStack[0]
            tree[rootTree] = []
            tree[rootTree].append(nameStack[1])
    rootTree = name
    return tree

def getVertexSet(tree, seq, i):
    global rootTree
    query = []
    setL = {}
    reverseTree = {}
    for vertex in tree:
        for child in tree[vertex]:
            reverseTree[child] = vertex
    for leave in seq:
        query.append(leave)
        setL[leave] = set(seq[leave][i])
    while query != []:
        current = query[0]
        if current == rootTree:
            break
        temp = set()
        if len(tree[reverseTree[current]]) == 2:
            temp = setL[tree[reverseTree[current]][0]] & setL[tree[reverseTree[current]][1]]
        else:
            temp = setL[tree[reverseTree[current]][0]]
        if len(temp) == 0:
            for child in tree[reverseTree[current]]:
                temp = temp | setL[child]
        setL[reverseTree[current]] = temp
        for child in tree[reverseTree[current]]:
            query.remove(child)
        query.append(reverseTree[current])
    #print setL
    #print reverseTree
    return setL

def getVertexSeq(tree, set, current, seq, i):
    global rootTree
    global hammD
    global internalSeq
    for child in tree[current]:
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
        treeLine = fin.readline()[:-2]
        while True:
            temp = fin.readline()[1:-1]
            if temp == '':
                break
            seq[temp] = fin.readline()[:-1]
    #print '\r\n' + treeLine + '\r\n'
    tree = getTree(treeLine, seq)
    #print tree

    n = len(seq.values()[0])
    internalSeq[rootTree] = ''
    for i in range(n):
        setL = getVertexSet(tree, seq, i)
        listL = list(setL[rootTree])
        internalSeq[rootTree] += listL[0]
        internalSeq = getVertexSeq(tree, setL, rootTree, seq, i)

    with open('outputF.txt', 'w') as fout:
        fout.write(str(hammD) + '\r\n')
        for name in internalSeq:
            fout.write('>' + name + '\r\n' + internalSeq[name] + '\r\n')

main()