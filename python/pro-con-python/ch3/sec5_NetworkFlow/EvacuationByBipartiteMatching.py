'''
Created on 2017/01/03

@author: kazuyoshi
'''

move=[(-1,0),(0,-1),(0,1),(1,0)]
#dx=[-1,0,0,1]
#dy=[0,-1,1,0]
door=[]
people=[]
dist=dict() # key=door, value=dist for all x,y

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

def bfs(G, X, Y, dr):
    que=[]
    di=[[-1 for i in range(Y)] for j in range(X)]
    di[dr[0]][dr[1]]=0
    que.append(dr)
    while len(que)>0:
        p=que.pop()
        for m in move:
            p2=(p[0]+m[0],p[1]+m[1])
            if 0 <= p2[0] < X and 0 <= p2[1] < Y and G[p2[0]][p2[1]] == '.' and di[p2[0]][p2[1]]<0:
                di[p2[0]][p2[1]] = di[p[0]][p[1]] + 1
                que.append(p2)
    return di



def solve(G,X,Y):
    global door, people, dist
    n = X*Y
    door=[]
    people=[]
    dist=dict()

    for x in range(X):
        for y in range(Y):
            if G[x][y] == 'D':
                dr=(x,y)
                door.append(dr)
                dist[dr] = bfs(G,X,Y,dr)
            elif G[x][y] == '.':
                pp=(x,y)
                people.append(pp)
    d=len(door)
    p=len(people)
    Gr=[[] for i in range(n * n)]

    for i,dr in enumerate(door):
        for j,pp in enumerate(people):
            if dist[dr][pp[0]][pp[1]] >= 0:
                for k in range(dist[dr][pp[0]][pp[1]],n+1):
                    addEdge(Gr, (k-1) * d + i, n * d + j)
    if p==0:
        print(0)
        return
    num=0
    match=[-1 for i in range(n*n)]
    for v in range(n*d):
        used=[0 for i in range(n*n)]
        if dfs(Gr,match,used,v):
            num += 1
            if num == p:
                print(int(v/d)+1)
                return
    print("impossible")


if __name__ == '__main__':
    X=5
    Y=5
    G=['XXDXX',
           'X...X',
           'D...X',
           'X...D',
           'XXXXX']
    solve(G,X,Y)
    
    X=5
    Y=12
    G=['XXXXXXXXXXXX',
           'X..........D',
           'X.XXXXXXXXXX',
           'X..........X',
           'XXXXXXXXXXXX']
    solve(G,X,Y)
    
    X=5
    Y=5
    G=['XDXXX',
           'X.X.D',
           'XX.XX',
           'D.X.X',
           'XXXXX']
    solve(G,X,Y)