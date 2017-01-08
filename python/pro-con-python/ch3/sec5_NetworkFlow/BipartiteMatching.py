'''
Created on 2017/01/02

@author: kazuyoshi.hayase
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

if __name__ == '__main__':
    V=6
    G=[[] for i in range(V)]
    E=[[0,3],[0,4],[1,3],[1,5],[2,4],[2,5]]
       #[3,0],[4,0],[3,1],[5,1],[4,2],[5,2]]
    for e in E:
        addEdge(G,e[0],e[1])
    num,match = bipartiteMatching(G,V)
    print(num)
    #print(match)
    pair=[]
    N=V>>1
    for i in range(N):
        pair.append((i,match[i]-N))
    print(pair)
        
        