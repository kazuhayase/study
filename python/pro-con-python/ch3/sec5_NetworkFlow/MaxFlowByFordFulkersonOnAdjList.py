'''
Created on 2017/01/01

@author: kazuyoshi.hayase
'''

INF=1<<32
MAXV=100

#from collections import namedtuple
#edge = namedtuple('edge', 'to cap rev')


G=[[] for i in range(MAXV)] # Graph by adjacent list
used=[False for i in range(MAXV)]

def addEdge (fr, to, cap):
    G[fr].append([to, cap, len(G[to])])
    G[to].append([fr, 0, len(G[fr])-1])

def dfs(v,t,f):
    if v==t:
        return f
    used[v]=True
    for e in G[v]:
        if (not used[e[0]]) and e[1] > 0:
            d = dfs(e[0], t, min(f, e[1]))
            if d>0:
                e[1] -= d
                G[e[0]][e[2]][1] += d
                return d
    return 0

def maxFlow(s,t):
    flow=0
    global used
    while True:
        used = [False for i in range(MAXV)]
        f = dfs(s,t,INF)
        if f==0:
            return flow
        flow += f

if __name__ == '__main__':
    s=0
    t=4
    E=[[s,1,10],[s,2,2],[1,2,6],[1,3,6],[2,t,5],[3,2,3],[3,t,8]]
    for e in E:
        addEdge(e[0],e[1],e[2])
    print(maxFlow(s,t))