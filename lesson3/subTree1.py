__author__ = 'lenk'

import sys
import threading

set = []
newTree = {}

def getMaxWSubTree(u, tree, q, maxW):
    if q == 0:
        return maxW
    if len(tree[u]) == 2:
        left = tree[u].keys()[0]
        right = tree[u].keys()[1]
    elif len(tree[u]) == 1:
        left = tree[u].keys()[0]
        right = None
    else:
        return 0
    m = []
    for i in range(q + 1):
        currentW = 0
        leftMax = 0
        rightMax = 0
        if i != 0 and right != None:
            currentW += tree[u][right]
            rightMax = getMaxWSubTree(right, tree, i - 1, maxW)
        if q - i != 0:
            currentW += tree[u][left]
            leftMax = getMaxWSubTree(left, tree, q - 1 - i, maxW)
        m.append(leftMax + rightMax + currentW)
    temp = m[0]
    for w in m:
        if w > temp:
            temp = w
    maxW += temp
    return maxW

def getTree(u, tree):
    global set
    global newTree
    set.append(u)
    for child in tree[u]:
        if child not in set:
            newTree[u][child] = tree[u][child]
            getTree(child, tree)
    return newTree

def main():
    global newTree
    tree = {}
    with open(sys.argv[1], 'r') as fin:
        temp = fin.readline().split(' ')
        n = int(temp[0])
        q = int(temp[1][:-1])
        for vertex in range(1, n + 1):
            tree[vertex] = {}
        for line in fin:
            temp = line.split(' ')
            temp[2] = temp[2][:-1]
            tree[int(temp[0])][int(temp[1])] = int(temp[2])
            tree[int(temp[1])][int(temp[0])] = int(temp[2])
    #print tree
    for vertex in range(1, n + 1):
        newTree[vertex] = {}
    newTree = getTree(1, tree)
    #print newTree
    maxW = getMaxWSubTree(1, newTree, q, 0)
    print maxW

'''threading.stack_size(67108864)
sys.setrecursionlimit(2 ** 20)
thread = threading.Thread(target=main)
thread.start()'''

main()