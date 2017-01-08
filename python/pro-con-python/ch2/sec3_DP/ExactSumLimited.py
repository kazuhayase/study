'''
Created on 2016/11/27

@author: kazuyoshi
'''

if __name__ == '__main__':
    n=int(input())
    a=list(map(int,input().split()))
    m=list(map(int,input().split()))
    K=int(input())
    N=100
    
    dp=dict()
    for j in range(K+1):
        dp[0,j]=-1
    dp[0,0]=0
    for i in range(n):
        for j in range(K+1):
            if dp[i,j] >= 0:
                dp[i+1,j]=m[i]
            elif j<a[i] or dp[i+1,j-a[i]]<=0:
                dp[i+1,j]=-1
            else:
                dp[i+1,j]=dp[i+1,j-a[i]]-1
    if dp[n,K]>=0:
        print("Yes")
    else:
        print("No")
                