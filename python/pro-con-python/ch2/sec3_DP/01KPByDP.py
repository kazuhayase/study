'''
Created on 2016/11/26

@author: kazuyoshi
'''

import itertools

if __name__ == '__main__':
    n=int(input())
    W=int(input())
    w=list(map(int,input().split()))
    v=list(map(int,input().split()))

    dp=dict()
    
    # DP ; weight is less than or equal to j with products after i 

    for i in range(n+1):
        for j in range(W+1):
            dp[(i,j)]=0
        
    for i in range(n-1,-1,-1):
        for j in range(W+1):
            if j < w[i]:
                dp[(i,j)] = dp[(i+1,j)]
            else:
                dp[(i,j)] = max(dp[(i+1,j)], dp[(i+1,j-w[i])]+v[i])
    print("{}".format(dp[(0,W)]))
    
    # DP ; weight is less than or equal to j with products until i 
    for i in range(n+1):
        for j in range(W+1):
            dp[(i,j)]=0
    for i in range(n):
        for j in range(W+1):
            if j < w[i]:
                dp[(i+1,j)] = dp[(i,j)]
            else:
                dp[(i+1,j)] = max(dp[(i,j)], dp[(i,j-w[i])]+v[i])
    print("{}".format(dp[(n,W)]))
    
    # DP ; status (i,j)as products until i and weight is less than or equal to j 
    for i in range(n+1):
        for j in range(W+1):
            dp[(i,j)]=0
    for i in range(n):
        for j in range(W+1):
            dp[(i+1,j)] = max(dp[(i+1,j)],dp[(i,j)])
            if j + w[i] <= W:
                dp[(i+1,j+w[i])] = max(dp[(i+1,j+w[i])],dp[(i,j)]+v[i])
    print("{}".format(dp[(n,W)]))
                              
    # DP ; reuse same dp[]
    for j in range(W+1):
            dp[j]=0
    for i in range(n):
        for j in range(W,w[i]-1,-1):
            dp[j] = max(dp[j], dp[j-w[i]]+v[i])
    print("{}".format(dp[W]))
                              
    
    