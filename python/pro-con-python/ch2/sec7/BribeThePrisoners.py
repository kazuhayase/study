'''
Created on 2016/12/11

@author: kazuyoshi
'''

INF=1<<32

def solve(P,Q,A):
    A.append(0)
    A.append(P+1)
    A.sort()
    
    dp=[[0 for i in range(Q+2)] for i in range(Q+2)]
    
    for i in range(Q+1):
        dp[i][i+1]=0
    
    for w in range(2,Q+2):
        for i in range(Q-w+2):
            j=i+w
            t=INF
            for k in range(i+1, j):
                t = min(t, dp[i][k]+dp[k][j])
            dp[i][j] = t + A[j] - A[i] -2
    return dp[0][Q+1]


if __name__ == '__main__':
    #1
    P=8
    Q=1
    A=[3]
    ans=solve(P,Q,A)
    print("P={}, Q={}, A={}, ans={}".format(P,Q,A,ans))

    #2
    P=20
    Q=3
    A=[3, 6, 14]
    ans=solve(P,Q,A)
    print("P={}, Q={}, A={}, ans={}".format(P,Q,A,ans))

