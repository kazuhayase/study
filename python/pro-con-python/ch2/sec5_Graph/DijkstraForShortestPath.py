'''
Created on 2016/12/03

@author: kazuyoshi
'''
G=[]

prev=[]
V=0 
E=0

INF=1<<30

import heapq

def dijkstra(s):
    global G,V,E,prev
    d=[INF for i in range(V)]
    prev=[-1 for i in range(V)]
    d[s]=0
    q=[]
    heapq.heappush(q, (0,s))
    
    while len(q)>0:
        (pd, pv) = heapq.heappop(q)
        if d[pv] < pd:
            continue
        for (t,c) in G[pv]:
            if d[t] > d[pv] + c:
                d[t] = d[pv] + c
                prev[t]=pv
                heapq.heappush(q, (d[t],t))
    return d

def getPath(t):
    global prev
    path=[]
    while t !=-1:
        path.append(t)
        t=prev[t]
    path.reverse()
    return path

if __name__ == '__main__':
    V=int(input())
    E=int(input())
    G=[[] for i in range(V)]
    for i in range(E):
        (f,t,c)=map(int, input().split())
        G[f].append((t,c))
        G[t].append((f,c))
    d=dijkstra(0)
    print (d)
    print(getPath(V-1))