__author__ = 'lenk'

import sys
import threading

tree = {}
mark = {}

def getSum(u, tree, sum, dist):
    #global mark
    #m = True
    #for vertex in dist:
        #if vertex in tree[u] or vertex == u:
    distNew = dist[:]
    for child1 in tree[u]:
        sum += tree[u][child1] * 2
        #print child1, u
        #print u, child1

        sum = getSum(child1, tree, sum, distNew)
        #mark[child1] = True

        '''m = True
        for child in tree[u].keys():
            if mark[child] == False:
                m = False
        if m == True:
            for child in tree[u].keys():
                del distNew[child]'''

        for vertex in dist[child1]:
            distNew[u][vertex] = dist[child1][vertex] + tree[u][child1]
            sum += (distNew[child1][vertex] + tree[u][child1]) * 2
            #print vertex, u
            #print u, vertex
        for child2 in tree[u]:
            if child1 != child2:
                sum += dist[u][child1] + dist[u][child2]
                #print child1, child2
                for vertex1 in dist[child1]:
                    sum += (dist[child1][vertex1] + tree[u][child1] + tree[u][child2]) * 2
                    #print vertex1, child2
                    #print child2, vertex1
                    for vertex2 in dist[child2]:
                        sum += dist[child1][vertex1] + dist[child2][vertex2] + \
                               tree[u][child1] + tree[u][child2]
                        #print vertex1, vertex2
    print distNew
    return sum

def main():
    global mark
    sum = 0.0
    dist = []
    with open('inputAT.txt', 'r') as fin:
        n = int(fin.readline())
        for vertex in range(n):
            tree[vertex] = {}
            dist.append({})
            mark[vertex] = False
        for line in fin:
            temp = line.split(' ')
            temp[2] = temp[2][:-1]
            tree[int(temp[0]) - 1][int(temp[1]) - 1] = float(temp[2])
            dist[int(temp[0]) - 1][int(temp[1]) - 1] = float(temp[2])
    #print tree
    sum = getSum(0, tree, sum, dist)
    #print sum
    #print dist
    averageTravel = round(sum / n / (n - 1), 4)
    print(averageTravel)


threading.stack_size(67108864)
sys.setrecursionlimit(2 ** 20)
thread = threading.Thread(target=main)
thread.start()
