'''
Created on 2016/12/03

@author: kazuyoshi
'''
G=[]
d=[]
V=0 
E=0

INF=1<<30

import heapq

def dijkstra(s):
    global G,d,V,E
    d=[INF for i in range(V)]
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
                heapq.heappush(q, (d[t],t))
                
if __name__ == '__main__':
    V=int(input())
    E=int(input())
    G=[[] for i in range(V)]
    for i in range(E):
        (f,t,c)=map(int, input().split())
        G[f].append((t,c))
        G[t].append((f,c))
    dijkstra(0)
    print (d)