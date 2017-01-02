'''
Created on 2017/01/02

@author: kazuyoshi.hayase
'''

from heapq import heappush, heappop

INF=1<<32
def addEdge(G,f,t,cap,cost):
    G[f].append([t,cap,cost,len(G[t])])
    G[t].append([f,0,-cost,len(G[f])-1])
    
def minCostFlow(G,V,s,t,f):
    res=0
    h=[0 for i in range(V)]
    prevv=[-1 for i in range(V)]
    preve=[[] for i in range(V)]
    while f>0:
        #print(h) #display potential
        que=[]
        dist=[INF for i in range(V)]
        dist[s]=0
        heappush(que,(0,s))
        while len(que) > 0:
            p = heappop(que)
            v = p[1]
            if dist[v] < p[0]:
                continue
            for e in G[v]:
                if e[1]>0 and dist[e[0]] > dist[v] + e[2] + h[v] - h[e[0]]:
                    dist[e[0]] = dist[v] + e[2] + h[v] - h[e[0]]
                    prevv[e[0]] = v
                    preve[e[0]] = e
                    heappush(que,(dist[e[0]],e[0]))
        if dist[t] == INF:
            return -1
        for v in range(V):
            h[v] += dist[v]
        d=f
        v=t
        while v != s:
            e=preve[v]
            d=min(d, e[1])
            v=prevv[v]
        f -=d
        res += d * h[t]
        v=t
        while v != s:
            e=preve[v]
            e[1] -= d
            G[v][e[3]][1] += d
            v=prevv[v]
    return res

if __name__ == '__main__':
    s=0
    t=4
    f=9
    #Edge [from,to,cap,cost]
    E=[[s,1,10,2],[s,2,2,4],[1,2,6,6],[1,3,6,2],[2,t,5,2],[3,2,3,3],[3,t,8,6]]
    V=5
    G=[[] for i in range(V)] # Graph by adjacent list
    for e in E:
        addEdge(G,e[0],e[1],e[2],e[3])
    print(minCostFlow(G,V,s,t,f))
    