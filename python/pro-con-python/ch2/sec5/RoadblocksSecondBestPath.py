'''
Created on 2016/12/04

@author: kazuyoshi
'''

G=[]
prev=[]
prev2=[]
N=0 
R=0

INF=1<<30

import heapq

def dijkstra(s):
    global G,N,R,prev,prev2
    d=[INF for i in range(N)]
    d2=[INF for i in range(N)]
    prev=[-1 for i in range(N)]
    prev2=[-1 for i in range(N)]
    d[s]=0
    q=[]
    heapq.heappush(q, (0,s))
    
    while len(q)>0:
        (pd, pv) = heapq.heappop(q)
        if d2[pv] < pd:
            continue
        for (t,c) in G[pv]:
            dd=pd+c
            if d[t] > dd:
                d[t],dd = dd,d[t]
                heapq.heappush(q,(d[t],t))
                prev[t]=pv
            if d2[t] > dd and d[t] < dd:
                d2[t]=dd
                heapq.heappush(q,(d2[t],t))
                if t != s:
                    prev2[t]=pv
                
    return (d,d2)

def getPath(t):
    global prev,prev2
    path=[]
    path2=[]
    t2=t
    while t !=-1:
        path.append(t)
        t=prev[t]
#    while t2 !=-1:
#        path2.append(t2)
#        if prev2[t2] == -1:
#            t2 = prev[t2]
#        else:
#            t2=prev2[t2]

    path.reverse()
 #   path2.reverse()
    return (path)

if __name__ == '__main__':
    N=int(input())
    R=int(input())
    G=[[] for i in range(N)]
    for i in range(R):
        (f,t,c)=map(int, input().split())
        G[f].append((t,c))
        G[t].append((f,c))
    #(d,d2)=dijkstra(0)
    print (dijkstra(0))
    print(getPath(N-1))