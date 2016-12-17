'''
Created on 2016/12/04

@author: kazuyoshi
'''
import heapq
G=[]   

V=0
E=0
INF=1<30

def prim():
    global G,V,E
    que=[] #(cost, f, t)
    T=[]
    X=[]
    res=0
    MST=[]
    
    X.append(0)
    for (t,c) in G[0]:
        heapq.heappush(que, (c,0,t))

    while len(X)<V:
        while True:
            (c,f,t) = heapq.heappop(que)
            if not t in X:
                X.append(t)
                res += c
                T.append((f,t))
                for (tt,cc) in G[t]:
                    heapq.heappush(que, (cc,t,tt))
                break
    return (T,res)    
    
if __name__ == '__main__':
    V=int(input())
    E=int(input())
    G=[[] for i in range(V)]
    for i in range(E):
        (f,t,c)=map(int,input().split())
        G[f].append((t,c))
        G[t].append((f,c))
    (T,c) = prim()
    print("cost={}".format(c))
    print(T)