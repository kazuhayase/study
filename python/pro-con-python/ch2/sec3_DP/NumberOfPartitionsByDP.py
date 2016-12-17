'''
Created on 2016/11/27

@author: kazuyoshi
'''

if __name__ == '__main__':
    n=int(input())
    m=int(input())
    M=int(input())
    #dp[m,n]
    #dp[i,j] = dp[i,j-i]+dp[i-1,j]
    dp=dict()
    dp[0,0]=1
    nm=max(n,m)
    for i in range(nm):
        dp[i+1,0]=0
        dp[0,i+1]=0
    for i in range(m):
        for j in range(n+1):
            if j-(i+1) >= 0:
                dp[i+1,j] = dp[i+1,j-(i+1)]+dp[i,j] % M
            else:
                dp[i+1,j] = dp[i,j]
    print("{}".format(dp[m,n]))

        