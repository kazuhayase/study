'''
Created on 2017/01/02

@author: kazuyoshi.hayase
'''
INF=1<<32
MAXV=100

G=[[] for i in range(MAXV)] # Graph by adjacent list
level=[]
iter=[]

#edge =[to, cap, rev]

def addEdge (fr, to, cap):
    G[fr].append([to, cap, len(G[to])])
    G[to].append([fr, 0, len(G[fr])-1])

def bfs(s):
    global level
    level = [-1 for i in range(MAXV)]
    que=[]
    level[s]=0
    que.append(s)
    while len(que)>0:
        v=que.pop()
        for e in G[v]:
            if e[1] > 0 and level[e[0]]<0:
                level[e[0]] = level[v]+1
                que.append(e[0])

def dfs(v,t,f):
    global iter
    if v==t:
        return f
    for i in range(iter[v],len(G[v])):
        iter[v] = i
        e=G[v][i]
        if e[1]>0 and level[v] < level[e[0]]:
            d = dfs(e[0], t, min(f,e[1]))
            if d>0:
                e[1] -= d
                G[e[0]][e[2]][1] += d
                return d
    return 0

def maxFlow(s,t):
    global iter
    flow=0
    while True:
        bfs(s)
        if level[t] < 0:
            return flow
        iter=[0 for i in range(MAXV)]
        while True:
            f = dfs(s,t,INF)
            if f==0:
                break
            flow +=f

if __name__ == '__main__':
    s=0
    t=4
    E=[[s,1,10],[s,2,2],[1,2,6],[1,3,6],[2,t,5],[3,2,3],[3,t,8]]
    for e in E:
        addEdge(e[0],e[1],e[2])
    print(maxFlow(s,t))