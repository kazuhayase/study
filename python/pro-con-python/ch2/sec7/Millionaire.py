'''
Created on 2016/12/11

@author: kazuyoshi
'''
def solve(M,P,x):
    n = 1 << M
    dp = [[0 for i in range(n+1)] for j in range(2)]
    current=0
    dp[0][n]=1.0
    for r in range(M):
        for i in range(n+1):
            jub = min(i,n-i)
            t = 0.0
            for j in range(jub+1):
                t = max(t, P * dp[current][i+j] + (1-P) * dp[current][i-j])
            dp[1-current][i]=t
        current = 1- current
    i= int (x * n / 1000000)
    return dp[current][i]

if __name__ == '__main__':
    #1
    M=1
    P=0.5
    x=500000
    ans=solve(M,P,x)
    print("M={}, P={}, x={}, ans={}".format(M,P,x,ans))
    
    #2
    M=3
    P=0.75
    x=600000
    ans=solve(M,P,x)
    print("M={}, P={}, x={}, ans={}".format(M,P,x,ans))
    