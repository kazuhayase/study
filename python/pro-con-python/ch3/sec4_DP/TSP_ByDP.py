'''
Created on 2016/12/23

@author: kazuyoshi.hayase
'''

INF=1<<32

def rec(S,v,dp,n,d):
    if dp[v][S] >=0:
        return dp[v][S]
    if S == (1<<n)-1 and v==0:
        dp[v][S]=0
        return 0
    res = INF
    for u in range(n):
        if not ((S >> u) & 1):
            res = min(res, rec(S | (1<<u), u, dp,n,d) + d[v][u])
    dp[v][S] = res
    return res

def solve(n,d):
    dp=[[-1 for S in range(1<<n)] for v in range(n)]
    print(rec(0,0,dp,n,d))

if __name__ == '__main__':
    n=5
    d=[[0,3,INF,4,INF],[INF,0,5,INF,INF],[4,INF,0,5,INF],[INF,INF,INF,0,3],[7,6,INF,INF,0]]
    solve(n,d)