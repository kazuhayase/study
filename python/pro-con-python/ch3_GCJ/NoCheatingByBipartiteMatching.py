'''
Created on 2017/02/05

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

dd=[(-1,0),(1,0),(-1,-1),(1,-1)]

def solve(M,N,seat):
    num=0
    V=M*N
    G=[[] for i in range(V)]
    for y in range(M):
        for x in range(N):
            if seat[y][x]=='.':
                num += 1
                for (dx,dy) in dd:
                    x2 = x+dx
                    y2 = y+dy
                    if 0<=x2<N and 0<=y2<M and seat[y2][x2] == '.':
                        addEdge(G,x*M+y,x2*M+y2)
    res,match=bipartiteMatching(G,V)
    return num-res

if __name__ == '__main__':
    M=2
    N=3
    seat=['...','...']
    print(solve(M,N,seat))
    seat=['x.x','x.x']
    print(solve(M,N,seat))