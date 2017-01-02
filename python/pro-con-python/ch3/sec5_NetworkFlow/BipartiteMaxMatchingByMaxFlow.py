'''
Created on 2017/01/02

@author: kazuyoshi.hayase
'''

INF=1<<32

def addEdge (G, fr, to, cap):
    G[fr].append([to, cap, len(G[to])])
    G[to].append([fr, 0, len(G[fr])-1])

def bfs(G, V, s):
    level = [-1 for i in range(V)]
    que=[]
    level[s]=0
    que.append(s)
    while len(que)>0:
        v=que.pop()
        for e in G[v]:
            if e[1] > 0 and level[e[0]]<0:
                level[e[0]] = level[v]+1
                que.append(e[0])
    return level

def dfs(level,iter,G,v,t,f):
    if v==t:
        return f
    for i in range(iter[v],len(G[v])):
        iter[v] = i
        e=G[v][i]
        if e[1]>0 and level[v] < level[e[0]]:
            d = dfs(level,iter,G,e[0], t, min(f,e[1]))
            if d>0:
                e[1] -= d
                G[e[0]][e[2]][1] += d
                return d
    return 0

def maxFlow(G,V,s,t):
    flow=0
    while True:
        level = bfs(G,V,s)
        if level[t] < 0:
            return flow
        iter=[0 for i in range(V)]
        while True:
            f = dfs(level,iter,G,s,t,INF)
            if f==0:
                break
            flow +=f

def bipartiteMatching(N,K,can):
    s=N+K
    t=s+1
    V=t+1
    G=[[] for i in range(V)] # Graph by adjacent list

    for i in range(N):
        addEdge(G,s,i,1)
    for i in range(K):
        addEdge(G,i+N,t,1)
    for e in can:
        addEdge(G,e[0],e[1]+N,1)
    print(maxFlow(G,V,s,t))
    pair=[]
    for i in range(N):
        for e in G[i]:
            if e[1] == 0:
                pair.append((i,e[0]-N))
    print(pair)
    
if __name__ == '__main__':
    N=3 #computers (0-indexed)
    K=3 #jobs (0-indexed)
    can=[[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]]
    bipartiteMatching(N, K, can)