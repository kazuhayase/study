'''
Created on 2016/12/25

@author: kazuyoshi
'''
INF=1<<32

def solve(n,m,a,b,t,g):
    dp=[[INF for i in range(1<<n)] for j in range (m+1)]
    dp[a-1][(1<<n)-1]=0
    res=INF
    for S in range((1<<n)-1, -1, -1):
        res=min(res, dp[b-1][S])
        for v in range(m):
            for i in range(n):
                if (S>>i) & 1:
                    for e in g[v]:
                        dp[e[0]][S & ~(1<<i)] = min(dp[e[0]][S & ~(1<<i)], dp[v][S] + e[1]/t[i])
    if res == INF:
        return("Impossible")
    else:
        return ("{:.3f}".format(res))


if __name__ == '__main__':
    n=2
    m=4
    a=2
    b=1
    t=(3,1)
    g=[[],[(3,3),(4,2)],[(3,3),(4,5)],[(1,3),(2,3)],[(1,2),(2,5)]]
    print(solve(n,m,a,b,t,g))
    