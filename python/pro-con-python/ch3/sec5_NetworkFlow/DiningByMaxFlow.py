'''
Created on 2017/01/03

@author: kazuyoshi
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

def solve(N,F,D,likeF,likeD):
    #cattle = 0 .. N-1
    #food = N .. N+F-1
    #drink = N+F .. N+F+D-1
    s=F+N+D
    t=s+1
    V=t+1
    G=[[] for i in range(V)]
    for i in range(F):
        addEdge(G,s,N+i,1)
    for i in range(D):
        addEdge(G,N+F+i,t,1)
    for i in range(N):
        for f in likeF[i]:
            addEdge(G,N+f-1,i,1)
        for d in likeD[i]:
            addEdge(G,i,N+F+d-1,1)
    return maxFlow(G,V,s,t)

if __name__ == '__main__':
    N=4
    F=3
    D=3
    likeF=[[1,2],[2,3],[1,3],[1,3]]
    likeD=[[1,3],[1,2],[1,2],[3]]
    print(solve(N,F,D,likeF,likeD))
    
    