'''
Created on 2017/03/05

@author: kazuyoshi
'''

def addEdge(G,u,v):
    G[u].append(v)
    G[v].append(u)

def dfs(G,match,used,v):
    used[v]=True
    for u in G[v]:
        w=match[u]
        if w < 0 or (not used[w] and dfs(G,match,used,w)):
            match[v]=u
            match[u]=v
            return True
    return False

def bipartiteMatching(G,V):
    res=0
    match=[-1 for i in range(V)]
    for v in range(V):
        if match[v]<0:
            used=[0 for i in range(V)]
            if dfs(G,match,used,v):
                res += 1
    return res,match

def solve(n,k,p):
    V=n*2
    G=[[] for i in range(V)]
    for i in range (n):
        for j in range(n):
            if i==j:
                continue
            f = True
            for ii in range(k):
               if p[j][ii] >= p[i][ii]:
                   f= False
            if f:
                addEdge(G,i,n+j)
    ans = n - bipartiteMatching(G,V)[0]
    print(ans) 
    

if __name__ == '__main__':
    n=5
    k=2
    price=[[1,1],[2,2],[5,4],[4,4],[4,1]]
    solve(n,k,price)