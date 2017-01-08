'''
Created on 2016/11/27

@author: kazuyoshi
'''

if __name__ == '__main__':
    n=int(input())
    m=int(input())
    a=list(map(int, input().split()))
    M=int(input())
    
    #dp[i+1][j] = dp[i][j] + dp[i][j-1] + ... + dp[i][j-a[i]]
    #dp[i+1][j-1] = dp[i][j-1] + ... + dp[i][j-1-a[i]]
    #dp[i+1][j] = dp[i][j] + dp[i+1][j-1] - dp[i][j-1-a[i]]
    
    dp=dict()
    for j in range(m+1):
        dp[0,j] = 0
    for i in range(n+1):
        dp[i,0] = 1
    for i in range(n):
        for j in range(1,m+1):
            if j-1-a[i] >= 0:
                dp[i+1,j]= (dp[i,j] + dp[i+1,j-1] - dp[i,j-1-a[i]] + M) % M
            else:
                dp[i+1,j]= (dp[i,j] + dp[i+1,j-1]) % M
    print("{}".format(dp[n,m]))