'''
Created on 2017/01/08

@author: kazuyoshi
'''
INF=1<<32

def solve(N,M,XYB,PQC,E):
    V=N+M+1
    g=[[INF for i in range(V)] for j in range(V)]
    for j,(p,q,c) in enumerate(PQC): 
        Sum=0
        for i,(x,y,b) in enumerate(XYB):
            c=abs(x-p)+abs(y-q)+1
            g[i][N+j]=c
            if E[i][j]>0:
                g[N+j][i] = -c
            Sum += E[i][j]
        if Sum>0:
            g[N+M][N+j]=0
        if Sum<c:
            g[N+j][N+M]=0
    prev=[[i for j in range(V)] for i in range(V)]
    for k in range(V):
        for i in range(V):
            for j in range(V):
                if g[i][j] > g[i][k]+g[k][j]:
                    g[i][j] = g[i][k]+g[k][j]
                    prev[i][j] = prev[k][j]
                    if i==j and g[i][i]<0:
                        used=[False for i in range(V)]
                        v=i
                        while not used[v]:
                            used[v]=True
                            if v != N+M and prev[i][v] !=N+M:
                                if v>=N:
                                    E[prev[i][v]][v-N] += 1
                                else:
                                    E[v][prev[i][v]-N] -= 1
                            v = prev[i][v]
                        print("SUBOPTIMAL")
                        print(E)
                        return
    print("OPTIMAL")
        
if __name__ == '__main__':
    N=3
    M=4
    XYB=[[-3,3,5],[-2,-2,6],[2,2,5]]
    PQC=[[-1,1,3],[1,1,4],[-2,-2,7],[0,-1,3]]
    E=[[3,1,1,0],[0,0,6,0],[0,3,0,2]]
    solve(N,M,XYB,PQC,E)
    