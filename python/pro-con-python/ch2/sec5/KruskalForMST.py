'''
Created on 2016/12/04

@author: kazuyoshi
'''
G=[]
V=0
E=0
INF=1<30

from ch2.sec4 import UnionFindTree  # @UnresolvedImport

def kruskal():
    G.sort()
    uft=UnionFindTree.UFT(V)
    res=0
    T=[]
    for (c,f,t) in G:
        if not uft.same(f,t):
            uft.unite(f,t)
            res+=c
            T.append((f,t))
    return (T,res)

if __name__ == '__main__':
    V=int(input())
    E=int(input())
    
    for i in range(E):
        (f,t,c)=map(int,input().split())
        G.append((c,f,t))
    (T,c) = kruskal()
    print("cost={}".format(c))
    print(T)