'''
Created on 2017/01/01

@author: kazuyoshi.hayase
'''

def solve(n,m,color):
    dp=[[0 for i in range(1<<m)] for j in range(2)]
    crt=0
    nxt=1
    dp[crt][0]=1
    for i in range(n-1,-1,-1):
        for j in range(m-1,-1,-1):
            for used in range(1<<m):
                if ((used>>j)&1) or color[i][j]:
                    dp[nxt][used] = dp[crt][used & ~(1<<j)]
                else:
                    res=0
                    if j+1 < m and (not ((used>>(j+1)) &1)) and (not (color[i][j+1])):
                        res += dp[crt][used | (1<<(j+1))]
                    if i+1 < n and (not (color[i+1][j])):
                        res += dp[crt][used | (1<<j)]
                    dp[nxt][used]= res % M
            crt,nxt = nxt,crt
    print(dp[crt][0])

if __name__ == '__main__':
    M=1<<32
    n=3
    m=3
    color=[[False,False,False],[False,True,False],[False,False,False]]
    solve(n,m,color)
