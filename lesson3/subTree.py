__author__ = 'lenk'

import sys

def getMaxWSubTree(u, tree, N, maxW):
    if N == 0:
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
    if right != None:
        for i in range(N - 1 + 1):
            rightMax = 0
            if i != 0:
                currentW = tree[u][left] + tree[u][right]
                rightMax = getMaxWSubTree(right, tree, i, maxW)
            else:
                currentW = tree[u][left]
            leftMax = getMaxWSubTree(left, tree, N - 1 - i, maxW)
            m.append(leftMax + rightMax + currentW)
    else:
        currentW = tree[u][left]
        leftMax = getMaxWSubTree(left, tree, N - 1, maxW)
        m.append(leftMax + currentW)
    temp = m[0]
    for w in m:
        if w > temp:
            temp = w
    maxW += temp
    return maxW

def main():
    tree = {}
    with open(sys.argv[1], 'r') as fin:
        temp = fin.readline().split(' ')
        n = int(temp[0])
        q = int(temp[1][:-1])
        for vertex in range(1, n + 2):
            tree[vertex] = {}
        for line in fin:
            temp = line.split(' ')
            temp[2] = temp[2][:-1]
            tree[int(temp[0])][int(temp[1])] = int(temp[2])
            #tree[int(temp[1])][int(temp[0])] = int(temp[2])
    #print n, q, '\r\n', tree
    maxW = getMaxWSubTree(1, tree, q, 0)
    print maxW

    with open('outputST.txt', 'w') as fout:
        fout.write(str(maxW))


main()